from setuptools import setup, find_packages
from os.path import abspath, dirname, join


path = abspath(dirname(__file__))
with open(join(path, "README.rst")) as f:
    readme = f.read()

setup(
    name="batch-mailchimp",
    description="A python client for MailChimp Marketing API, with batch support",
    url="https://github.com/FullFact/python-batchmailchimp",
    author="Andy Lulham",
    author_email="andy.lulham@fullfact.org",
    version="1.1.0",
    packages=find_packages(),
    license="MIT",
    keywords="mailchimp marketing api client wrapper",
    long_description=readme,
    install_requires=["mailchimp-marketing>=3.0.80"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
