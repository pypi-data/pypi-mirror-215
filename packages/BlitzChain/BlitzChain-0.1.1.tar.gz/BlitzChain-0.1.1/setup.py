from setuptools import setup, find_packages

from pathlib import Path


# Read the contents of the README.md file
# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()
# long_description = Path("README.md").read_text()


setup(
    name='BlitzChain',
    version='0.1.1',
    url='https://github.com/mr-gpt/blitzchain',
    author='Twilix',
    author_email='jacky@twilix.io',
    description='BlitzChain',
    packages=find_packages(),    
    install_requires=['requests'],
    # long_description=long_description,
)
