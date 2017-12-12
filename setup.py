from setuptools import setup, find_packages


def readme():
    with open("README.md", 'r') as f:
        return f.read()


setup(
    name="relativizer",
    description="A tool for comparing the mergability of relative roots",
    version="0.0.1",
    long_description=readme(),
    author="Brian Balsamo",
    author_email="brian@brianbalsamo.com",
    packages=find_packages(
        exclude=[
        ]
    ),
    include_package_data=True,
    url='https://github.com/bnbalsamo/relativizer',
    install_requires=[
    ],
    tests_require=[
        'pytest'
    ],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'relativize = relativizer:main'
        ]
    }
)
