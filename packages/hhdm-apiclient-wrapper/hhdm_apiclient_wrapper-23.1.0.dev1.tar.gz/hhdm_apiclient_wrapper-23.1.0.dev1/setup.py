from setuptools import find_packages, setup

setup(
    name='hhdm_apiclient_wrapper',
    packages=find_packages(include=['hhdm_apiclient_wrapper']),
    version='23.1.0.dev1',
    description='Wrapper for use of the HH Data Management Api Client',
    author='HH Development',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)