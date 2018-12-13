# Functional Specification

### Background

Parking is a main issue in our daily life. People often spend a lot of time parking their car because they can't find a suitable place for them, especially during the peak hours.

### User profile

Almost everyone. They need to know how to read virtual maps. Follow the map to find the best parking location.

### Data sources

* **Annual Parking Study Data**
  Manual parking study details from citywide paid parking study, presented by blockface and date/hour of study. Most data is from spring of each year, with some data sets including summer studies.
* **Seattle Streets** 
  Streets data includes: Arterial Classification, Street Names, Block Number, Direction, One-way, Surface Width, Surface Type, Pavement Condition, Speed Limit, Percent Slope.
* **Blockface**
  Displays blockfaces for all segments of the street network. Identifies the elements of the block, such as peak hour restrictions, length of the block, parking categories, and restricted parking zones.
* **Electric Vehicle Charging Station Locations**
  Displays electric vehicle charging stations in the United States.
  It includes Fuel Type Code, Station Name, Location, Phone number, Latitude and Longitude.

### Use cases

1. Displays parking blockfaces under different modes.

   **User**: input the destination name, then choose different ranking modes.

   **System**: Displays all available parking area near the place chosen by user.

2. Show details of a specifc parking lot.

   **User**: Select one of the parking lot.

   **System**: Displays the detailed information of the parking lot.

3. Displays electric vehicle charging station.

   **User**: After receving the blockface map, use can select the "EVC" checkbox to show the charging station.

   **System**: Displays all charging stations on the blockface map

4. Show details of a specific charging station.

   **User**: Select one of the charging station.

   **System**: Displays the detailed information of the charging station.

