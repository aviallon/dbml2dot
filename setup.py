from setuptools import setup

setup(
    name='dbml2dot',
    version='0.1.0',
    description='Converts DBML files to their graphviz representation in .dot format. It can also optionally do the additional conversion to an image format using graphviz.',
    url='https://github.com/aviallon/dbml2dot',
    author='Antoine Viallon (aviallon)',
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