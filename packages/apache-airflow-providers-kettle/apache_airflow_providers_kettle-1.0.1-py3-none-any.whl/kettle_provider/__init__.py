from importlib.metadata import version

__name__ = "apache_airflow_providers_kettle"
__version__ = version(__name__)


def get_provider_info():
    return {
        "package-name": __name__,
        "name": "Kettle Apache Airflow Provider",
        "description": "A simple Apache Airflow Kettle Operator that can invoke jobs and transformations for Linux based systems.",
        "versions": ["1.0.1", "1.0.0"], 
    }
