from setuptools import setup, find_packages
import codecs
import os
# 
here = os.path.abspath(os.path.dirname(__file__))
# 
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()\

from pathlib import Path
this_directory = Path(__file__).parent
#long_description = (this_directory / "README.md").read_text()

VERSION = '''0.10'''
DESCRIPTION = '''converts large CSV files into smaller, Pandas-compatible Parquet files'''

# Setting up
setup(
    name="dfcsv2parquet",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/dfcsv2parquet',
    author="Johannes Fischer",
    author_email="aulasparticularesdealemaosp@gmail.com",
    description=DESCRIPTION,
long_description = long_description,
long_description_content_type="text/markdown",
    #packages=['a_pandas_ex_less_memory_more_speed', 'hackyargparser', 'pandas', 'pyarrow'],
    keywords=['csv', 'parquet', 'pandas', 'DataFrame'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['a_pandas_ex_less_memory_more_speed', 'hackyargparser', 'pandas', 'pyarrow'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*