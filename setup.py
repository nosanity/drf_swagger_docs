from setuptools import setup, find_packages

setup(
    name='drf_swagger_docs',
    version='0.1',
    packages=find_packages(),
    description='Documentation generator for drf',
    url='http://example.com',
    author='author',
    install_requires=['drf-yasg==1.15.1', 'packaging']
)
