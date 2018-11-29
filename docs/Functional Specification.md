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

1. Displays recommended parking area.

   **User**: Put a pinpoint on the map or input the location name.

   **System**: Displays all the recommended parking area near the place chose by user.

2. Show flow analysis of parking lots.

   **User**: Select one of the parking lot and choose to show the flow analysis of this parking lot.

   **System**: Displays the flow analysis of the parking lot.

3. Displays recommended parking area including electric vehicle charging station.

   **User**: Select the "EVC" checkbox and put a pinpoint on the map or input the location name.

   **System**: Displays all the recommended parking area near the place chose by user.



