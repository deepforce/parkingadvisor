# ParkingAdvisor
<img src="images/Logo.png" style="zoom:50%" />

![](https://img.shields.io/github/license/mashape/apistatus.svg)

Hello there! Here is **ParkingAdvisor**, a webpage-based tool to provide the best on-street parking spot for you. Here is our web app [demo](http://parkingadvisor.westus2.cloudapp.azure.com/).

Let me introduce myself.
## Background
A [study](https://www.seattlemag.com/article/how-find-parking-seattle) shows Seattle is the sixth-most-expensive city in the nation in which to park a car, according to a 2011 Colliers International survey. Finding a parking spot in Seattle downtown is a big issue for peopel due to the limited parking lots especially in peak-hour. 

In order to provide a beeter experience for people to park their car, we develop a tool to provide a list of recommendation for our users to park theie car, just based on the user's location and their preference. In addition, our tool could show every public charging station around our user's target parking area. 

**ParkingAdvisor**, provide your parking lot and save both money and time!

## Data
* [Annual Parking Study Data](https://data.seattle.gov/Transportation/Annual-Parking-Study-Data/7jzm-ucez)
* [Seattle Streets](http://data-seattlecitygis.opendata.arcgis.com/datasets/seattle-streets)
* [Blockface](https://data-seattlecitygis.opendata.arcgis.com/datasets/blockface)
* [Electric Vehicle Charging Station Locations](https://afdc.energy.gov/fuels/electricity_locations.html#/find/nearest?fuel=ELEC)

## Documentation

To make users unsterstand the functions we used in ParkingAdvisor project easierly, we documented every modules and functions within this project.

To document `parking_advisor` we use the [sphinx documentation system](http://sphinx-doc.org/). You can follow the instructions on the sphinx website, and the example [here](http://matplotlib.org/sampledoc/) to set up the system, but we have also already initialized and commited a skeleton documentation system in the `docs/AutoDoc` directory, that you can build upon.

For example, if you want to generate the HTML rendering of the documentation (web pages that you can upload to a website to explain the software), you will type:

```
make html
```

This will generate a set of static webpages in the `doc/AutoDoc/Documentation/build/html`, which you can then upload to a website of your choice.

## Software dependencies and license information

#### Programming language:
* Python, version 3.6 and above

* JavaScript

* HTML

#### Python packages needed:
* folium

* geopandas

* pandas

* NumPy

#### Tools
* Bootstrap

#### License Information:
The [MIT License](https://en.wikipedia.org/wiki/MIT_License) is a permissive free software license originating at the Massachusetts Institute of Technology (MIT). As a permissive license, it puts only very limited restriction on reuse and has therefore an excellent license compatibility. [This link](https://opensource.org/licenses/MIT) grant the permission of MIT License.

## Directory Structure
#### ParkingAdvisor (master)
```bash
.
├── Backend
│   └── ParkingAdvisor
│       ├── Datasets
│       ├── ParkingAdvisor
│       ├── db.sqlite3
│       ├── home_page
│       ├── launch_page
│       ├── manage.py
│       ├── static
│       └── templates
├── LICENSE
├── README.md
├── docs
│   ├── Component\ Specification.md
│   ├── Functional\ Specification.md
│   └── presentation.pptx
├── images
│   ├── Logo
│   │   ├── 0.5x
│   │   ├── 1x
│   │   ├── 2x
│   │   └── SVG
│   └── Logo.png
├── parkingadvisor
│   ├── __init__.py
│   ├── data
│   │   ├── Clean_Annual_Parking_Strudy.ipynb
│   │   ├── Clean_Blockface.ipynb
│   │   ├── Clean_EV_Charger.ipynb
│   │   ├── EV\ Charger.json
│   │   ├── Occupancy_per_hour.csv
│   │   ├── Rate_limit.csv
│   │   ├── Streets_gis.json
│   │   ├── Subset_Streets_GIS.ipynb
│   │   ├── clean_up
│   │   ├── flow_all_streets.csv
│   │   └── raw_data
│   ├── filter.py
│   ├── plot_map.py
│   ├── test.py
│   └── visual.py
└── website
    ├── css
    │   ├── L.Control.Sidebar.css
    │   └── bootstrap.min.css
    ├── homepage.html
    ├── images
    │   ├── _DS_Store
    │   └── homepage
    ├── js
    │   ├── L.Control.Sidebar.js
    │   ├── bootstrap.min.js
    │   ├── jquery.cookie.js
    │   └── jquery.min.js
    └── launch_page.html
```
## Installation Tutorial

#### To install FirstStop perform following steps:

* clone the repo: 

  `git clone https://github.com/deepforce/parkingadvisor`

* run the setup.py file: 

  `python setup.py install`

* open homepage.html and click ParkingAdvisor to access the launch page 

* input the destination of your parking area and research

* the information will be provided in the pop window
