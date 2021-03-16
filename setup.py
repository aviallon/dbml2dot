from textwrap import dedent

from setuptools import setup

import dbml2dot

setup(
    name='dbml2dot',
    version=dbml2dot.__version__,
    description=dedent('''
    Converts DBML files to their graphviz representation in .dot format.
    It can also optionally do the additional conversion to an image format using graphviz.'''),
    url=dbml2dot.__url__,
    author=dbml2dot.__author__,
    author_email='antoine+pip@lesviallon.fr',
    license='GPL 3.0',
    packages=['dbml2dot'],
    install_requires=['pydbml~=0.3.4',
                      'pydot~=1.4.2',
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
