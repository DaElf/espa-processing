from setuptools import find_packages
from setuptools import setup

def version():
    with open('version.txt') as f:
        return f.read()

def readme():
    with open('README.md') as f:
        return f.read()


setup(name='espa-processing',
      version=version(),
      description='The ESPA Product Fullfillment system',
      long_description=readme(),
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: Public Domain',
        'Programming Language :: Python :: 2.7',
      ],
      keywords='usgs eros lsrd espa',
      url='http://github.com/usgs-eros/espa-processing',
      author='USGS EROS ESPA',
      author_email='',
      license='Unlicense',
      packages=find_packages(),
      install_requires=[
          'falcon',
          'PyYAML',
          'requests',
          'uWSGI',
          'marshmallow>=3.0.0b8',
          'addict',
          'python-dateutil',
          'espa-python-library==1.1.0',
      ],
      dependency_links=[
          'git+https://github.com/USGS-EROS/espa-python-library.git@v1.1.0#egg=espa-python-library-1.1.0',
      ],
      # List additional groups of dependencies here (e.g. development
      # dependencies). You can install these using the following syntax,
      # for example:
      # $ pip install -e .[test]
      extras_require={
          'test': [
              'pylint',
              'pytest',
              'pytest-cov',
              'vcrpy',
              'hypothesis',
                  ],
          'doc': [
              'sphinx',
              'sphinx-autobuild',
              'sphinx_rtd_theme'],
          'dev': [],
      },
      entry_points={
          'console_scripts': [
              'espa-cli = processing.cli:main'
          ],
      },
      include_package_data=True,
      zip_safe=False
)
