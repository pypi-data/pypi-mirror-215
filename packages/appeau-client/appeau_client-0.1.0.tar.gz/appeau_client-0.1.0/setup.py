from setuptools import setup, find_packages
# read the contents of your README file
from pathlib import Path
import appeau_client
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Voir https://blog.engineering.publicissapient.fr/2020/06/04/packaging-python-setup-py-et-setuptools/
setup(name="appeau_client",
version=appeau_client.__version__,
description="A client for http://appeau.api.vignevin-epicure.com API",
author="Guilhem Heinrich",
author_email="guilhem.heinrich@id2l.fr",
packages=["appeau_client"],
# package_dir={'':'src'},
# packages=find_packages('src'),
install_requires=["requests"],
# format=["tar.gz", "zip"],
# extras_require={
# "dev": ["requests-mock"],
# },
# options={"sdist": {
#     "formats": ['zip', 'tar.gz']
# }},
license="Apache 2.0",
long_description=long_description)