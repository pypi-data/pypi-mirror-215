"""
Setup script for my-python-calculator package.
"""

from setuptools import setup

setup(
    name='Haleh-python-calculator',
    version='2.0.0',
    author='Haleh Kafashinamdar',
    author_email='halehnamdar@gmail.com',
    description='A lightweight and easy-to-use calculator package for Python',
    url='https://github.com/TuringCollegeSubmissions/hkafas-DWWP.1',
    packages=['calculator'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
