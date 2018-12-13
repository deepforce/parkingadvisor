#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = "ParkingAdvisor",
    version = "0.1",
    author = 'Jiajie Guo | Zhicheng Ju | Yue Wang | Yuqi Zheng',
    author_email = "jguo16@uw.edu | zju2@uw.edu | yuew03@uw.edu | yuqi95@uw.edu",
    packages = find_packages(),
    package_data = {
        # If any package contains *.csv or *.json files, include them:
        '': ['*.csv', '*.json'],
    },
    description = 'Active map for finding parking lots in Seattle',
    license = 'MIT',
    long_description = '''
    ParkingAdvisor
    ==========================================================================
    ParkingAdvisor is a python-based package to provide an active map to
    drivers who is seeking for a parking position in Seattle.
    
    With the detailed information and our recommendation model, the
    comparision between each on-street parking spot is visualized on a color
    map for users. We currently have three ranking mode: Rate, Occiupancy, and
    Recommendation.

    To get started more information and instruction, please go to the repository
    README: https://github.com/deepforce/parkingadvisor/blob/master/README.md

    MIT License
    ==========================================================================
    Copyright (c) 2018

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions: 

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
    ''',
    url = 'https://github.com/deepforce/parkingadvisor',
    install_requires = ['folium', 'geopandas', 'pandas', 'numpy'],
    # metadata for upload to PyPI
    keywords = "active Seattle parking map "
    )