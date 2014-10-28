"""
ps_calcs
======

The ps_calcs library helps run calculations for creating a product space as
well as other related calculations.

Resources
---------

* `Issue Tracker <https://github.com/alexandersimoes/ps_calcs/issues>`_
* `Source <https://github.com/alexandersimoes/ps_calcs>`_
* `About Product Space <http://en.wikipedia.org/wiki/The_Product_Space>`_

"""

from setuptools import setup
import os

setup(
    name='ps_calcs',
    version='1.0.0',
    url='https://github.com/alexandersimoes/ps_calcs',
    license='MIT',
    author='Alexander Simoes',
    author_email='simoes@mit.edu',
    description='Product Space calculations.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    packages=[
        'ps_calcs'
    ],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[x.strip() for x in
            open(os.path.join(os.path.dirname(__file__),
                'requirements.txt')).xreadlines()],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Data',
    ]
)
