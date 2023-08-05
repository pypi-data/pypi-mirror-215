import json
import os
import re

import requests
from flask import Flask, request, abort, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import time
import _thread

from app import authdns_zone as _authdns_zone
from app import app_service as _app_service
from app import cdn as _cdn
from app import gts as _gts
from app import service_group as _service_group
from app import health_monitors as _health_monitors
from app import dns_app_service as _dns_app_service
from app import alarm as _alarm
from app.common.transports import handle_general_dingman_cmd, handle_show_dingman_cmd

from consts import APP_KEY_PAIR, DM_NAME_SEP, APP_CMS, APP_REVIEW, HELP_LINK, LARK_BOT_API_LINK, ACCESS_TOKEN_LINK, \
    APP_SEARCH_KEY, APP_SEARCH_VAL
from app.common.consts import GRPC_LOG_LEVEL_ERROR
from grpc_instance_pool import grpc_pool, get_grpc_server_from_requests
from dns_utils import dns_cmd_handler, send_dns_alert, query_dns, update_dns, format_result

from utils import add_dm_allowed_args, catchall_policy_add_handler, api_policy_add_handler, \
    cert_add_handler, cert_del_handler, cert_set_handler, show_handler, test_handler, list_handler, \
    stat_handler, ip_handler, purge_handler, preload_handler, qitem_handler, general_handler, device_set_handler, \
    adding_queue, checking_labels, get_labels_dic, \
    get_data_arg_dic, pop_add_handler, pop_set_handler, device_add_handler, device_del_handler, pop_del_handler, \
    cdn_vendor_set_handler, ipnet_add_handler, ipnet_set_handler, ipnet_del_handler, \
    traffic_group_add_handler, isplink_add_handler, \
    isplink_del_handler, traffic_group_set_handler, \
    resource_group_add_handler, resource_group_set_handler, \
    deploy_task_add_handler, deploy_task_set_handler, deploy_task_del_handler, \
    roll_back_add_handler, roll_back_set_handler, \
    cdn_service_add_via_template_handler, cdn_service_set_via_template_handler, cdn_service_del_via_template_handler, \
    rbac_user_add_handler, rbac_user_del_handler, rbac_user_set_handler, \
    rbac_role_add_handler, rbac_role_del_handler, labels_definition_add_handler, labels_definition_del_handler,\
    libra_test_add_handler, libra_test_del_handler, libra_test_set_handler, labels_definition_set_handler,\
    base64_encode_string, domain_add_handler, domain_set_handler, domain_del_handler, \
    namespace_set_handler, namespace_add_handler, namespace_del_handler, \
    project_set_handler, project_add_handler, project_del_handler, \
    netpool_set_handler, netpool_add_handler, netpool_del_handler, \
    make_error_response, obj_type_roll_back_add_handler, obj_type_roll_back_set_handler, adding_token, \
    get_token_from_request, set_default_labels_for_cdn_profile, encode_dingman_response, \
    encode_deploy_resources, encode_deploy_resource_overlays, get_user_from_token, validate_cdn_edge_syntax, \
    process_xflow_field, encode_deploy_platform_resources

if os.path.isfile("api_server_token.py"):
    from api_server_token import DINGMAN_TOKENS, GENERAL_ADMIN, DNS_ADMIN
    print("dingman tokens", DINGMAN_TOKENS, flush=True)
else:
    DINGMAN_TOKENS = {}
    GENERAL_ADMIN = {}
    DNS_ADMIN = {}
    print("dingman tokens", DINGMAN_TOKENS, flush=True)

CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")
STAGING = int(os.environ.get("STAGING", 0))

STAT_ARGS_LIST = ['country', 'domain', 'start', 'end', 'interval', 'estimate', 'response', 'response-detail', 'pop',
                  'queue', 'cdn-vendor', 'format']
TEST_ARGS_LIST = ['resolve', 'domain', 'tls-version', 'http-version', 'byte-range', 'test-type', 'queue']

API_POP_KEY_DICT = dict([('pop-type', ""), ('pop', ""), ('namespace', ""), ('pop-region', ""),
                         ('disable', ""), ('capacity', ""), ('no-stats', ""), ('disable-reason', "")])

API_DEVICE_KEY_DICT = dict([('external-service', ""), ('namespace', ""), ('alias', ""), ('ttl', ""), ('device', ""),
                            ('pop', ""), ('region', ""), ('private-ip', []), ('public-ip', []), ('service-ip', [])])

CDN_VENDOR_KEY_DICT = dict([('rtt-refresh', ''), ('rtt-period', ''), ('es-user', ''),
                            ('es-passwd', ''), ('es-url', ''),
                            ('rtt-interval', ''), ('enable-log', ''),
                            ('snmp-data-timeout', ''), ('snmp-api-timeout', ''),
                            ('nic-api-timeout', ''), ('playcnt-period', ''),
                            ('snmp-url', ''), ('origin-cost-url', ''), ('origin-cost-timeout', ''),
                            ('origin-cost-interval', '')])

API_DOMAIN_KEY_DICT = dict([('service-type', ""), ('hc-uri', ""), ('type', ""), ('ttl', ""), ('dns-type', ""),
                            ('dns-data', []), ('is-host-regex', "")])

ENABLE_LARK_IP_RESET = True
RUN_LOCAL = False
APP_NAME = APP_CMS


def get_client_ip(request):
    """
    Get client ip address.

    Detect ip address provided by HTTP_X_REAL_IP, HTTP_X_FORWARDED_FOR
    and REMOTE_ADDR meta headers.

    :param request: django request
    :return: ip address
    """

    real_ip = request.environ.get('HTTP_X_REAL_IP')
    if real_ip:
        print('real ip is', real_ip)
        return real_ip

    x_forwarded_for = request.environ.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        print('forward ip is', x_forwarded_for.split(',')[0])
        return x_forwarded_for.split(',')[0]
    # print('remote ip is', request.environ.get('REMOTE_ADDR'))
    return request.environ.get('REMOTE_ADDR')


# this function is only for checking if client configured token for now
def rbac_check(user, token):
    if token:
        return True
    else:
        return False


def get_parent_name(name: str) -> str:
    name_list = name.split(DM_NAME_SEP)
    return name_list[-1] if len(name_list) > 1 else ''


def get_base_name(name: str) -> str:
    name_list = name.split(DM_NAME_SEP)
    return name_list[0]


def get_full_name(*argv) -> str:
    return DM_NAME_SEP.join(list(argv))


def parse_device_name(device, pop):
    pop_name = get_parent_name(device)
    if pop:
        if pop_name != pop and device != 'all':
            device = get_full_name(device, pop)
    elif pop_name:
        pop = pop_name
    return device, pop


def check_purge_token(token):
    if check_admin_token(token):
        return True
    if DINGMAN_TOKENS:
        if 'purge' in DINGMAN_TOKENS.keys():
            if token in DINGMAN_TOKENS['purge']:
                return True
    return True


def check_namespace_token(token, namespace):
    if check_admin_token(token):
        return True
    if DINGMAN_TOKENS:
        if namespace in DINGMAN_TOKENS.keys():
            if token == DINGMAN_TOKENS[namespace]:
                return True
    return False


def check_admin_token(token):
    if DINGMAN_TOKENS:
        if 'admin' in DINGMAN_TOKENS.keys():
            if token == DINGMAN_TOKENS['admin']:
                return True
    return True


