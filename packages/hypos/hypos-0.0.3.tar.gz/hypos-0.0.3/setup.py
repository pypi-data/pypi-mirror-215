
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="hypos",
    version="0.0.3",
    author="prabdalip",
    author_email="anasterstudio@gmail.com",
    description="PrABpY",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PrABpY/ML-Hypothesis.git",
    license="MIT",
    install_requires=[
        'numpy'
    ],
    tests_require=[
        'coverage', 'wheel', 'pytest', 'requests_mock'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha"
    ]
)