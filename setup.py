#from distutils.core import setup
from setuptools import setup, find_packages

# http://guide.python-distribute.org/quickstart.html
# python setup.py sdist
# python setup.py register
# python setup.py sdist upload
# pip install python-html-objects
# pip install python-html-objects --upgrade --no-deps
# Manual upload to PypI
# http://pypi.python.org/pypi/python-html-objects
# Go to 'edit' link
# Update version and save
# Go to 'files' link and upload the file


tests_require = [
    'nose==1.1.2',
    'django-nose==0.1.3',
]

install_requires = [
]

setup(name='python-html-objects',
      url='https://github.com/paulocheque/python-html-objects',
      author="paulocheque",
      author_email='paulocheque@gmail.com',
      keywords='python html objects',
      description='Python library that contains objects that represents HTML tags.',
      license='MIT',
      classifiers=[
          'Operating System :: OS Independent',
          'Topic :: Software Development'
      ],

      version='0.1.0',
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='runtests.runtests',
      extras_require={'test': tests_require},

      packages=find_packages(),
)
