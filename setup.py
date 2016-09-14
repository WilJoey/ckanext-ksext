from setuptools import setup, find_packages
import sys, os

version = '0.2'

setup(
    name='ckanext-ksext',
    version=version,
    description="kaohsiung open data ckan extension",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='kaohsiung',
    author_email='kaohsiung@gmail.com',
    url='',
    license='mit',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.ksext'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'losser'
    ],
    entry_points='''
        [ckan.plugins]
        ksext=ckanext.ksext.plugin:KsextPlugin
        [babel.extractors]
        ckan = ckan.lib.extract:extract_ckan
        [ckan.celery_task]
        tasks=ckanext.ksext.celery_import:task_imports
        [paste.paster_command]
        ksext=ckanext.ksext.commands:KsextCommand
    ''',

    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    }
)
