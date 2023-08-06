from setuptools import setup, find_packages

setup(
    name='trex_flare_detector',
    version='0.1.0',
    author='Shachar Israeli',
    description='A PMF Flare Detection Tool',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'pandas',
        'matplotlib',
    ],
)
