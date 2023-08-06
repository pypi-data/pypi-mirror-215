from setuptools import setup
import setuptools
from src.VersionUtil import VersionUtil


setup(
    name='REMLA23Team09LibProject',
    version=VersionUtil.get_version(),
    description='A version-aware library',
    author='Zhiyong Zhu',
    author_email='z13913982280@gmail.com',
    url='https://github.com/remla23-team09/lib',
    license='MIT',
    long_description="REMLA23Team09LibProject",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
)
