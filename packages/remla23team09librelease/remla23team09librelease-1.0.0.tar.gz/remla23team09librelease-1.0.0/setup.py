from setuptools import setup
import setuptools
from remla23team09librelease.VersionUtil import VersionUtil


setup(
    name='remla23team09librelease',
    version=VersionUtil.get_version(),
    description='A version-aware library',
    author='Zhiyong Zhu',
    author_email='z13913982280@gmail.com',
    url='https://github.com/remla23-team09/lib',
    license='MIT',
    long_description="package for remla",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
)
