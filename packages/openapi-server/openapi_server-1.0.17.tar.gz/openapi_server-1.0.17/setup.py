import setuptools

api_version_file = "openapi_version"
api_version = "1.0.0"

try:
    with open(api_version_file, 'r') as f:
        val = f.readline().split()
        api_version = ".".join(val)
except OSError:
    print('openapi version file not found')

setuptools.setup(
    name="openapi_server",
    version=api_version,
    author="BD Data Sys IE CDN",
    description="CDN DMS Open API",
    url="https://code.byted.org/savanna/dingman_api_server",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires = [
        "gunicorn",
        "gevent",
        "flask",
        "flask-limiter",
        "flask-cors",
        "grpcio==1.47.0",
        "grpcio-tools==1.47.0",
        "protobuf==3.20.1",
        "requests",
        "ipaddress",
        "retry",
        "swagger-ui-bundle>=0.0.2",
        "python_dateutil>=2.6.0",
        "connexion[swagger-ui]>=2.6.0; python_version>='3.6'",
        "connexion[swagger-ui]<=2.3.0; python_version=='3.5' or python_version=='3.4'",
        "werkzeug == 0.16.1; python_version=='3.5' or python_version=='3.4'",
        "PyJWT"
    ]
)