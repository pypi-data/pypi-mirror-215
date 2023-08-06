from setuptools import setup, find_packages

setup(
    name='fastexception',
    version='0.1.0',
    author='Mojtaba',
    author_email='mojtabapaso@gamil.com',
    description='fast exception for fastapi or starlette',
    packages=find_packages(),
    install_requires=[
        'starlette',
    ],

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
