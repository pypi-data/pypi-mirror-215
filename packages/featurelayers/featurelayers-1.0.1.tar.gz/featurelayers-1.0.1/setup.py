import setuptools
from setuptools import setup, find_packages

setup(
    name='featurelayers',
    version='1.0.1',
    description='FeatureLayers Package',
    author='khengyun',
    author_email='khaangnguyeen@email.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'tensorflow',
        'keras',
        'scipy',
    ],
    classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]

)
