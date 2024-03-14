from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'ECV code generator prototype'
LONG_DESCRIPTION = 'ECV code generator prototype'


# Setting up
setup(
        name="ecv-codegen", 
        version=VERSION,
        author="ECV Peeps",
        author_email="reyeskimberly018@gmail.com",
        # author_email="ecv_devph@ecloudvalley.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
                "typing_extensions"
            ], # add any additional packages
        py_modules= ['main'],
        keywords=[ 'python', 'ecv-codegen', 'ecv-code-generator'],
        classifiers= [
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers', 
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ],
        entry_points={
            'console_scripts': [
                'ecv-codegen = main:run_parser'
            ]
        },
        url="https://github.com/kimreyess/ecvcodegen",
)