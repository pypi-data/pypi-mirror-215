from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing_dp",
    version="0.0.1",
    author="Danillo Souza Pereira",
    description="Pacote para processar imagens usando Skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DanilloSouza03/Pacote-de-processar-imagens",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5',
)