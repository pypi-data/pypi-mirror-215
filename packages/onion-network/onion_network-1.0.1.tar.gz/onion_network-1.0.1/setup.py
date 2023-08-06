from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    tests_require = f.readlines()
install_requires = [t.strip() for t in tests_require]

setup(
    name="onion_network",
    version="1.0.1",
    description="A module for generating and visualizing onion-structured networks!",
    long_description=long_description,
    author="Simon Popelier",
    author_email="simon.popelier@gmail.com",
    packages=["onion_network"],
    install_requires=install_requires,
    url='https://github.com/SimonPop/onion_network'
)
