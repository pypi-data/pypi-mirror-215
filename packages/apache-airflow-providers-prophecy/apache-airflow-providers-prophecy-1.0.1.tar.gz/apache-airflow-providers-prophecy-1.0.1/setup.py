# setup.py

from setuptools import setup, find_packages

setup(
    name='apache-airflow-providers-prophecy',
    version='1.0.1',
    description='Your provider package for Apache Airflow',
    packages=find_packages(),
    install_requires=[
        'apache-airflow>=2.2.0'
        # Add any additional dependencies required by your provider
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "apache_airflow_provider": [
            "provider_info=prophecy_provider.__init__:get_provider_info"
        ]
    },
    python_requires=">=3.6",
)
