from setuptools import find_packages, setup

setup(
    name='pythonparts',
    packages=find_packages(),
    version='0.1.0',
    description='PythonParts library',
    author='Yaroslav Oliinyk',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)