from setuptools import setup, find_packages
from the_useless_cli.constants import VERSION

setup(
    name='the_useless_cli',
    version=VERSION,
    packages=find_packages(),
    author='ItsQuadrus',
    author_email='quadrus@gaboule.com',
    description='A pretty useless CLI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    package_dir={'the_useless_cli': 'the_useless_cli'},
    install_requires=[
        'typer',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'useless = the_useless_cli.__main__:app',
        ],
    },
)