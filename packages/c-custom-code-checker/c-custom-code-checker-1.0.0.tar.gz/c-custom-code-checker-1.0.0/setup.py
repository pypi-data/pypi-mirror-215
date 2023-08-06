from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='c-custom-code-checker',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'c-validator= c_custom_code_checker:main',
        ],
    },
    install_requires=requirements,
)