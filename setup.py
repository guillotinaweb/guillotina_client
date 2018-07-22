# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


requirements = open('requirements.txt').read()
test_requirements = open('test_requirements.txt').read()
readme = open('README.rst').read() + '\n'
version = open('VERSION').read().strip()

setup(
    name='guillotinaclient',
    version=version,
    description='Guillotina python client',
    long_description=readme,
    author='Nil & Ferran',
    author_email='llamas.arroniz@gmail.com',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    url='https://github.com/lferran/guillotinaclient',
    license='BSD',
    setup_requires=[
        'pytest-runner'
    ],
    zip_safe=True,
    include_package_data=True,
    package_data={'': ['*.txt', '*.rst']},
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'test': [
            test_requirements
        ]
    },
)
