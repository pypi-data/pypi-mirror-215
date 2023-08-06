from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Airvue-gn',
    version='0.0.2',
    author="AirvueTech",
    author_email="dev@airvue.news",
    description='Airvue-gn',
    long_description="Airvue-gn",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    url='https://github.com/AirvueTech/Airvue-gn',
)
