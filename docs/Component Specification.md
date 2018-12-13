# Component Specification

### Software components

*1.*

**Name**: Display all the parking lots nearby the specific location

**What it does:** 

rank parking lots by different modes

*Mode 1 (Rate) :* rank the blockface by rate from lower to higher, with colorbar from lighter to darker.

*Mode 2 (Occupancy):* rank the blockface by parking lots occupancy in corresponding street, from lower occupancy to higher, with colorbar from lighter to darker.

*Mode 3 (Recommendation):* rank the blockface by recommendation values, from higher to lower, with colorbar from green to red.

**Input**:  <String> destination name

**Output**: List of <Object> parking blockface displayed on map, with different color shows various corresponding mode values



*2*.

**Name:** Show details of a specific parking lots

**What it does:** 

Display information of a specific parking lot, such as parking time restriction, rates for different time intervals, and a figure containing busy levels

**Input:** <Object> Selected parking blockface

**Output:** <list of string> A list of information about specific parking lot



*3.*

**Name:** Display EV charging stations

**What it does:** 

Add a layer on the map with EV charging stations to the result of first component under every mode.

**Input:** <boolean> Turn on the EV_charger option or not

**Output**: List of <Object> charging stations displayed on map from first component.



*4*.

**Name:** Show details of a specific EV charging station

**What it does:** 

Display information of a specific charging station, such as detailed address, station phone number, connection types, and charging type.

**Input:** <Object> Selected charging station

**Output:** <list of string> A list of information about specific charging station



### Interactions to accomplish use cases

At very first, we need input about specific location that user wants to park. 

Then, the first use case works, which outputs a list of available parking areas, displayed on the map.

Users then inputs specific parking lot that she/he prefers, the second use case applies under such circumstance, which outputs details about that parking lot.

Optionally, users are free to input extraordinary information, ie. whether she/he needs charging station. With a boolean input about whether the charging station is needed or not, third use case works, which maks all the charging stations on the previous map, also, users can also check the details of specific charging station info through fourth user case by clicking one specific charging station.

### Preliminary plan

1. Prototypes of interactive map product
2. EV changer stations data cleansing
3. Annual parking study data linked to GIS information datasets (Blockface/ Seattle Streets)
4. Build a model to rank the parking blockface within a certain range
5. Interactive interface based on web
6. GIS layers display on interactive map using `folium` package