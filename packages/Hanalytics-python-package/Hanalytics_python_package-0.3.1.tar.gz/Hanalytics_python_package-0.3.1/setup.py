from setuptools import setup


setup(
    name="Hanalytics_python_package",
    version="0.3.1",
    description="Useful tools for GA3 & GA4 and Google ADs generator",
    author = "Hanalytics",
    install_requires=["google-auth<=2.13.0", "google","pandas","google-analytics-data","openai","google-api-python-client<=2.10.2","oauth2client"],
    packages=["hanalytics/hanalytics_ga4","hanalytics/hanalytics_keywords_generator","hanalytics/hanalytics_ua"]
)