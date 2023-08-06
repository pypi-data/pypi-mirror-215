from setuptools import setup, find_packages

setup(
    name='yb-hello',
    version='1.0.0',
    description='Your package description',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'urllib3==1.25.11',
    ],
)
