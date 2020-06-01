# Copyright (C) 2020 Guillaume VINET
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import setuptools

import pynfcreader

with open("README.md", "r") as fh:
    long_description = fh.read()

name = 'pyNFCReader'
version = str(pynfcreader.__version__)
release = str(version)

setuptools.setup(
    name=name,
    version=pynfcreader.__version__,
    author="Guillaume VINET",
    description="NFC reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gvinet/pynfcreader",
    packages=setuptools.find_packages(),
    install_requires=['pyHydrabus'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
