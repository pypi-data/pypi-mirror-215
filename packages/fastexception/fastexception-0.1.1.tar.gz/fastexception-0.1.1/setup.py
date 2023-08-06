from setuptools import setup, find_packages

setup(
    name='fastexception',
    version='0.1.1',
    license='MIT',
    author='Mojtaba',
    author_email='mojtabapaso@gamil.com',
    packages=find_packages(),
    url='https://github.com/mojtabapaso/fastexception',
    keywords='FastAPI Tools Fast Exception',
    install_requires=[
        'starlette',
    ],

)
