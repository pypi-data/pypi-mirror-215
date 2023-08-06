from setuptools import setup, find_packages

setup(
    name='mycoinlib',
    version='1.4',
    packages=find_packages(),
    install_requires=[
        'bitcoinlib',
        'blockcypher',
        'requests',
        'eth_account',
        'eth-keys',

    ]
)
