from setuptools import setup, find_packages

setup(
    name='jsonrequest',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pydantic',
    ],
    author='Justin Wong',
    description='Lightweight wrapper to make http(s) requests. POST, PATCH, and DELETE requests only support json content.',
)
