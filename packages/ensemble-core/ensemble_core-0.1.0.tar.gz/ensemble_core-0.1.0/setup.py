from setuptools import setup, find_packages

setup(
    name='ensemble_core',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[line.strip() for line in open('requirements.txt')],
    author='Chenwei Xu',
    author_email='q1062327596@gmail.com',
    description='Ensemble-AI Company, generator & transformer',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    url='https://github.com/SirAlex900/ensemble_core',
)
