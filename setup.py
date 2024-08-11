from setuptools import setup, find_packages

import pyawsopstoolkit_advsearch

setup(
    name=pyawsopstoolkit_advsearch.__name__,
    version=pyawsopstoolkit_advsearch.__version__,
    packages=find_packages(),
    url='https://github.com/coldsofttech/pyawsopstoolkit-advsearch.git',
    license='MIT',
    author='coldsofttech',
    description=pyawsopstoolkit_advsearch.__description__,
    requires_python=">=3.10",
    install_requires=[
        "pyawsopstoolkit==0.1.19",
        "pyawsopstoolkit_models==0.1.1",
        "botocore==1.34.158"
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=[
        "aws", "toolkit", "operations", "tools", "development", "python", "search", "utilities",
        "amazon-web-services", "advance-search", "search-functionality"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ]
)
