import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid==1.5.7',
    'pyramid_debugtoolbar==2.4',
    'pyramid_tm==0.12',
    'SQLAlchemy==1.0.8',
    'transaction==1.4.4',
    'zope.sqlalchemy==0.7.6',
    'waitress==0.8.9',
    'psycopg2==2.6.1',
    'pyramid_jinja2==2.5',
    'WTForms==2.0.2',
    'paginate_sqlalchemy==0.2.0',
    'paginate',
    'WebTest',
    'pyramid-multiauth==0.5.0',
    'ldap3==0.9.9.1',
    'uwsgi==2.0.11'
    ]

setup(name='arhea',
      version='1.0.0',
      description='arhea',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='arhea',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = arhea:main
      [console_scripts]
      initialize_arhea_db = arhea.scripts.initializedb:main
      """,
      )
