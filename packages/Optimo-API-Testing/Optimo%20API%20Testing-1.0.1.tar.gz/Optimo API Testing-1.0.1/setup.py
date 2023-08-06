from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Optimo API Testing',
    version='1.0.1',
    author='Bacho Labadze',
    author_email='bachukilabadze@gmail.com',
    description='Package for testing optimo API',
    packages=['Optimo','Optimo_Instance_Manager'],
    install_requires=requirements
)