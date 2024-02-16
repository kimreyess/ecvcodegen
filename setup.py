from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'SERFF generator prototype'
LONG_DESCRIPTION = 'SERFF generator prototype'

# Setting up
setup(
        name="ecv-serff-gen", 
        version=VERSION,
        author="ECV Peeps",
        author_email="ecv_devph@ecloudvalley.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
                "pyyaml",
                "typing_extensions"
            ], # add any additional packages
        py_modules= ['main'],
        keywords=[ 'python', 'serff', 'ecv-code-generator'],
        classifiers= [
            "Development Status :: Alpha",
            "Intended Audience :: ECV Devs",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ],
        entry_points={
            'console_scripts': [
                'serff = main:run_parser'
            ]
        }
)