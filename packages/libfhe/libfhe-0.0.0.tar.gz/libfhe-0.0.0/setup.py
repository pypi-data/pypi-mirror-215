import os
from setuptools import find_packages, Extension, setup
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "bgv",
        ["python/bgv.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
        libraries=['gmp', 'gomp', 'fhe']
    )
]

with open('README') as f:
    LONG_DESCRIPTION = f.read()

with open('python/requirements.txt', 'r') as fh:
    REQ = fh.readlines()

setup(
    name='libfhe',
    version='0.0.0',
    ext_modules=cythonize(ext_modules),
    author='tazzaoui',
    author_email='taha@azzaoui.org',
    description='Python wrapper around libfhe',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    setup_requires=['wheel'],
    include_package_data=True,
    install_requires=REQ,
    url="https://git.azzaoui.org/libfhe.git",
    packages=find_packages(),
    keywords = ['cryptography', 'fhe', 'Homomorphic Encryption'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Intended Audience :: Developers',
		'Topic :: Security :: Cryptography',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],
    python_requires='>=3.6'
)
