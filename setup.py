from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
    name='rapidsms-textit',
    version=__import__('rtextit').__version__,
    author='V.Cole @ eHealthAfrica',
    author_email='vernon.cole@ehealthafrica.org',
    packages=find_packages(),
    include_package_data=True,
    exclude_package_data={
        '': ['*.sql', '*.pyc'],
    },
    url='https://github.com/ehealthafrica/rapidsms-textit/',
    license='LICENSE.txt',
    description='RapidSMS TextIt Threadless Backend',
    long_description=open('README.rst').read(),
    install_requires=(
        'rapidsms>=0.10.0',
        'requests>=1.2.0',
        'django>=1.4',
    ),
    test_suite="runtests.runtests",
    tests_require=(
        'mock',
    )
)
