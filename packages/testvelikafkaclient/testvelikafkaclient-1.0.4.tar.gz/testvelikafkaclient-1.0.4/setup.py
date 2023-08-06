from setuptools import setup, find_packages
from testvelikafkaclient import __version__

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name='testvelikafkaclient',
    version=__version__,
    description='veli kafka client <3 (demo)',
    author='Konstantine',
    author_email='kdvalishvili@veli.store',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages()
)
