# encoding: utf-8
from setuptools import setup, find_packages
from eureka import __version__ as version

setup(
    name = 'cloud-data-generator',
    version = version,
    description = '',
    author = u'Pablo Calvo',
    author_email = 'pablo.calvo.velilla@everis.com',
    zip_safe=False,
    include_package_data = True,
    packages = find_packages(exclude=[]),
    install_requires=[
        'django-iban-field',
        'django',
        'fake-factory',
        'pycountry'
    ],
)





