import os
from setuptools import find_packages, setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='time-to-live',
    version='1.0.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    license='BSD',  # example license
    description='',
    long_description='',
    url='',
    author_email='pkucmus@gmail.com',
    extras_require={
        'develop': [
            'readline',
            'pdbpp',
            'ipdb',
            'ipython',
            'mock',
            'coverage',
        ]
    },
    install_requires=[
        'requests',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'ttl = ttl.main:cli',
        ],
    },
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.6.3',
    ],
)
