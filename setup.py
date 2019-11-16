from setuptools import setup, find_packages

setup(name='age of triggers',
      version='0.0',
      description='Age of Empire 2 HD/DE python API',
      author='Nicolas Carrara',
      author_email='nicolas.carrara1u@gmail.com',
      url='https://github.com/ncarrara/age-of-triggers',
      package_data={'aot.api': ['templates/*.aoe2scenario']},
      include_package_data=True,
      packages=['aot',
                'aot.model',
                'aot.api',
                'aot.utilities',
                'aot.controller',
                'aot.enums',
                'aot.groups'])
