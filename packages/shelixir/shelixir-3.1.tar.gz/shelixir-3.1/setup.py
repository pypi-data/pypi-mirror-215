from setuptools import setup, find_packages

with open('README') as f:
    long_description = ''.join(f.readlines())

setup(
    name='shelixir',
    version='3.1',
    description="Experimental phasing with SHELX C/D/E",
    long_description=long_description,
    author="Petr Kolenko",
    author_email='kolenpe1@cvut.cz',
    url='https://github.com/kolenpe1/shelixir',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
    ],
    entry_points={
        'console_scripts': [
            'shelixir = shelixir.source:main',
        ],
    },
    zip_safe=False,
)
