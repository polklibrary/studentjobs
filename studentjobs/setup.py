import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'chameleon==2.11',
	'pyramid==1.3.3',
    'pymysql==0.5',
	'mako==0.7.3',
    'SQLAlchemy==0.7.8',
    'transaction',
    'pyramid_tm==0.7',
    'pyramid_mailer==0.11',
    'repoze.sendmail==4.0',
    'zope.sqlalchemy',
    'waitress',
    'requests',
    ]

setup(name='studentjobs',
      version='0.0',
      description='studentjobs',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
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
      test_suite='studentjobs',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = studentjobs:main
      [console_scripts]
      initialize_ArchivesIndexes_db = studentjobs.scripts.initializedb:main
      """,
      )

