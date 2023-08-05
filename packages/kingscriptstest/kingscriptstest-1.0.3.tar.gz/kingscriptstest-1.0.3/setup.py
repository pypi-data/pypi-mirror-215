from setuptools import setup, find_packages

# reading long description from file
with open('kingscriptstest/Readme.md', 'r') as file:
    long_description = file.read()


# specify requirements of your package here
REQUIREMENTS = ['requests', 'pandas']

# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
]

# calling the setup function
setup(name='kingscriptstest',
      version='1.0.3',
      description='Test push of the King Scripts',
      long_description=long_description,
      url='https://github.com/kingoperating/v2',
      author='Michael Tanner',
      author_email='mtanner@kingoperating.com',
      license='MIT',
      packages_dir={'': 'kingscriptstest'},
      packages=find_packages(where='kingscriptstest'),
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      extras_require={"dev": ["twine>=3.2.0"]},
      keywords='maps location address'
      )
