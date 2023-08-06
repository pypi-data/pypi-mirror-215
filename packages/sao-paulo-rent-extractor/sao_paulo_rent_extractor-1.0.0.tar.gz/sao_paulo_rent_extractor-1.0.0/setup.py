from setuptools import setup, find_packages

setup(
    name='sao_paulo_rent_extractor',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4==4.12.2',
        'requests==2.31.0',
        'pandas==2.0.2',
        'logging==0.4.9.6'
    ],
)