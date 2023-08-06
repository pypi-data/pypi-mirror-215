from setuptools import setup, find_packages


setup(
    name='dadajokes',
    version='0.1.0',
    description='A Python package for getting random dad jokes',
    author='Innocent Kithinji',
    author_email='innocent@ikithinji.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6',
)