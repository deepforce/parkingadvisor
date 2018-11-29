# Component Specification

### Software components

*1.*

**Name**: Display recommended parking area

**What it does:** Show all the recommended parking area near the location chosen by user.

**Input**: <list of float> (longitude, latitude); or <String> location name

​             (Pinpoint the specific location where the user wants to park)

**Output**: List of <Object> recommended parking blockface



*2*.

**Name:** Show flow analysis of parking lots

**What it does:** Display information of a specific parking lot

**Input:** <Object> Selected parking blockface

​	     (Pinpoint the specific parking lot where the user wants to park)	

**Output:** <list of string> A plot showing the vehicle flow of the parking lot.

​	      (A list of information about specific parking lot)

*3.*

**Name:** Display recommended parking area with charging station

**What it does:** Show all the recommended parking area with electric vehicle charging station near the place chosen by user

**Input:** float longitude, float latitude, and Boolean charging station(or not); 

​	     or String location name, and Boolean charging station(or not).

**Output**: List of float

​		(A list of float inidicating longitude and latitude of recommended parking area with charging station)

### Interactions to accomplish use cases

At very first, we need input about specific location that user wants to park. 

Then, the first use case works, which outputs a list of available parking areas.

Users then inputs specific parking lot that she/he prefers, the second use case applies under such circumstance, which outputs details about that parking lot.

Optionally, users are free to input extraordinary information, ie. whether she/he needs charging station. With a boolean input about whether the charging station is needed or not, third use case works, which shows recommended parking lots with charging station.

### Preliminary plan

1. Prototypes of interactive map product
2. EV changer stations data cleansing
3. Annual parking study data linked to GIS information datasets (Blockface/ Seattle Streets)
4. Build a model to rank the parking blockface within a certain range
5. Interactive interface based on arcGIS web
6. GIS layers display on interactive map using `arcGIS` package