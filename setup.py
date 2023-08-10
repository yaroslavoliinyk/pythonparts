from setuptools import find_packages, setup
# for test commit

setup(
    name='pythonparts',
    packages=find_packages(),
    version='0.1.1',
    description='PythonParts library',
    author='Yaroslav Oliinyk',
    license='MIT',
    install_requires=['pytest==7.4.0',
                      'openpyxl==3.0.7'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
