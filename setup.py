from setuptools import setup, find_packages

setup(name='age of triggers',
      version='0.0',
      description='Age of Empire 2 HD/DE python API',
      author='Nicolas Carrara',
      author_email='nicolas.carrara1u@gmail.com',
      url='https://github.com/ncarrara/age-of-triggers',
      package_data={'aot.*': ['templates/*.aoe2scenario']},
      include_package_data=True,
      packages=['aot',
                'aot.model',
                'aot.utilities',
                'aot.meta_triggers',
                'aot.examples'])
