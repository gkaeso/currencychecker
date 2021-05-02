import setuptools


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name='currencychecker',
    version='1.0.0',
    author='Guillaume Marcel',
    description='A currency command-line program to check various things',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gkaeso/currencychecker",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'beautifulsoup4', 'lxml'],
    python_requires='>=3.9',
)