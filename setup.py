"""
Growth
======

The Growth library helps run calculations for creating a product space as
well as other related calculations.

Resources
---------

* `Issue Tracker <https://github.com/alexandersimoes/growth/issues>`_
* `Source <https://github.com/alexandersimoes/growth>`_
* `About Product Space <http://en.wikipedia.org/wiki/The_Product_Space>`_

"""

from setuptools import setup

setup(
    name='Growth',
    version='1.0.0',
    url='https://github.com/alexandersimoes/growth',
    license='MIT',
    author='Alexander Simoes',
    author_email='simoes@mit.edu',
    description='Product Space calculations.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    packages=[
        'growth'
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