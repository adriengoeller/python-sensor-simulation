from setuptools import setup, find_packages

setup(
     name='sensorsim',
     version='0.0.1',
     author='Adrien Goeller',
     author_email='adrien.goeller.pro@gmail.com',
     packages=find_packages('./src/sensorsim'),
     url='http://pypi.python.org/pypi/PackageName/', 
     python_requires='>=3',
     license='LICENSE', 
     description='Function collection for specific pressure sensor simulation',
     long_description=open('README.md').read(),
    )