import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


long_description = read('README.md') if os.path.isfile("README.md") else ""

setup(
    name='band-etl',
    version='0.0.8',
    author='Evgeny Medvedev',
    author_email='evge.medvedev@gmail.com',
    description='Tools for exporting Band Protocol blockchain data to JSON',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/blockchain-etl/band-etl',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='Band Protocol',
    python_requires='>=3.6.0,<3.8.0',
    install_requires=[
        'blockchain-etl-common==1.3.0',
        'bech32==1.2.0',
        'ecdsa==0.16.0',
        'bip32==0.0.8',
        'mnemonic==0.19',
        'requests==2.24.0',
        'python-dateutil==2.8.1',
        'six==1.15.0',
        'click==7.0',
        'pyband==0.0.8',
    ],
    extras_require={
        'streaming': [
            'timeout-decorator==0.4.1',
            'google-cloud-pubsub==0.39.1',
        ],
        'dev': [
            'pytest~=4.3.0',
            'pytest-timeout~=1.3.3'
        ],
    },
    entry_points={
        'console_scripts': [
            'bandetl=bandetl.cli:cli',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/blockchain-etl/band-etl/issues',
        'Source': 'https://github.com/blockchain-etl/band-etl',
    },
)
