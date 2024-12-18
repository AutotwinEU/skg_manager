from setuptools import find_packages, setup
import re

# read the contents of the README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")


VERSIONFILE=f"{this_directory}/version.md"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^# version ([\d]+.[\d]+.[\d]*)"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
    name='skg_manager',
    version=str(verstr),
    description='Pyhton library to build a generic skg manager api and some generic functions',
    author='A. Swevels, D.Fahland',
    python_requires='>=3.8',
    install_requires=['neo4j', 'numpy', 'pandas', 'promg', 'requests', 'flask-swagger-ui', 'flask'],
    license='GPL 3.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(
        where='src',
        include=['skg_manager*']),
    package_dir={"": "src"},
    package_data={'skg_manager': ['api/static/swagger.json']}
)
