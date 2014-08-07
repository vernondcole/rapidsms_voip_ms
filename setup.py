"""a Backend connecting RapidSMS with TextIt to receive SMS messages for a django project
"""
# CLASSIFIERS = """\   ##  TODO: fix these qualifiers, they are wrong
# Development Status :: 5 - Production/Stable
# Intended Audience :: Developers
# License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
# Operating System :: POSIX :: Linux
# Programming Language :: Python
# Programming Language :: Python :: 3
# Topic :: Software Development
# Topic :: Software Development :: Libraries :: Python Modules
# Topic :: Database
# """

MAINTAINER          = "eHealth Africa staff"
MAINTAINER_EMAIL    = "service@ehealthafrica.org"
DESCRIPTION         = 'a Backend connecting RapidSMS with TextIt to receive SMS messages for a django project'
URL                 = 'https://github.com/ehealthafrica/rapidsms-textit/'
##CLASSIFIERS         = filter(None, CLASSIFIERS.split('\n'))  ## TODO fix the qualifiers
PLATFORMS           = ["Linux"]


def setup_package():

    from distutils.core import setup

    setup(
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        url=URL,

        license='LICENSE.txt from caktus',
        ## classifiers=CLASSIFIERS,   ## TODO correct classifiers
        ## keywords='database ado odbc dbapi db-api Microsoft SQL',

        platforms=PLATFORMS,
        package_dir = {'rapidsms_textit':''},
        name='rapidsms-textit',
        version=__import__('textit').__version__,
        packages=['rapidsms_textit'],
        long_description=open('README.rst').read()
    )
    return

if __name__ == '__main__':
    setup_package()
