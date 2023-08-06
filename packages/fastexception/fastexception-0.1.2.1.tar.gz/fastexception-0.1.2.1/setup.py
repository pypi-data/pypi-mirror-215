from setuptools import setup, find_packages
from pathlib import Path
# this_directory = Path(__file__)
long_description = "README.md"
setup(
    name='fastexception',
    version='0.1.2.1',
    license='MIT',
    author='Mojtaba',
    author_email='mojtabapaso@gamil.com',
    packages=find_packages(),
    url='https://github.com/mojtabapaso/fastexception',
    keywords='FastAPI Tools Fast Exception',
    install_requires=[
        'starlette',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'

)