def create_app(**config):
    port = str(config.get('port', '30301'))
    lark_app_name = str(config.get('lark_app_name', 'cms'))
    if RUN_LOCAL:
        host = str(config.get('host', 'dingman'))
    else:
        host = str(os.environ.get('DINGMAN_GRPC_HOST', 'localhost'))
    _GRPC_SERVER_SOCKET = ":".join([host, port])
    GRPC_POOL = grpc_pool(server_socket=_GRPC_SERVER_SOCKET)
    app = Flask(__name__)
    # app.wsgi_app = ProfilerMiddleware(app.wsgi_app)
    app.config['DEBUG'] = False
    CORS(app, origins=[CORS_ORIGINS])
    limiter = Limiter(app=app, key_func=get_remote_address)

    @app.route('/xflow/add_dns', methods=['post'])
    def xflow_add_dns():
        grpc_server = GRPC_POOL.get_default_grpc_server()
        ret, res = update_dns(grpc_server.cli, request, replace=False, originator='xflow')
        return jsonify(format_result(ret, res, originator='xflow'))

    @app.route('/xflow/update_dns', methods=['post'])
    def xflow_update_dns():
        grpc_server = GRPC_POOL.get_default_grpc_server()
        ret, res = update_dns(grpc_server.cli, request, replace=True, originator='xflow')
        return jsonify(format_result(ret, res, originator='xflow'))

    @app.route('/tlb/query', methods=['get'])
    def tlb_query():
        grpc_server = GRPC_POOL.get_default_grpc_server()
        ret, res = query_dns(grpc_server.cli, request)
        return jsonify(result=format_result(ret, res))

    @app.route('/tlb/add_dns', methods=['post'])
    def tlb_add_dns():
        grpc_server = GRPC_POOL.get_default_grpc_server()
        ret, res = update_dns(grpc_server.cli, request, replace=False)
        return jsonify(result=format_result(ret, res))

    @app.route('/tlb/update_dns', methods=['post'])
    def tlb_update_dns():
        grpc_server = GRPC_POOL.get_default_grpc_server()
        ret, res = update_dns(grpc_server.cli, request, replace=True)
        return jsonify(result=format_result(ret, res))
        # grpc_server = GRPC_POOL.get_default_grpc_server()
        # print(general_handler(grpc_server.cli, "set dns-domain:otn.byted.byted.org dns-type:A dns-ttl:60 dns-rdata:10.8.9.70", {}, []))
        # print(general_handler(grpc_server.cli, "set dns-domain:otn1.byted.byted.org dns-type:A dns-ttl:60 dns-rdata:10.8.9.70", {}, []))
        # return jsonify("{}")

    @app.route('/')
    @app.route('/index')
    def index():
        return jsonify("Hello, World!")

    @app.route('/stat', methods=['get'])
    @app.route('/stats', methods=['get'])
    @limiter.limit("2/second")
    def stat():
        dic = dict()
        print(STAT_ARGS_LIST, request.args, flush=True)
        for k in STAT_ARGS_LIST:
            if request.args.get(k):
                dic[k] = request.args.get(k)
        print('dic', dic, flush=True)
        return jsonify(stat_handler(get_grpc_server_from_requests(request, GRPC_POOL), dic))

    @app.route('/v1/app-service/<app_svc_name>/deploy-resources', methods=['put'])
    def put_deploy_resources(app_svc_name):
        req_body = request.get_json()
        body = base64_encode_string(json.dumps(req_body), 'utf-8')
        token = get_token_from_request(request)
        cmd = 'set app-service:{0} deploy-resources:{1} token:{2}'.format(app_svc_name, body, token)
        return handle_general_dingman_cmd(
            get_grpc_server_from_requests(request, GRPC_POOL), cmd, encode_dingman_response)

    @app.route('/v1/app-service/<app_svc_name>/deploy-resources', methods=['patch'])
    def patch_deploy_resources(app_svc_name):
        req_body = request.get_json()
        body = base64_encode_string(json.dumps(req_body), 'utf-8')
        token = get_token_from_request(request)
        cmd = 'set app-service:{0} deploy-resources:{1} patch:true token:{2}'.format(app_svc_name, body, token)
        return handle_general_dingman_cmd(
            get_grpc_server_from_requests(request, GRPC_POOL), cmd, encode_dingman_response)

    @app.route('/v1/app-service/<app_svc_name>/deploy-resources/<pop_name>', methods=['get'])
    @app.route('/v1/app-service/<app_svc_name>/deploy-resources/', methods=['get'])
    def show_deploy_resources(app_svc_name, pop_name=''):
        token = get_token_from_request(request)
        cmd = 'show app-service:{0} deploy-resources:true pop:{1} token:{2}'.format(app_svc_name, pop_name, token)
        return handle_general_dingman_cmd(
            get_grpc_server_from_requests(request, GRPC_POOL), cmd, encode_deploy_resources)

    @app.route('/v1/app-service/<app_svc_name>/deploy-resource-overlays', methods=['put'])
    def put_deploy_resource_overlays(app_svc_name):
        req_body = request.get_json()
        body = base64_encode_string(json.dumps(req_body), 'utf-8')
        token = get_token_from_request(request)
        cmd = 'set app-service:{0} deploy-resource-overlays:{1} token:{2}'.format(app_svc_name, body, token)
        return handle_general_dingman_cmd(
            get_grpc_server_from_requests(request, GRPC_POOL), cmd, encode_dingman_response)

    @app.route('/v1/app-service/<app_svc_name>/deploy-resource-overlays', methods=['get'])
    def show_deploy_resource_overlays(app_svc_name):
        token = get_token_from_request(request)
        cmd = 'show app-service:{0} deploy-resource-overlays:true token:{1}'.format(app_svc_name, token)
        return handle_general_dingman_cmd(
            get_grpc_server_from_requests(request, GRPC_POOL), cmd, encode_deploy_resource_overlays)

    @app.route('/v1/app-service/<app_svc_name>/deploy-resource-overlays', methods=['patch'])
    def patch_deploy_resource_overlays(app_svc_name):
        req_body = request.get_json()
        body = base64_encode_string(json.dumps(req_body), 'utf-8')
        token = get_token_from_request(request)
        cmd = 'set app-service:{0} deploy-resource-overlays:{1} patch:true token:{2}'.format(app_svc_name, body, token)
        return handle_general_dingman_cmd(
            get_grpc_server_from_requests(request, GRPC_POOL), cmd, encode_dingman_response)

    @app.route('/v1/app-service/<app_svc_name>/deploy-platform-resources/<pop_name>', methods=['get'])
    @app.route('/v1/app-service/<app_svc_name>/deploy-platform-resources', methods=['get'])
    def show_deploy_platform_resources(app_svc_name, pop_name=''):
        token = get_token_from_request(request)
        cmd = 'show app-service:{0} deploy-platform-resources:true pop:{1} token:{2}'\
            .format(app_svc_name, pop_name, token)
        return handle_general_dingman_cmd(
            get_grpc_server_from_requests(request, GRPC_POOL), cmd, encode_deploy_platform_resources)

    def show_resource():
        pop = request.args.get('pop')
        cdn_vendor = request.args.get('resource-cdn-vendor')
        format = request.args.get('format')
        device = request.args.get('device')
        isplink = request.args.get('isp-link')
        region = request.args.get('region')
        queue = request.args.get('queue')
        external_service = request.args.get('external-service')
        namespace = request.args.get('namespace')
        app = request.args.get('app')
        app_service = request.args.get('app-service')
        switch = request.args.get('switch')
        admin = request.args.get('admin')
        cache = request.args.get('cache')
        xlb = request.args.get('xlb')
        lvs = request.args.get('lvs')
        node = request.args.get('node')
        cdn_related = request.args.get('cdn-related')
        dsa = request.args.get('dsa')
        search_key = request.args.get(APP_SEARCH_KEY)
        search_val = request.args.get(APP_SEARCH_VAL)
        summary = request.args.get('summary')
        token = get_token_from_request(request)
        args = request.args
        labels = get_labels_dic(args)
        content = ""
        if device:
            print('device here', flush=True)
            content = content + "device:{0}".format(device)
            if app_service:
                content = content + " app-service:{0}".format(app_service)
                if token:
                    content = content + " token:{0}".format(token)
            if switch:
                content = content + " switch:{0}".format(switch)
            if admin:
                content = content + " admin:{0}".format(admin)
            if cache:
                content = content + " cache:{0}".format(cache)
            if xlb:
                content = content + " xlb:{0}".format(xlb)
            if lvs:
                content = content + " lvs:{0}".format(lvs)
            if node:
                content = content + " node:{0}".format(node)
            if cdn_related:
                content = content + " cdn-related:{0}".format(cdn_related)
            print('adding labels for device', labels)
            content = checking_labels(content, labels)
            print('dev content', content, flush=True)
        elif external_service:
            external_service, namespace = parse_device_name(external_service, namespace)
            if not namespace or namespace == 'all':
                abort(403)
            content = content + "device:{0} pop:{1} service-type:external-service".format(external_service, namespace)
            content = checking_labels(content, labels)
        elif isplink:
            content = content + "isp-link:{0}".format(isplink)
        elif namespace:
            content = content + "pop:{0} service-type:external-service".format(namespace)
            content = checking_labels(content, labels)
        if pop:
            if len(content) > 0:
                content = content + " "
            content = content + "pop:{0} app:{1}".format(pop, app)
            if not token:
                print("RBAC no token ip is ", get_client_ip(request))
            if app_service:
                content = content + " app-service:{0}".format(app_service)
            if format and cdn_vendor:
                content = content + " cdn-vendor:{0} format:{1}".format(cdn_vendor, format)
            if dsa:
                content = content + " dsa:{0}".format(dsa)
            content = checking_labels(content, labels)
        if region:
            if len(content) > 0:
                content = content + " "
            content = content + "region:{0} app:{1}".format(region, app)
        if content:
            if token:
                content = adding_token(content, token)
            if queue:
                content = adding_queue(content, queue)
            print('content before show handler', content, flush=True)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content, search_key, search_val)
        return ""

    def show_cert():
        cert = request.args.get('cert-tls')
        queue = request.args.get('queue')
        search_key = request.args.get(APP_SEARCH_KEY)
        search_val = request.args.get(APP_SEARCH_VAL)
        token = get_token_from_request(request)
        args = request.args
        labels = get_labels_dic(args)
        content = ""
        if cert:
            content = "cert-tls:{0}".format(base64_encode_string(cert))
            content = add_dm_allowed_args(content, request.args, set(['cert-tls']))
            content = checking_labels(content, labels)
        if content:
            if token:
                content = adding_token(content, token)
            if queue:
                content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content, search_key, search_val)
        return ""

    def show_cdn_vendor_content():
        cdn_vendor = request.args.get('cdn-vendor')
        queue = request.args.get('queue')
        token = get_token_from_request(request)
        args = request.args
        labels = get_labels_dic(args)
        content = ""
        if cdn_vendor:
            content = content + 'show cdn-vendor:{0}'.format(cdn_vendor)
            content = add_dm_allowed_args(content, request.args, {'cdn-vendor'})
            content = checking_labels(content, labels)
        if content:
            if token:
                content = adding_token(content, token)
            if queue:
                content = adding_queue(content, queue)
            return content
        return ""

    def show_traffic_group():
        traffic_group = request.args.get('traffic-group')
        cdn_vendor = request.args.get('resource-cdn-vendor')
        formatting = request.args.get('format')
        search_key = request.args.get(APP_SEARCH_KEY)
        search_val = request.args.get(APP_SEARCH_VAL)
        token = get_token_from_request(request)
        queue = request.args.get('queue')
        args = request.args
        content = ""
        if traffic_group:
            content = "traffic-group:{0}".format(traffic_group)
        if content:
            if token:
                content = adding_token(content, token)
            if cdn_vendor:
                content = content + ' cdn-vendor:{0}'.format(cdn_vendor)
                if formatting:
                    content = content + ' format'.format(formatting)
            if queue:
                content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content, search_key, search_val)
        return ""

    def show_resource_group():
        resource_group = request.args.get('resource-group')
        cdn_vendor = request.args.get('resource-cdn-vendor')
        formatting = request.args.get('format')
        search_key = request.args.get(APP_SEARCH_KEY)
        search_val = request.args.get(APP_SEARCH_VAL)
        queue = request.args.get('queue')
        args = request.args
        content = ""
        if resource_group:
            content = "resource-group:{0}".format(resource_group)
        if content:
            if cdn_vendor:
                content = content + ' cdn-vendor:{0}'.format(cdn_vendor)
                if formatting:
                    content = content + ' format'.format(formatting)
            if queue:
                content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content, search_key, search_val)
        return ""

    def show_ipnet():
        ipnet = request.args.get('ip-net')
        queue = request.args.get('queue')
        search_key = request.args.get(APP_SEARCH_KEY)
        search_val = request.args.get(APP_SEARCH_VAL)
        token = get_token_from_request(request)
        args = request.args
        content = ""
        if ipnet:
            content = "ip-net:{0}".format(ipnet)
        if content:
            if token:
                content = adding_token(content, token)
            if queue:
                content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content, search_key, search_val)
        return ""

    def show_dns_vendor():
        dns_vendor = request.args.get('dns-vendor')
        zone_files = request.args.get('zone-files')
        formatting = request.args.get('format')
        queue = request.args.get('queue')
        search_key = request.args.get(APP_SEARCH_KEY)
        search_val = request.args.get(APP_SEARCH_VAL)
        token = get_token_from_request(request)
        args = request.args
        content = ""
        if dns_vendor:
            content = "dns-vendor:{0}".format(dns_vendor)
        if content:
            if token:
                content = adding_token(content, token)
            if zone_files:
                content = content + " zone-files:{0}".format(zone_files)
            elif formatting:
                content = content + " format:{0}".format(formatting)
                print('format!!')
            if queue:
                content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content, search_key, search_val)
        return ""

    def show_deploy_task():
        deploy_task = request.args.get('deploy-task')
        cdn_vendor = request.args.get('cdn-vendor', 'bos_cdn')
        queue = request.args.get('queue')
        token = get_token_from_request(request)
        agent = request.args.get('agent')
        search_key = request.args.get(APP_SEARCH_KEY)
        search_val = request.args.get(APP_SEARCH_VAL)
        args = request.args
        labels = get_labels_dic(args)
        content = ""
        if deploy_task and cdn_vendor:
            content = "deploy-task:{0} cdn-vendor:{1}".format(deploy_task, cdn_vendor)
            content = checking_labels(content, labels)
            if agent:
                content = content + " agent:{0}".format(agent)
        if content:
            if token:
                content = adding_token(content, token)
            if queue:
                content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content, search_key, search_val)
        return ""

    def show_logop_etcd():
        elog_list = request.args.get('logop-etcd')
        token = get_token_from_request(request)
        queue = request.args.get('queue')
        search_key = request.args.get(APP_SEARCH_KEY)
        search_val = request.args.get(APP_SEARCH_VAL)
        content = ""
        if elog_list:
            content = "logop-etcd:{0}".format(elog_list)
        if content:
            if token:
                content = adding_token(content, token)
            if queue:
                content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content, search_key, search_val)
        return ""

    def show_cdn_profile():
        cdn_profile = request.args.get('cdn-profile')
        search_key = request.args.get(APP_SEARCH_KEY)
        search_val = request.args.get(APP_SEARCH_VAL)
        token = get_token_from_request(request)
        print('cdn-profile', cdn_profile)
        queue = request.args.get('queue')
        content = ""
        if cdn_profile:
            content = "cdn-profile:{0}".format(cdn_profile)
        if content:
            if token:
                content = adding_token(content, token)
            if queue:
                content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content, search_key, search_val)
        return ""

    def show_incre_cmds():
        start_incre_cmd = request.args.get('start-incre-serial-num')
        end_incre_cmd = request.args.get('end-incre-serial-num')
        incre_cmds = request.args.get('incre-cmds')
        token = get_token_from_request(request)
        queue = request.args.get('queue')
        content = ''
        if incre_cmds:
            content = content + "incre-cmds:{0}".format(incre_cmds)
        if start_incre_cmd and end_incre_cmd:
            content = content + " start-incre-serial-num:{0} end-incre-serial-num:{1}".format(start_incre_cmd,
                                                                                              end_incre_cmd)
        if content:
            if token:
                content = adding_token(content, token)
            if queue:
                content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content)
        return ""

    def show_roll_back():
        roll_back = request.args.get('roll-back')
        search_key = request.args.get(APP_SEARCH_KEY)
        search_val = request.args.get(APP_SEARCH_VAL)
        token = get_token_from_request(request)
        content = ''
        queue = request.args.get('queue')
        if roll_back:
            content = content + "roll-back:{0}".format(roll_back)
            if content:
                if token:
                    content = adding_token(content, token)
                if queue:
                    content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content, search_key, search_val)
        return ""

    def show_obj_type_roll_back():
        roll_back = request.args.get('obj-type-roll-back')
        token = get_token_from_request(request)
        content = ''
        queue = request.args.get('queue')
        if roll_back:
            content = content + "obj-type-roll-back:{0}".format(roll_back)
            if content:
                if token:
                    token = adding_token(content, token)
                if queue:
                    content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content)
        return ""

    def show_obj_history():
        obj_key = request.args.get('obj-history')
        token = get_token_from_request(request)
        content = ''
        queue = request.args.get('queue')
        if obj_key:
            content = content + "obj-type-history:{0} prefix:False".format(obj_key)
            if token:
                content = adding_token(content, token)
            if queue:
                content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content)
        return ""

    def show_obj_type_history():
        obj_type = request.args.get('obj-history-type')
        content = ''
        token = get_token_from_request(request)
        queue = request.args.get('queue')
        if obj_type:
            content = content + "obj-type-history:{0} prefix:True".format(obj_type)
            if content:
                if token:
                    content = adding_token(content, token)
                if queue:
                    content = adding_queue(content, queue)
            print(content)
            res = get_grpc_server_from_requests(request, GRPC_POOL)
            print(res)
            return show_handler(res, content)
        return ""

    def show_review_cmd():
        review_cmd = request.args.get('review-cmd')
        search_key = request.args.get(APP_SEARCH_KEY)
        search_val = request.args.get(APP_SEARCH_VAL)
        token = get_token_from_request(request)
        content = ''
        queue = request.args.get('queue')
        if review_cmd:
            content = content + "review-cmd:{0}".format(review_cmd)
            if content:
                if token:
                    content = adding_token(content, token)
                if queue:
                    content = adding_queue(content, queue)
                return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content, search_key, search_val)
        return ""

    def show_rbac_user():
        rbac_user = request.args.get('rbac-user')
        token = get_token_from_request(request)
        content = ''
        queue = request.args.get('queue')
        if rbac_user:
            print('rbac user True')
            content = content + "rbac-user:{0} token:{1}".format(rbac_user, token)
            if queue:
                content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content)
        return ""

    def show_rbac_role():
        rbac_role = request.args.get('rbac-role')
        token = get_token_from_request(request)
        content = ''
        queue = request.args.get('queue')
        if rbac_role:
            print('rbac role True')
            content = content + "rbac-role:{0} token:{1}".format(rbac_role, token)
            if queue:
                content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content)
        return ""

    def show_rbac_token():
        rbac_token_user = request.args.get('rbac-token', '')
        if not rbac_token_user:
            return ''
        search_key = request.args.get(APP_SEARCH_KEY)
        search_val = request.args.get(APP_SEARCH_VAL)
        jwt_used = 'false'
        token = get_token_from_request(request)
        content = ''
        queue = request.args.get('queue')
        if rbac_token_user == 'all':
            user = get_user_from_token(token)
            if user:
                rbac_token_user = user
                jwt_used = 'true'
        content = content + "rbac-token:{0} token:{1} jwt:{2}".format(rbac_token_user, token, jwt_used)
        if queue:
            content = adding_queue(content, queue)
        return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content, search_key, search_val)

    def show_libra_test():
        libra_test_name = request.args.get('libra-test')
        search_key = request.args.get(APP_SEARCH_KEY)
        search_val = request.args.get(APP_SEARCH_VAL)
        if libra_test_name:
            token = get_token_from_request(request)
            content = ''
            queue = request.args.get('queue')
            content = content + "libra-test:{0} token:{1}".format(libra_test_name, token)
            if queue:
                content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content, search_key, search_val)
        return ""

    def show_labels_definition():
        labels_definition = request.args.get('labels-definition')
        store_object_type = request.args.get('store-object-type')
        token = get_token_from_request(request)
        content = ''
        queue = request.args.get('queue')
        if labels_definition:
            print('labels definition True')
            content = content + "labels-definition:{0} store-object-type:{1}".format(labels_definition,
                                                                                     store_object_type)
            if content:
                if token:
                    content = adding_token(content, token)
                if queue:
                    content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content)
        return ""

    def show_namespace():
        namespace = request.args.get('namespace')
        queue = request.args.get('queue')
        token = get_token_from_request(request)
        content = ""
        if namespace:
            content = "namespace:{0}".format(namespace)
        if content:
            if token:
                content = adding_token(content, token)
            if queue:
                content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content)
        return ""

    def show_project():
        project = request.args.get('project')
        token = get_token_from_request(request)
        queue = request.args.get('queue')
        content = ""
        if project:
            content = "project:{0}".format(project)
        if content:
            if token:
                content = adding_token(content, token)
            if queue:
                content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content)
        return ""

    def show_netpool():
        netpool = request.args.get('net-pool')
        queue = request.args.get('queue')
        token = get_token_from_request(request)
        content = ""
        if netpool:
            content = "net-pool:{0}".format(netpool)
        if content:
            if token:
                content = adding_token(content, token)
            if queue:
                content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content)
        return ""

    @app.route('/show-multi', methods=['get'])
    def show_multi():
        print('show multi paths')
        data_types = ['deploy-task', 'app-service']
        token = get_token_from_request(request)
        cmds = []
        for data_type in data_types:
            data = request.args.get(data_type)
            if not data:
                continue
            cmd = 'show {0}:{1}'.format(data_type, data)
            args = get_data_arg_dic(request.args, data_type)
            labels = {}
            labels_prefix = 'label.'
            for key in args:
                if key.startswith(labels_prefix):
                    real_key = key[len(labels_prefix):]
                    labels[real_key] = args[key]
                else:
                    cmd = cmd + ' {0}:{1}'.format(key, args[key])
            cmd = checking_labels(cmd, labels)
            if token:
                cmd = cmd + ' token:{0}'.format(token)
            if cmd:
                cmds.append(cmd)
        combined_cmd = "\n".join(cmds)
        resp = get_grpc_server_from_requests(request, GRPC_POOL).run(combined_cmd)
        return jsonify(json.loads(resp))

    @app.route('/show', methods=['get'])
    def show():
        print('show path')
        domain = request.args.get('domain')
        service = request.args.get('service')
        cdn_path = request.args.get('cdn-path')
        cdn_vendor = request.args.get('cdn-vendor')
        search_key = request.args.get(APP_SEARCH_KEY)
        search_val = request.args.get(APP_SEARCH_VAL)
        queue = request.args.get('queue')
        token = get_token_from_request(request)
        if service:
            if token:
                service = adding_token(service, token)
            if queue:
                print('service')
                service = adding_queue(service, queue)
            return jsonify(show_handler(get_grpc_server_from_requests(request, GRPC_POOL), service, search_key,
                                        search_val))
        if cdn_path and cdn_vendor:
            print('cdn-path')
            content = "show cdn-path:{0} cdn-vendor:{1}".format(cdn_path, cdn_vendor)
            if content:
                if token:
                    content = adding_token(content, token)
                if queue:
                    content = adding_queue(content, queue)
            return handle_show_dingman_cmd(get_grpc_server_from_requests(request, GRPC_POOL),
                                           content, (search_key, search_val))

        cli = get_grpc_server_from_requests(request, GRPC_POOL)

        if request.args.get(_cdn.service_group.transports.ENTITY_CDN_SERVICE_GROUP) is not None:
            return _cdn.service_group.transports.show(cli, request)
        if request.args.get(_cdn.service.transports.ENTITY_CDN_SERVICE) is not None:
            return _cdn.service.transports.show(cli, request)
        if request.args.get(_cdn.policy.transports.ENTITY_CDN_POLICY) is not None:
            return _cdn.policy.transports.show(cli, request)
        if request.args.get(_cdn.origin.transports.ENTITY_CDN_ORIGIN) is not None:
            return _cdn.origin.transports.show(cli, request)
        if request.args.get(_cdn.ingress_host.transports.ENTITY_CDN_INGRESS_HOST) is not None:
            return _cdn.ingress_host.transports.show(cli, request)

        cert = show_cert()
        if cert:
            print('cert')
            return jsonify(cert)
        cdn_vendor = show_cdn_vendor_content()
        if cdn_vendor:
            return handle_show_dingman_cmd(get_grpc_server_from_requests(request, GRPC_POOL),
                                           cdn_vendor, (search_key, search_val))
        logop_etcd = show_logop_etcd()
        if logop_etcd:
            print('logop-etcd')
            return jsonify(logop_etcd)
        namespace = show_namespace()
        if namespace:
            print('namespace')
            return jsonify(namespace)
        project = show_project()
        if project:
            print('project')
            return jsonify(project)
        netpool = show_netpool()
        if netpool:
            print('net-pool')
            return jsonify(netpool)
        resource = show_resource()
        if resource:
            print('resource')
            return jsonify(resource)
        traffic_group = show_traffic_group()
        if traffic_group:
            print('tg')
            return jsonify(traffic_group)
        resource_group = show_resource_group()
        if resource_group:
            print('resource-group')
            return jsonify(resource_group)
        ipnet = show_ipnet()
        if ipnet:
            print('ipnet')
            return jsonify(ipnet)

        if request.args.get(_app_service.app.transports.ENTITY_APP) is not None:
            return _app_service.app.transports.show(cli, request)
        if request.args.get(_app_service.app_service.transports.ENTITY_APP_SERVICE) is not None:
            return _app_service.app_service.transports.show(cli, request)

        dns_vendor = show_dns_vendor()
        if dns_vendor:
            print('dns-vendor')
            return jsonify(dns_vendor)
        incre_cmds = show_incre_cmds()
        if incre_cmds:
            print('incre-cmds')
            return jsonify(incre_cmds)
        roll_back = show_roll_back()
        if roll_back:
            print('roll-back')
            return jsonify(roll_back)
        obj_type_roll_back = show_obj_type_roll_back()
        if obj_type_roll_back:
            print('obj_type_roll_back')
            return jsonify(obj_type_roll_back)
        obj_history = show_obj_history()
        if obj_history:
            print('obj-history')
            return jsonify(obj_history)
        obj_type_history = show_obj_type_history()
        if obj_type_history:
            print('obj_type_history')
            return jsonify(obj_type_history)
        review_cmd = show_review_cmd()
        if review_cmd:
            print('review-cmd')
            return jsonify(review_cmd)
        rbac_user = show_rbac_user()
        if rbac_user:
            print('rbac-user')
            return jsonify(rbac_user)
        rbac_role = show_rbac_role()
        if rbac_role:
            print('rbac-role')
            return jsonify(rbac_role)
        libra_test = show_libra_test()
        if libra_test:
            print('libra-test')
            return jsonify(libra_test)
        labels_definition = show_labels_definition()
        if labels_definition:
            print('labels-definition')
            return jsonify(labels_definition)
        if domain:
            print("show domain path")
            domain_type = request.args.get('domain-type', 'normal').lower()
            enable_status_check = request.args.get('domain-status-check', 'false')
            domain_content = "domain:{0} domain-type:{1}".format(domain, domain_type)
            if enable_status_check:
                domain_content = domain_content + " domain-status-check:{0}".format(enable_status_check)
            if domain_content:
                if token:
                    domain_content = adding_token(domain_content, token)
                if queue:
                    domain_content = adding_queue(domain_content, queue)
            print("domain content", domain_content)
            return jsonify(show_handler(get_grpc_server_from_requests(request, GRPC_POOL), domain_content,
                                        search_key, search_val))
        deploy_task = show_deploy_task()
        if deploy_task:
            print('deploy-task')
            return jsonify(deploy_task)

        if request.args.get(_authdns_zone.transports.ENTITY_AUTH_DNS_ZONE) is not None:
            return _authdns_zone.transports.show(cli, request)
        if request.args.get(_gts.zones.transports.ENTITY_GTS_DNS_ZONE) is not None:
            return _gts.zones.transports.show(cli, request)
        if request.args.get(_gts.policy.transports.ENTITY_GTS_POLICY) is not None:
            return _gts.policy.transports.show(cli, request)
        if request.args.get(_gts.ruleset.transports.ENTITY_GTS_RULESET) is not None:
            return _gts.ruleset.transports.show(cli, request)
        if request.args.get(_gts.view.transports.ENTITY_GTS_VIEW) is not None:
            return _gts.view.transports.show(cli, request)
        if request.args.get(_gts.region_map.transports.ENTITY_REGION_MAP) is not None:
            return _gts.region_map.transports.show(cli, request)
        if request.args.get(_service_group.transports.ENTITY_SERVICE_GROUP) is not None:
            return _service_group.transports.show(cli, request)
        if request.args.get(_health_monitors.transports.ENTITY_HEALTH_MONITOR) is not None:
            return _health_monitors.transports.show(cli, request)
        if request.args.get(_alarm.transports.ENTITY_ALARM) is not None:
            return _alarm.transports.show(cli, request)

        cdn_profile = show_cdn_profile()
        if cdn_profile:
            print('cdn-profile')
            return jsonify(cdn_profile)

        print('rbac-token here')
        rbac_token_user = show_rbac_token()
        if rbac_token_user:
            print('rbac-token')
            return jsonify(rbac_token_user)

        # Return HTTP 404 if none of the above matches.
        abort(make_error_response("not found", 404))

    @app.route('/ip', methods=['get'])
    @limiter.limit("10/second")
    def ip():
        ips = request.args.get('ip')
        ipdb_type = request.args.get('ipdb-type')
        queue = request.args.get('queue')
        token = get_token_from_request(request)
        return jsonify(ip_handler(get_grpc_server_from_requests(request, GRPC_POOL), ips, ipdb_type, queue, token))

    @app.route('/qitem', methods=['get'])
    @limiter.limit("10/second")
    def qitem():
        qitems = request.args.get('qitem')
        queue = request.args.get('queue')
        token = get_token_from_request(request)
        return jsonify(qitem_handler(get_grpc_server_from_requests(request, GRPC_POOL), qitems, queue, token))

    @app.route('/v2/querydomain', methods=['get'])
    @limiter.limit("100/second")
    def querydomain():
        domain = request.args.get('domain')
        queue = request.args.get('queue')
        token = get_token_from_request(request)
        search_key = request.args.get(APP_SEARCH_KEY)
        search_val = request.args.get(APP_SEARCH_VAL)
        if domain:
            print("show domain path")
            domain_type = request.args.get('domain-type', 'normal').lower()
            enable_status_check = request.args.get('domain-status-check', 'false')
            if domain_type == 'regex' or domain_type == 'wildcard':
                domain = ','.join([base64_encode_string(item) for item in domain.split(',')])
            domain_content = "domain:{0} domain-type:{1}".format(domain, domain_type)
            if enable_status_check:
                domain_content = domain_content + " domain-status-check:{0}".format(enable_status_check)
            if domain_content:
                if token:
                    domain_content = adding_token(domain_content, token)
                if queue:
                    domain_content = adding_queue(domain_content, queue)
            print("domain content", domain_content)
            return jsonify(show_handler(get_grpc_server_from_requests(request, GRPC_POOL), domain_content,
                                        search_key, search_val))

    @app.route('/list', methods=['get'])
    def list():
        domain = request.args.get('cdn-vendor')
        queue = request.args.get('queue')
        ipnet = request.args.get('ip-net')
        token = get_token_from_request(request)
        if domain:
            return jsonify(list_handler(get_grpc_server_from_requests(request, GRPC_POOL), domain, 'cdn-vendor', queue, token))
        elif ipnet:
            return jsonify(list_handler(get_grpc_server_from_requests(request, GRPC_POOL), ipnet, 'ip-net', queue, token))
        else:
            abort(409)

    @app.route('/test', methods=['get'])
    @limiter.limit("5/second")
    def test():
        dic = dict()
        for k in TEST_ARGS_LIST:
            if request.args.get(k):
                dic[k] = request.args.get(k)
        token = get_token_from_request(request)
        return jsonify(test_handler(get_grpc_server_from_requests(request, GRPC_POOL), dic, token))

    @app.route('/load_test', methods=['get'])
    def server_load_test():
        return jsonify('test path hit')

    @app.route('/purge', methods=['post'])
    @limiter.limit("50/second")
    def purge():
        body = request.json
        if not body:
            abort(404)
        cdn_vendor = body.get('cdn-vendor', '')
        purge_type = body.get('purge-type', '')
        purge_layers = body.get('purge-layer', [])
        urls = body.get('urls', [])
        token = get_token_from_request(request)
        queue = body.get('queue')
        if not check_purge_token(token) or len(urls) > 1000:
            abort(403)
        return jsonify(
            purge_handler(get_grpc_server_from_requests(request, GRPC_POOL), cdn_vendor, urls, purge_type, queue,
                          purge_layers=purge_layers, token=token))

    @app.route('/preload', methods=['post'])
    @limiter.limit("50/second")
    def preload():
        body = request.json
        if not body:
            abort(404)
        cdn_vendor = body.get('cdn-vendor', '')
        urls = body.get('urls', [])
        app = body.get('app', '')
        region = body.get('region', '')
        country = body.get('country', '')
        app_service = body.get('app-service', '')
        token = get_token_from_request(request)
        queue = body.get('queue')
        if not check_purge_token(token) or len(urls) > 1000:
            abort(403)
        res = preload_handler(get_grpc_server_from_requests(request, GRPC_POOL), cdn_vendor, urls, app, region, country,
                              app_service, queue, token)
        return jsonify(res)

    @app.route('/add', methods=['post'])
    @limiter.limit("5/second")
    def add():
        body = request.json
        if not body:
            abort(404)
        cert = body.get('cert-tls', '')
        print('cert', cert, flush=True)
        pop = body.get('pop', '')
        namespace = body.get('namespace', '')
        project = body.get('project', '')
        print('pop', pop, flush=True)
        print('namespace', namespace, flush=True)
        device = body.get('device', '')
        external_service = body.get('external-service', '')
        print('device', device, flush=True)
        print('external-service', external_service, flush=True)
        netpool = body.get('net-pool', '')
        ipnet = body.get('ip-net', '')
        traffic_group = body.get('traffic-group', '')
        resource_group = body.get('resource-group', '')
        isplink = body.get('isp-link', '')
        deploy_task = body.get('deploy-task', '')
        catchall_policy = body.get('catchall-policy', '')
        api_policy = body.get('api-policy', '')
        roll_back = body.get('roll-back', '')
        obj_type_roll_back = body.get('obj-type-roll-back', '')
        roll_back_revision = body.get('roll-back-revision', '')
        rbac_user = body.get('rbac-user', '')
        rbac_role = body.get('rbac-role', [])
        domain = body.get('domain')
        libra_test = body.get('libra-test', '')
        print('body', body)
        labels = get_labels_dic(body)
        print('labels', labels)
        token = get_token_from_request(request)
        queue = body.get('queue')
        user = body.get('user', '')
        labels_definition = body.get('labels-definition')

        cli = get_grpc_server_from_requests(request, GRPC_POOL)

        if body.get(_cdn.service.transports.ENTITY_CDN_SERVICE) is not None:
            return _cdn.service.transports.add(cli, request)
        if body.get(_cdn.policy.transports.ENTITY_CDN_POLICY) is not None:
            return _cdn.policy.transports.add(cli, request)
        if body.get(_cdn.origin.transports.ENTITY_CDN_ORIGIN) is not None:
            return _cdn.origin.transports.add(cli, request)
        if body.get(_cdn.ingress_host.transports.ENTITY_CDN_INGRESS_HOST) is not None:
            return _cdn.ingress_host.transports.add(cli, request)

        if cert:
            print('add cert!', flush=True)
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels)
            ret = cert_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), cert,
                                   body, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif device:
            device, pop = parse_device_name(device, pop)
            print('device parsed', device, flush=True)
            if not pop:
                abort(403)
            print('adding device')
            device_para_dict = {}
            for key in API_DEVICE_KEY_DICT:
                device_para_dict[key] = body.get(key, API_DEVICE_KEY_DICT[key])
            device_para_dict['device'] = device
            device_para_dict['pop'] = pop
            print(device_para_dict['device'])
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = device_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), device_para_dict['device'],
                                     device_para_dict['pop'], device_para_dict['region'],
                                     device_para_dict['private-ip'],
                                     device_para_dict['public-ip'], device_para_dict['service-ip'],
                                     device_para_dict['alias'], device_para_dict['ttl'], labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif libra_test:
            owner = body.get('owner', '')
            cdn_type = body.get('type', '')
            libra_link = body.get('libra-link', '')
            xflow_link = body.get('xflow-link', '')
            onboarding_type = body.get('onboarding-type', '')
            region = body.get('region', '')
            vendor = body.get('vendor', '')
            vendor_status = body.get('vendor-status', '')
            target_traffic_volume = body.get('target-traffic-volume', '')
            target_traffic_percentage = body.get('target-traffic-percentage', '')
            if not owner or not libra_link:
                abort(403)
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = libra_test_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), libra_test,
                                         owner, cdn_type, libra_link, xflow_link, onboarding_type, region,
                                         vendor, vendor_status, target_traffic_volume, target_traffic_percentage,
                                         labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif labels_definition:
            description = body.get('description', [])
            store_object_type = body.get('store-object-type', '')
            input_type = body.get('type', 'str')
            example_value = body.get('example-value', [])
            ret = labels_definition_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), labels_definition,
                                                description, store_object_type, input_type, example_value, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif external_service:
            external_service, namespace = parse_device_name(external_service, namespace)
            if not check_namespace_token(token, namespace):
                abort(403)
            print('adding external-service')
            device_para_dict = {}
            for key in API_DEVICE_KEY_DICT:
                device_para_dict[key] = body.get(key, API_DEVICE_KEY_DICT[key])
            device_para_dict['external-service'] = external_service
            device_para_dict['namespace'] = namespace
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = device_add_handler(get_grpc_server_from_requests(request, GRPC_POOL),
                                     device_para_dict['external-service'],
                                     device_para_dict['namespace'], device_para_dict['private-ip'],
                                     device_para_dict['public-ip'], device_para_dict['service-ip'],
                                     device_para_dict['alias'], device_para_dict['ttl'], labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif ipnet:
            if not check_admin_token(token):
                abort(403)
            print('adding ipnet')
            ipnet = body.get('ip-net', '')
            pop = body.get('ip-net-pop', '')
            country = body.get('country', '')
            city = body.get('city', '')
            owner = body.get('owner', '')
            state = body.get('state', '')
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = ipnet_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), ipnet, pop,
                                    country, city, owner, state, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif pop:
            if not check_admin_token(token):
                abort(403)
            print('adding pop')
            region = body.get('region', '')
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = pop_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), pop, region, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif namespace:
            if not check_admin_token(token):
                abort(403)
            print('adding namespace')
            namespace = body.get('namespace', '')
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = namespace_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), namespace, labels, queue,
                                        token)
            handler_process_response(ret)
            return jsonify(ret)
        elif project:
            if not check_admin_token(token):
                abort(403)
            print('adding project')
            project = body.get('project', '')
            store_args = body.get('project-store-args', '')
            log_type = body.get('project-log-type', '')
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = project_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), project, store_args, log_type,
                                      labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif netpool:
            if not check_admin_token(token):
                abort(403)
            print('adding netpool')
            netpool = body.get('net-pool', '')
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = netpool_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), netpool, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif isplink:
            if not check_admin_token(token):
                abort(403)
            print('adding isplink')
            isplink = body.get('isp-link', '')
            link_type = body.get('link-type', '')
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = isplink_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), isplink,
                                      link_type, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif traffic_group:
            if not check_admin_token(token):
                abort(403)
            print('adding traffic_group')
            traffic_group = body.get('traffic-group', '')
            member_list = body.get('member', [])
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = traffic_group_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), traffic_group,
                                            member_list, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif resource_group:
            if not check_admin_token(token):
                abort(403)
            print('adding resource_group')
            resource_group = body.get('resource-group', '')
            member_list = body.get('member', [])
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = resource_group_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), resource_group,
                                      member_list, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)

        if body.get(_gts.region.transports.ENTITY_REGION) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _gts.region.transports.add(cli, request)

        if body.get(_app_service.app.transports.ENTITY_APP) is not None:
            return _app_service.app.transports.add(cli, request)

        if body.get(_app_service.app_service.transports.ENTITY_APP_SERVICE) is not None:
            return _app_service.app_service.transports.add(cli, request)

        if catchall_policy:
            if not check_admin_token(token):
                abort(403)
            server_name = catchall_policy.get('server_name', '')
            is_host_regex = process_xflow_field(catchall_policy.get('is_host_regex'), 'false')
            if is_host_regex.lower() == 'true':
                if not validate_cdn_edge_syntax(server_name, 'regex'):
                    abort(make_error_response("syntax of domain does not match regex syntax: {0}".format(server_name), 400))
            else:
                if not validate_cdn_edge_syntax(server_name, 'normal'):
                    abort(make_error_response("syntax of domain does not match normal syntax: {0}".format(server_name), 400))
            print('adding catchall-policy')
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = catchall_policy_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), catchall_policy,
                                              labels, queue, token)
            return jsonify(ret)
        elif api_policy:
            if not check_admin_token(token):
                abort(403)
            print('adding api-policy')
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = api_policy_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), api_policy, labels, queue,
                                         token)
            return jsonify(ret)
        elif roll_back and roll_back_revision:
            if not check_admin_token(token):
                abort(403)
            print('adding roll back')
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            incre_serial_num_list = body.get('incre-cmds-serial-list', [])
            ret = roll_back_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), roll_back,
                                        roll_back_revision, incre_serial_num_list,
                                        labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif obj_type_roll_back and roll_back_revision:
            if not check_admin_token(token):
                abort(403)
            print('adding roll back')
            ret = obj_type_roll_back_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), obj_type_roll_back,
                                                 roll_back_revision, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif rbac_user:
            if not check_admin_token(token):
                abort(403)
            print('adding rbac user')
            ret = rbac_user_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), rbac_user, rbac_role, queue,
                                        token)
            handler_process_response(ret)
            return jsonify(ret)
        elif rbac_role:
            if not check_admin_token(token):
                abort(403)
            print('adding rbac role')
            ret = rbac_role_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), rbac_role, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif domain and not body.get(_gts.zones.transports.ENTITY_GTS_DNS_ZONE):
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            domain_type = body.get('domain-type', 'normal').lower()
            if domain_type == 'regex' or domain_type == 'wildcard':
                domain = base64_encode_string(domain)
            ret = domain_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), domain, domain_type, labels, queue,
                                     token)
            handler_process_response(ret)
            return jsonify(ret)
        elif deploy_task:
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = deploy_task_add_handler(get_grpc_server_from_requests(request, GRPC_POOL), deploy_task,
                                          user, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)

        if body.get(_authdns_zone.transports.ENTITY_AUTH_DNS_ZONE) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _authdns_zone.transports.add(cli, request)
        if body.get(_gts.zones.transports.ENTITY_GTS_DNS_ZONE) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _gts.zones.transports.add(cli, request)
        if body.get(_gts.ruleset.transports.ENTITY_GTS_RULESET) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _gts.ruleset.transports.add(cli, request)
        if body.get(_gts.view.transports.ENTITY_GTS_VIEW) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _gts.view.transports.add(cli, request)
        if body.get(_gts.policy.transports.ENTITY_GTS_POLICY) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _gts.policy.transports.add(cli, request)
        if body.get(_gts.region_map.transports.ENTITY_REGION_MAP) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _gts.region_map.transports.add(cli, request)
        if body.get(_service_group.transports.ENTITY_SERVICE_GROUP) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _service_group.transports.add(cli, request)
        if body.get(_health_monitors.transports.ENTITY_HEALTH_MONITOR) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _health_monitors.transports.add(cli, request)
        if body.get(_dns_app_service.transports.ENTITY_DNS_APP_SERVICE) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _dns_app_service.transports.add(cli, request)
        if body.get(_alarm.transports.ENTITY_ALARM) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _alarm.transports.add(cli, request)

        # Return HTTP 404 if none of the above matches.
        abort(make_error_response("not found", 404))

    @app.route('/v2/add', methods=['post'])
    @limiter.limit("5/second")
    def add_cdn_service_via_template():
        body = request.json
        if not body:
            abort(404)
        cdn_vendor = body.get('cdn-vendor', '')
        cdn_service = body.get('cdn-service', '')
        cdn_policy = body.get('cdn-policy', '')
        cdn_origin = body.get('cdn-origin-list', '')
        origin_policy = body.get('origin-policy', '')
        domain_type = body.get('domain-type', 'normal').lower()
        labels = get_labels_dic(body)
        if '' in labels:
            del labels['']
        if not labels:
            labels = body.get('labels', {})
        set_default_labels_for_cdn_profile(labels)
        token = get_token_from_request(request)
        queue = body.get('queue')
        if cdn_service:
            cdn_edge = body.get('cdn-edge', [])
            cdn_origin = json.dumps(cdn_origin)
            origin_policy = json.dumps(origin_policy)
            origin_host = body.get('origin-host', '')
            if not validate_cdn_edge_syntax(cdn_edge, domain_type):
                abort(make_error_response("syntax of domain does not match domain-type: {0}".format(domain_type), 400))
            if domain_type == 'regex' or domain_type == 'wildcard':
                cdn_service = base64_encode_string(cdn_service)
                cdn_edge = [base64_encode_string(edge) for edge in cdn_edge]
            ret = cdn_service_add_via_template_handler(get_grpc_server_from_requests(request, GRPC_POOL), cdn_service,
                                                       cdn_vendor, cdn_origin,
                                                       cdn_policy, cdn_edge, origin_host, domain_type,
                                                       origin_policy, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        else:
            abort(404)

    @app.route('/v2/set', methods=['post'])
    @limiter.limit("5/second")
    def set_cdn_service_via_template():
        body = request.json
        if not body:
            abort(404)
        cdn_vendor = body.get('cdn-vendor', '')
        cdn_service = body.get('cdn-service', '')
        cdn_policy = body.get('cdn-policy', '')
        cdn_origin = body.get('cdn-origin-list', '')
        origin_policy = body.get('origin-policy', '')
        domain_type = body.get('domain_type', 'normal').lower()
        labels = get_labels_dic(body)
        if '' in labels:
            del labels['']
        if not labels:
            labels = body.get('labels', {})
        token = get_token_from_request(request)
        queue = body.get('queue')
        if cdn_service:
            cdn_edge = body.get('cdn-edge', [])
            cdn_origin = json.dumps(cdn_origin)
            origin_host = body.get('origin-host', 'nO_ChANgE')
            origin_policy = json.dumps(origin_policy)
            if domain_type == 'regex' or domain_type == 'wildcard':
                cdn_service = base64_encode_string(cdn_service)
                cdn_edge = [base64_encode_string(edge) for edge in cdn_edge]
            ret = cdn_service_set_via_template_handler(get_grpc_server_from_requests(request, GRPC_POOL), cdn_service,
                                                       cdn_vendor, cdn_origin,
                                                       cdn_policy, cdn_edge, origin_host, domain_type,
                                                       origin_policy, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        else:
            abort(404)

    @app.route('/v2/del', methods=['post'])
    @limiter.limit("5/second")
    def del_cdn_service_via_template():
        body = request.json
        if not body:
            abort(404)
        cdn_vendor = body.get('cdn-vendor', '')
        cdn_service = body.get('cdn-service', '')
        domain_type = body.get('domain-type', 'normal').lower()
        if domain_type == 'regex' or domain_type == 'wildcard':
            cdn_service = base64_encode_string(cdn_service)
        labels = get_labels_dic(body)
        if '' in labels:
            del labels['']
        token = get_token_from_request(request)
        queue = body.get('queue')
        if cdn_service:
            if not labels:
                labels = body.get('labels', {})
            ret = cdn_service_del_via_template_handler(get_grpc_server_from_requests(request, GRPC_POOL), cdn_service,
                                                       cdn_vendor, domain_type, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        else:
            abort(404)

    @app.route('/v2/review', methods=['post'])
    def review_fss():
        body = request.json
        print('in review path now body is', body, flush=True)
        if ENABLE_LARK_IP_RESET:
            challenge_resp = is_challenge(body=body)
            if challenge_resp:
                return challenge_resp
        _thread.start_new_thread(handle_review_response, (body,))
        return ''

    @app.route('/v2/show', methods=['get'])
    def show_fss():
        print('v2/show path')
        review_cmd = show_review_cmd()
        if review_cmd:
            print('review-cmd')
            return jsonify(review_cmd)
        logop_etcd = show_logop_etcd_fss()
        if logop_etcd:
            print('logop-etcd')
            return jsonify(logop_etcd)
        roll_back = show_roll_back_fss()
        if roll_back:
            print('roll-back')
            return jsonify(roll_back)
        # Return HTTP 404 if none of the above matches.
        abort(make_error_response("not found", 404))

    def show_roll_back_fss():
        roll_back = request.args.get('roll-back')
        search_key = request.args.get(APP_SEARCH_KEY)
        search_val = request.args.get(APP_SEARCH_VAL)
        token = get_token_from_request(request)
        content = ''
        queue = request.args.get('queue')
        if roll_back:
            content = content + "roll-back:{0}".format(roll_back)
            if content:
                if token:
                    content = adding_token(content, token)
                if queue:
                    content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content, search_key, search_val)
        return ""

    def show_logop_etcd_fss():
        elog_list = request.args.get('logop-etcd')
        token = get_token_from_request(request)
        queue = request.args.get('queue')
        search_key = request.args.get(APP_SEARCH_KEY)
        search_val = request.args.get(APP_SEARCH_VAL)
        content = ""
        if elog_list:
            content = "logop-etcd:{0}".format(elog_list)
        if content:
            if token:
                content = adding_token(content, token)
            if queue:
                content = adding_queue(content, queue)
            return show_handler(get_grpc_server_from_requests(request, GRPC_POOL), content, search_key, search_val)
        return ""

    @app.route('/del', methods=['post'])
    @limiter.limit("5/second")
    def delete():
        body = request.json
        if not body:
            abort(404)
        cert = body.get('cert-tls', '')
        print('cert', cert, flush=True)
        external_service = body.get('external-service', '')
        print('external-service', external_service, flush=True)
        device = body.get('device', '')
        print('device', device, flush=True)
        pop = body.get('pop', '')
        print('pop', pop, flush=True)
        isplink = body.get('isp-link', '')
        ipnet = body.get('ip-net', '')
        rbac_user = body.get('rbac-user', '')
        rbac_role = body.get('rbac-role', '')
        libra_test = body.get('libra-test', '')
        deploy_task = body.get('deploy-task', '')
        domain = body.get('domain', '')
        user = body.get('user', '')
        token = get_token_from_request(request)
        queue = body.get('queue')
        region = body.get('region', '')
        namespace = body.get('namespace', '')
        project = body.get('project', '')
        netpool = body.get('net-pool', '')
        labels_definition = body.get('labels-definition', '')

        cli = get_grpc_server_from_requests(request, GRPC_POOL)

        if body.get(_cdn.service.transports.ENTITY_CDN_SERVICE) is not None:
            return _cdn.service.transports.delete(cli, request)
        if body.get(_cdn.policy.transports.ENTITY_CDN_POLICY) is not None:
            return _cdn.policy.transports.delete(cli, request)
        if body.get(_cdn.origin.transports.ENTITY_CDN_ORIGIN) is not None:
            return _cdn.origin.transports.delete(cli, request)
        if body.get(_cdn.ingress_host.transports.ENTITY_CDN_INGRESS_HOST) is not None:
            return _cdn.ingress_host.transports.delete(cli, request)

        if cert:
            print('del cert', flush=True)
            ret = cert_del_handler(get_grpc_server_from_requests(request, GRPC_POOL),
                                   cert, body, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif device:
            print('del device', flush=True)
            site_name = body.get('pop', '')
            device, site_name = parse_device_name(device, site_name)
            ret = device_del_handler(get_grpc_server_from_requests(request, GRPC_POOL), device, site_name, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif external_service:
            namespace = body.get('namespace', '')
            external_service, namespace = parse_device_name(external_service, namespace)
            print('external-service parsed', device, flush=True)
            if not namespace:
                abort(403)
            if not check_namespace_token(token, namespace):
                abort(403)
            print('del external-service', flush=True)
            ret = device_del_handler(get_grpc_server_from_requests(request, GRPC_POOL), external_service, namespace,
                                     queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif isplink:
            if not check_admin_token(token):
                abort(403)
            print('del isplink', flush=True)
            pop_name = body.get('pop', '')
            ret = isplink_del_handler(get_grpc_server_from_requests(request, GRPC_POOL), isplink, pop_name, queue,
                                      token)
            handler_process_response(ret)
            return jsonify(ret)
        elif pop:
            if not check_admin_token(token):
                abort(403)
            print('del pop', flush=True)
            ret = pop_del_handler(get_grpc_server_from_requests(request, GRPC_POOL), pop, queue, token)
            handler_process_response(ret)
            return jsonify(ret)

        if body.get(_app_service.app_service.transports.ENTITY_APP_SERVICE) is not None:
            return _app_service.app_service.transports.delete(cli, request)

        if rbac_user:
            if not check_admin_token(token):
                abort(403)
            print("rbac user is", rbac_user, flush=True)
            ret = rbac_user_del_handler(get_grpc_server_from_requests(request, GRPC_POOL), rbac_user, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif rbac_role:
            if not check_admin_token(token):
                abort(403)
            print("rbac role is", rbac_role, flush=True)
            ret = rbac_role_del_handler(get_grpc_server_from_requests(request, GRPC_POOL), rbac_role, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif libra_test:
            ret = libra_test_del_handler(get_grpc_server_from_requests(request, GRPC_POOL), libra_test, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif labels_definition:
            ret = labels_definition_del_handler(get_grpc_server_from_requests(request, GRPC_POOL), labels_definition,
                                                queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif deploy_task:
            print('del deploy-task', flush=True)
            ret = deploy_task_del_handler(get_grpc_server_from_requests(request, GRPC_POOL), deploy_task, user, queue,
                                          token)
            handler_process_response(ret)
            return jsonify(ret)
        elif domain and not body.get(_gts.zones.transports.ENTITY_GTS_DNS_ZONE):
            print("domain is", domain, flush=True)
            domain_type = body.get('domain-type', 'normal').lower()
            if domain_type == 'regex' or domain_type == 'wildcard':
                domain = base64_encode_string(domain)
            ret = domain_del_handler(get_grpc_server_from_requests(request, GRPC_POOL), domain, domain_type, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif ipnet:
            if not check_admin_token(token):
                abort(403)
            print('delete ipnet')
            ipnet = body.get('ip-net', '')
            owner = body.get('owner', '')
            ret = ipnet_del_handler(get_grpc_server_from_requests(request, GRPC_POOL), ipnet, owner, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif namespace:
            if not check_admin_token(token):
                abort(403)
            print('del namespace', flush=True)
            namespace = body.get('namespace', '')
            ret = namespace_del_handler(get_grpc_server_from_requests(request, GRPC_POOL), namespace, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif project:
            if not check_admin_token(token):
                abort(403)
            print('del project', flush=True)
            project = body.get('project', '')
            ret = project_del_handler(get_grpc_server_from_requests(request, GRPC_POOL), project, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif netpool:
            if not check_admin_token(token):
                abort(403)
            print('del netpool', flush=True)
            netpool = body.get('net-pool', '')
            ret = netpool_del_handler(get_grpc_server_from_requests(request, GRPC_POOL), netpool, queue, token)
            handler_process_response(ret)
            return jsonify(ret)

        if body.get(_authdns_zone.transports.ENTITY_AUTH_DNS_ZONE) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _authdns_zone.transports.delete(cli, request)
        if body.get(_gts.zones.transports.ENTITY_GTS_DNS_ZONE) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _gts.zones.transports.delete(cli, request)
        if body.get(_gts.ruleset.transports.ENTITY_GTS_RULESET) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _gts.ruleset.transports.delete(cli, request)
        if body.get(_gts.view.transports.ENTITY_GTS_VIEW) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _gts.view.transports.delete(cli, request)
        if body.get(_gts.policy.transports.ENTITY_GTS_POLICY) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _gts.policy.transports.delete(cli, request)
        if body.get(_gts.region_map.transports.ENTITY_REGION_MAP) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _gts.region_map.transports.delete(cli, request)
        if body.get(_gts.region.transports.ENTITY_REGION) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _gts.region.transports.delete(cli, request)
        if body.get(_service_group.transports.ENTITY_SERVICE_GROUP) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _service_group.transports.delete(cli, request)
        if body.get(_health_monitors.transports.ENTITY_HEALTH_MONITOR) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _health_monitors.transports.delete(cli, request)
        if body.get(_alarm.transports.ENTITY_ALARM) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _alarm.transports.delete(cli, request)

        abort(make_error_response("not found", 404))

    @app.route('/set', methods=['post'])
    @limiter.limit("5/second")
    def set():
        body = request.json
        if not body:
            abort(404)
        cdn_vendor = body.get('cdn-vendor', '')
        print('vendor', cdn_vendor, flush=True)
        cert = body.get('cert-tls', '')
        print('cert', cert)
        external_service = body.get('external-service', '')
        print('external-service', external_service)
        device = body.get('device', '')
        print('device', device)
        pop = body.get('pop', '')
        print('pop', pop)
        namespace = body.get('namespace', '')
        project = body.get('project', '')
        netpool = body.get('net-pool', '')
        print('namespace', namespace)
        traffic_group = body.get('traffic-group', '')
        resource_group = body.get('resource-group', '')
        ipnet = body.get('ip-net', '')
        token = get_token_from_request(request)
        queue = body.get('queue')
        roll_back = body.get('roll-back', '')
        print('roll_back', roll_back, flush=True)
        roll_back_revision = body.get('roll-back-revision', '')
        obj_type_roll_back = body.get('obj_type_roll_back', '')
        print('roll_back_revision', roll_back_revision, flush=True)
        rbac_user = body.get('rbac-user', '')
        rbac_role = body.get('rbac-role', '')
        libra_test = body.get('libra-test', '')
        domain = body.get('domain', '')
        deploy_task = body.get('deploy-task', '')
        user = body.get('user', '')
        labels_definition = body.get('labels-definition', '')
        labels = get_labels_dic(body)

        cli = get_grpc_server_from_requests(request, GRPC_POOL)

        if body.get(_cdn.service.transports.ENTITY_CDN_SERVICE) is not None:
            return _cdn.service.transports.set(cli, request)
        if body.get(_cdn.policy.transports.ENTITY_CDN_POLICY) is not None:
            return _cdn.policy.transports.set(cli, request)
        if body.get(_cdn.origin.transports.ENTITY_CDN_ORIGIN) is not None:
            return _cdn.origin.transports.set(cli, request)
        if body.get(_cdn.ingress_host.transports.ENTITY_CDN_INGRESS_HOST) is not None:
            return _cdn.ingress_host.transports.set(cli, request)

        if cert:
            print('set cert!')
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels)
            ret = cert_set_handler(get_grpc_server_from_requests(request, GRPC_POOL),
                                   cert, body, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif cdn_vendor:
            if not check_admin_token(token):
                abort(403)
            print('set cdn-vendor!', flush=True)
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels)
            cdn_vendor_para_dict = {}
            for key in CDN_VENDOR_KEY_DICT:
                cdn_vendor_para_dict[key] = body.get(key, CDN_VENDOR_KEY_DICT[key])
            ret = cdn_vendor_set_handler(get_grpc_server_from_requests(request, GRPC_POOL),
                                         cdn_vendor, cdn_vendor_para_dict['rtt-interval'],
                                         cdn_vendor_para_dict['rtt-refresh'],
                                         cdn_vendor_para_dict['rtt-period'], cdn_vendor_para_dict['playcnt-period'],
                                         cdn_vendor_para_dict['es-user'], cdn_vendor_para_dict['es-passwd'],
                                         cdn_vendor_para_dict['es-url'], cdn_vendor_para_dict['enable-log'],
                                         cdn_vendor_para_dict['snmp-data-timeout'],
                                         cdn_vendor_para_dict['snmp-api-timeout'],
                                         cdn_vendor_para_dict['nic-api-timeout'],
                                         cdn_vendor_para_dict['origin-cost-url'],
                                         cdn_vendor_para_dict['origin-cost-timeout'],
                                         cdn_vendor_para_dict['origin-cost-interval'],
                                         cdn_vendor_para_dict['snmp-url'],
                                         labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif device:
            print('set device labels!', flush=True)
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels)
            device_para_dict = {}
            for key in API_DEVICE_KEY_DICT:
                device_para_dict[key] = body.get(key, API_DEVICE_KEY_DICT[key])
            device_para_dict['device'] = device
            device_para_dict['pop'] = pop
            print(device_para_dict['device'])
            ret = device_set_handler(get_grpc_server_from_requests(request, GRPC_POOL),
                                     device_para_dict['device'], device_para_dict['pop'],
                                     device_para_dict['private-ip'], device_para_dict['public-ip'],
                                     device_para_dict['service-ip'], device_para_dict['alias'],
                                     device_para_dict['ttl'], labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif external_service:
            device_para_dict = {}
            external_service, namespace = parse_device_name(external_service, namespace)
            if not namespace:
                abort(403)
            if not check_namespace_token(token, namespace):
                abort(403)
            print('set external-service!', flush=True)
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels)
            for key in API_DEVICE_KEY_DICT:
                device_para_dict[key] = body.get(key, API_DEVICE_KEY_DICT[key])
            device_para_dict['external-service'] = external_service
            device_para_dict['namespace'] = namespace
            ret = device_set_handler(get_grpc_server_from_requests(request, GRPC_POOL),
                                     device_para_dict['external-service'], device_para_dict['namespace'],
                                     device_para_dict['private-ip'], device_para_dict['public-ip'],
                                     device_para_dict['service-ip'], device_para_dict['alias'],
                                     device_para_dict['ttl'], labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif pop:
            if not check_admin_token(token):
                abort(403)
            print('set pop!', flush=True)
            pop_para_dict = {}
            for key in API_POP_KEY_DICT:
                pop_para_dict[key] = body.get(key, API_POP_KEY_DICT[key])
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels)
            ret = pop_set_handler(get_grpc_server_from_requests(request, GRPC_POOL),
                                  pop_para_dict, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif traffic_group:
            if not check_admin_token(token):
                abort(403)
            print('setting traffic-group')
            member_list = body.get('member', [])
            ret = traffic_group_set_handler(get_grpc_server_from_requests(request, GRPC_POOL), traffic_group,
                                            member_list, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif resource_group:
            if not check_admin_token(token):
                abort(403)
            print('setting resource-group')
            member_list = body.get('member', [])
            ret = resource_group_set_handler(get_grpc_server_from_requests(request, GRPC_POOL), resource_group,
                                                  member_list, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)

        if body.get(_app_service.app.transports.ENTITY_APP) is not None:
            return _app_service.app.transports.set(cli, request)

        if body.get(_app_service.app_service.transports.ENTITY_APP_SERVICE) is not None:
            return _app_service.app_service.transports.set(cli, request)

        if roll_back and roll_back_revision:
            if not check_admin_token(token):
                abort(403)
            print("roll back is", roll_back, flush=True)
            ret = roll_back_set_handler(get_grpc_server_from_requests(request, GRPC_POOL), roll_back,
                                        roll_back_revision, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif obj_type_roll_back:
            if not check_admin_token(token):
                abort(403)
            print("obj roll back is", obj_type_roll_back, flush=True)
            ret = obj_type_roll_back_set_handler(get_grpc_server_from_requests(request, GRPC_POOL), obj_type_roll_back,
                                                 queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif rbac_user:
            if not check_admin_token(token):
                abort(403)
            print('setting rbac user')
            ret = rbac_user_set_handler(get_grpc_server_from_requests(request, GRPC_POOL), rbac_user, rbac_role, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif libra_test:
            if not check_admin_token(token):
                abort(403)
            print('setting libra test')
            owner = body.get('owner')
            libra_link = body.get('libra-link')
            target_traffic_volume = body.get('target-traffic-volume')
            target_traffic_percentage = body.get('target-traffic-percentage')
            ret = libra_test_set_handler(get_grpc_server_from_requests(request, GRPC_POOL), libra_test, owner,
                                         libra_link, target_traffic_volume,
                                         target_traffic_percentage, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif labels_definition:
            print('set labels definition')
            description = body.get('description', [])
            store_object_type = body.get('store-object-type')
            input_type = body.get('type')
            example_value = body.get('example-value')
            ret = labels_definition_set_handler(get_grpc_server_from_requests(request, GRPC_POOL), labels_definition,
                                                description, store_object_type, input_type, example_value, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif domain and not body.get(_gts.zones.transports.ENTITY_GTS_DNS_ZONE):
            print('setting domain')
            domain_para_dict = {}
            for key in API_DOMAIN_KEY_DICT:
                domain_para_dict[key] = body.get(key, API_DOMAIN_KEY_DICT[key])
            domain_type = body.get('domain-type', 'normal').lower()
            if domain_type == 'regex' or domain_type == 'wildcard':
                domain = base64_encode_string(domain)
            ret = domain_set_handler(get_grpc_server_from_requests(request, GRPC_POOL), domain, domain_type,
                                     domain_para_dict['service-type'], domain_para_dict['hc-uri'],
                                     domain_para_dict['dns-type'],
                                     domain_para_dict['ttl'], domain_para_dict['dns-data'],
                                     domain_para_dict['is-host-regex'],
                                     labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif deploy_task:
            print('set deploy-task')
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = deploy_task_set_handler(get_grpc_server_from_requests(request, GRPC_POOL), deploy_task, user,
                                          labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif ipnet:
            if not check_admin_token(token):
                abort(403)
            print('set ipnet')
            ipnet = body.get('ip-net', '')
            pop = body.get('ip-net-pop', '')
            country = body.get('country', '')
            city = body.get('city', '')
            owner = body.get('owner', '')
            state = body.get('state', '')
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = ipnet_set_handler(get_grpc_server_from_requests(request, GRPC_POOL), ipnet, pop,
                                    country, city, owner, state, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif namespace:
            print('setting namespace')
            namespace = body.get('namespace', '')
            project = body.get('project', '')
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = namespace_set_handler(get_grpc_server_from_requests(request, GRPC_POOL), namespace, project,
                                        labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif project:
            print('setting project')
            project = body.get('project', '')
            store_args = body.get('project-store-args', '')
            log_type = body.get('project-log-type', '')
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = project_set_handler(get_grpc_server_from_requests(request, GRPC_POOL), project, store_args,
                                      log_type, labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)
        elif netpool:
            print('setting netpool')
            netpool = body.get('net-pool', '')
            subnet = body.get('subnet', '')
            if not labels:
                labels = body.get('labels', {})
                print('labels set in body', labels, flush=True)
            ret = netpool_set_handler(get_grpc_server_from_requests(request, GRPC_POOL), netpool, subnet,
                                      labels, queue, token)
            handler_process_response(ret)
            return jsonify(ret)

        if body.get(_authdns_zone.transports.ENTITY_AUTH_DNS_ZONE) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _authdns_zone.transports.set(cli, request)
        if body.get(_gts.zones.transports.ENTITY_GTS_DNS_ZONE) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _gts.zones.transports.set(cli, request)
        if body.get(_gts.ruleset.transports.ENTITY_GTS_RULESET) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _gts.ruleset.transports.set(cli, request)
        if body.get(_gts.view.transports.ENTITY_GTS_VIEW) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _gts.view.transports.set(cli, request)
        if body.get(_gts.policy.transports.ENTITY_GTS_POLICY) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _gts.policy.transports.set(cli, request)
        if body.get(_service_group.transports.ENTITY_SERVICE_GROUP) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _service_group.transports.set(cli, request)
        if body.get(_health_monitors.transports.ENTITY_HEALTH_MONITOR) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _health_monitors.transports.set(cli, request)
        if body.get(_dns_app_service.transports.ENTITY_DNS_APP_SERVICE) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _dns_app_service.transports.set(cli, request)
        if body.get(_alarm.transports.ENTITY_ALARM) is not None:
            if not check_admin_token(token):
                abort(make_error_response("unauthorized", 403))
            return _alarm.transports.set(cli, request)

        abort(make_error_response("not found", 404))

    @app.route('/lark', methods=['post'])
    def lark():
        body = request.json
        if ENABLE_LARK_IP_RESET:
            challenge_resp = is_challenge(body=body)
            if challenge_resp:
                return challenge_resp
        event = body.get('event')
        text = body.get('event').get('text_without_at_bot').strip()
        print("Msg: ", event, flush=True)
        call_back(option=text, chat_id=event.get('chat_id'), root_id=event.get('root_id'), uid=event.get('user'))
        return ''

    @app.route('/review', methods=['post'])
    def review():
        body = request.json
        print('in review path now body is', body, flush=True)
        if ENABLE_LARK_IP_RESET:
            challenge_resp = is_challenge(body=body)
            if challenge_resp:
                return challenge_resp
        _thread.start_new_thread(handle_review_response, (body,))
        return ''

    @app.route('/webhook/bge', methods=['post'])
    def bge_webhook():
        body = request.json
        print('webhook request body is', body, flush=True)
        subject_type_name = body.get('subjectTypeName', '').lower()
        subject_name = body.get('subjectKey', '').lower()
        event_name = body.get('eventTypeName', '').lower()
        dingman_rbac_token = get_token_from_request(request)
        dic = {}
        wildcard = []
        dms_server_socket = os.environ.get('DMS_GRPC_ADDRESS')
        bge_cluster_host = os.environ.get('BGE_CLUSTER_HOST')
        grpc_server = GRPC_POOL.get_selected_grpc_server(dms_server_socket)
        if subject_type_name == 'cluster':
            if event_name == 'cluster online':
                cmd = "load event:online-cluster platform:bge event-obj:{0} " \
                      "review-cmd:yes token:{1}".format(subject_name, dingman_rbac_token)
            elif event_name == 'cluster offline':
                cmd = "load event:offline-cluster platform:bge event-obj:{0} " \
                      "review-cmd:yes token:{1}".format(subject_name, dingman_rbac_token)
            else:
                return ''
            if bge_cluster_host:
                labels = {'link': f'{bge_cluster_host}?clusterName={subject_name}'}
                cmd = checking_labels(cmd, labels)
            result = general_handler(grpc_server.cli, cmd, dic, wildcard)
            print('result is ', result, flush=True)
            return result
        if subject_type_name == 'project' and event_name == 'resource update':
            cmd = "load event:sync-project platform:bge event-obj:{0}".format(subject_name)
            result = general_handler(grpc_server.cli, cmd, dic, wildcard)
            print('result is ', result, flush=True)
            return result
        return ''

    def _get_tenant_access_token():
        body = APP_KEY_PAIR[lark_app_name]
        res = requests.post(ACCESS_TOKEN_LINK,
                            data=json.dumps(body),
                            headers={'content-type': 'application/json'})
        token = json.loads(res.text).get("tenant_access_token")
        return token

    def _get_review_tenant_access_token():
        body = APP_KEY_PAIR[APP_REVIEW]
        res = requests.post(ACCESS_TOKEN_LINK,
                            data=json.dumps(body),
                            headers={'content-type': 'application/json'})
        token = json.loads(res.text).get("tenant_access_token")
        return token

    def handle_review_response(body):
        action = body.get('action')
        val_map = action.get('value')
        pop = val_map.get('pop')
        if pop is not None:
            return handle_pop_event_review_response(body)
        else:
            return handle_dingman_job_review_response(body)

    def handle_dingman_job_review_response(body):
        review_card_update_token = body.get('token')
        open_id = body.get('open_id')  # from lark card
        user_email = body.get('reviewer-email')  # from gsm-gui
        action = body.get('action')
        val_map = action.get('value')
        approve = val_map.get('approve')
        job = val_map.get('job')
        dingman_rbac_token = val_map.get('token')
        key = job
        dic = {}
        wildcard = []
        grpc_server = GRPC_POOL.get_default_grpc_server()
        if approve == "true":
            cmd = "set review-cmd:{0} review-cmd-status:approved token:{1} reviewer-open-id:{2} " \
                  "reviewer-email:{3} review-card-token:{4}".\
                format(key, dingman_rbac_token, open_id, user_email, review_card_update_token)
            result = general_handler(grpc_server.cli, cmd, dic, wildcard)
            print('result is ', result, flush=True)
        else:
            cmd = "set review-cmd:{0} review-cmd-status:declined token:{1} reviewer-open-id:{2} " \
                  "reviewer-email:{3} review-card-token:{4}".\
                format(key, dingman_rbac_token, open_id, user_email, review_card_update_token)
            time.sleep(1)
            result = general_handler(grpc_server.cli, cmd, dic, wildcard)
            print('result is ', result)
        return result

    def handle_pop_event_review_response(body):
        review_card_update_token = body.get('token')
        open_id = body.get('open_id')
        action = body.get('action')
        val_map = action.get('value')
        review_result = val_map.get('approved')
        event_type = val_map.get('event')
        if review_result:
            review_cmd = 'approved'
        else:
            review_cmd = 'declined'
        pop = val_map.get('pop')
        labels = val_map.get('labels', {})
        dingman_rbac_token = val_map.get('token')
        labels.update({
            'review_card_update_token': review_card_update_token,
            'reviewer_open_id': open_id,
            'review_cmd': review_cmd,
        })
        dic = {}
        wildcard = []
        dms_server_socket = os.environ.get('DMS_GRPC_ADDRESS')
        grpc_server = GRPC_POOL.get_selected_grpc_server(dms_server_socket)
        cmd = "load event:{0}-cluster platform:bge event-obj:{1} token:{2}".format(event_type, pop, dingman_rbac_token)
        cmd = checking_labels(cmd, labels)
        result = general_handler(grpc_server.cli, cmd, dic, wildcard)
        if result.get(GRPC_LOG_LEVEL_ERROR) is not None:
            print(f'cmd:{cmd} result: {result}', flush=True)
        return result

    def call_back(option, chat_id, **kwargs):
        user_name = ""
        cmds = option.split(' ', 1)
        if len(cmds) < 2:
            cmd, args = cmds[0], ''
        else:
            cmd, args = cmds
        # check auth for certain cmds
        if cmd in ['add', 'set', 'del'] and lark_app_name not in ['wbot', 'reviewbot']:
            content_list = []
            content = _lark_text_formatter(
                data="Sorry, the queried bot do not have access of [{cmd}].".format(cmd=cmd))
            content_list.append(content)
            _lark_return(chat_id, content_list, **kwargs)
            return
        elif cmd not in ["load", "help", "show", "list", "test", "stat", "stats", "dig", "ip", "add-dns", "set-dns",
                         'add', 'set', 'del']:
            content_list = []
            content = _lark_text_formatter(
                data="Sorry, the command [{cmd}] is not yet supported. Please check the following link:".format(
                    cmd=cmd))
            content_list.append(content)
            content = _lark_link_formatter(data="海外自建CDN运维bot使用文档 CDN Dev&Ops Bot Instustions",
                                           link=HELP_LINK)
            content_list.append(content)
            _lark_return(chat_id, content_list, **kwargs)
            return

        dic = dict()
        wildcard = []
        args = re.sub(r':\s+', ':', args)
        for item in args.split():
            if item.find(':') < 0:
                wildcard.append(item)
                continue
            k, v = item.split(':', 1)
            dic[k] = v
        server_socket = dic.get('rpc', '')
        if server_socket:
            grpc_server = GRPC_POOL.get_selected_grpc_server(server_socket=server_socket)
            dic.pop('rpc')
        else:
            grpc_server = GRPC_POOL.get_default_grpc_server()

        if cmd in ["add-dns", "set-dns"]:
            # DNS user authentication
            auth, user_name = _lark_authenticate(uid=kwargs.get('uid'), cmd=cmd, args=args)
            if not auth:
                _lark_return(chat_id, content_list=[_lark_text_formatter(data="Sorry, authentication failed")],
                             **kwargs)
                return
            # DNS zone authentication
            ok, new_dic, detail = dns_cmd_handler(args, dic)
            if not ok:
                _lark_return(chat_id, content_list=[_lark_text_formatter(data=detail)], **kwargs)
                return
            dic = new_dic
            if dic.get("region"):
                dic.pop("region")
            cmd = cmd.split('-', 1)[0]
            wildcard = []
        elif cmd in ["add", "set", "del"]:
            print("--uid:{uid}, uname:{uname}, cmd:{cmd} {args}".format(uid=kwargs.get('uid'), uname="unknown", cmd=cmd,
                                                                        args=args), flush=True)

        # Sending results
        content_list = []

        # Default callbacks
        if cmd not in ["load", "help", "show", "list", "test", "stat", "stats", "dig", "ip", "add-dns", "set-dns",
                       "add", "set"]:
            content = _lark_text_formatter(
                data="Sorry, the command [{cmd}] is not yet supported. Please check the following link:".format(
                    cmd=cmd))
            content_list.append(content)
            content = _lark_link_formatter(data="海外自建CDN运维bot使用文档 CDN Dev&Ops Bot Instustions",
                                           link=HELP_LINK)
            content_list.append(content)
            _lark_return(chat_id, content_list, **kwargs)
            return
        elif cmd in ["help"]:
            content = _lark_link_formatter(data="海外自建CDN运维bot使用文档 CDN Dev&Ops Bot Instustions",
                                           link=HELP_LINK)
            content_list.append(content)
            _lark_return(chat_id, content_list, **kwargs)
            return

        # Send query to dingman grpc server
        data = general_handler(grpc_server.cli, cmd, dic, wildcard)
        if cmd in ["load"]:
            content = _lark_text_formatter(data="Loaded")
            content_list.append(content)
        elif not data or not isinstance(data, dict) or not data.get("data"):
            print("Invalid data:", data, flush=True)
            content = _lark_text_formatter(
                data="Sorry, we failed to find the resource you requested. Please check the following link:")
            content_list.append(content)
            content = _lark_link_formatter(data="海外自建CDN运维bot使用文档 CDN Dev&Ops Bot Instustions",
                                           link=HELP_LINK)
            content_list.append(content)
        else:
            # Config changing, send alert to lark group
            if cmd in ["add-dns", "set-dns"] and not STAGING:
                send_dns_alert(dic=dic, author=user_name, detail=json.dumps(data, indent=4))
            content = _lark_text_formatter(data=json.dumps(data, indent=4))
            content_list.append(content)

        _lark_return(chat_id, content_list, **kwargs)

        return

    def is_challenge(body):
        challenge = body.get("challenge")
        if challenge:
            print("Lark bot challenge recieved", body, flush=True)
            challenge_resp = {
                "challenge": challenge
            }
            data = json.dumps(challenge_resp)
            print("Lark bot challenge resp", data, flush=True)
            return data
        return ''

    def _lark_return(chat_id, content_list=None, **kwargs):
        if not content_list:
            content_list = []
        body = _lark_callback_body_formatter(chat_id=chat_id, root_id=kwargs.get('root_id'), content_list=content_list)
        data = json.dumps(body)

        if len(data) > 64000:
            print("data to long to proceed", len(data))
            content_list = []
            content = _lark_text_formatter(
                data="Sorry, the result was to long to be shown in Lark. Please check the following link:")
            content_list.append(content)
            content = _lark_link_formatter(data="海外自建CDN运维bot使用文档 CDN Dev&Ops Bot Instustions",
                                           link=HELP_LINK)
            content_list.append(content)
            body = _lark_callback_body_formatter(chat_id=chat_id, root_id=kwargs.get('root_id'),
                                                 content_list=content_list)
            data = json.dumps(body)

        s = requests.post(LARK_BOT_API_LINK,
                          data=data,
                          headers={'Authorization': 'Bearer {token}'.format(token=_get_tenant_access_token()),
                                   'Content-Type': 'application/json'})

    def _lark_callback_body_formatter(**kwargs):
        body = {
            "chat_id": kwargs.get('chat_id'),
            "msg_type": "post",
            "root_id": kwargs.get('root_id'),
            "content": {
                "post": {
                    "zh_cn": {
                        "title": kwargs.get('title'),
                        "content": kwargs.get('content_list')
                    }
                }
            }
        }
        return body

    def _lark_text_formatter(data):
        return [
            {
                "tag": "text",
                "text": data
            },
        ]

    def _lark_link_formatter(data, link):
        return [
            {
                "tag": "a",
                "text": data,
                "href": link
            },
        ]

    def _lark_authenticate(uid, cmd, args):
        # check if user has the authentication to set/add DNS record
        if uid in GENERAL_ADMIN:
            user_name = GENERAL_ADMIN[uid]
            return True, user_name
        elif uid in DNS_ADMIN:
            user_name = DNS_ADMIN[uid]
            return True, user_name
        return False, ''

    return app


def handler_process_response(ret):
    data = ret.get('data', None)
    print('data', data)
    if data is None:
        abort(409, ret)
    if len(data) <= 0:
        abort(409, ret)
    elem = data[0]
    if elem is None:
        abort(409, ret)
    log_level = elem.get("log-level", None)
    if log_level is None:
        abort(409, ret)
    if log_level != "2":
        abort(409, ret)
    print('succeed', ret, flush=True)
