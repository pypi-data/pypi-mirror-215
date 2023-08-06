from setuptools import setup, find_packages
import os


VERSION = '1.0.0'
DESCRIPTION = 'Log linear model regression and dealing with zeros'
LONG_DESCRIPTION = "The Zero-Inflated Log Linear Regression package provides a set of functions and utilities to handle zero-inflated cases in log linear regression models. It offers methods for estimating model parameters, calculating predicted values, and handling clustered data. This package is particularly useful when dealing with datasets where the dependent variable has excess zeros, allowing for more accurate and robust analysis of log linear regression models. It leverages the power of numpy, statsmodels, and pandas libraries to provide efficient and reliable computations for zero-inflated log linear regression analysis."

# Setting up
setup(
    name="iolsmp",
    version=VERSION,
    author="Oussama Elghodhben, Rami Znazen",
    author_email="<oussama.elghodhben@telecom-paris.fr>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'statsmodels'],
    keywords=["log linear", "regression"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)