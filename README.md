# HousingAnalysis
Housing proximity analysis visualizer in Bergen, Norway for the regular pedestrian.

## Description
The everyday pedestrian needs 2 things within walking distance (1 km) of their house i.e. food and public transport. This application collects publicly available information regarding housing, grocery stores and transportaion relevant in Bergen, Norway. The data is then stored in a database and retrieved to be plotted on a map and displayed. The properties available for sale that have either a grocery store or a transport available within 1 km (walkable distance) radius are shown on the map.

Available to view at : [HousingAnalysis](https://ipsitamishra16893.github.io/BergenHAV/index.html)

## Database
The database in use is Sqlite3. Schema for it is mentioned below :
```
sqlite> .schema store_info
CREATE TABLE store_info (  store_name text, street_address text, pincode text, city text, latitude real, longitude real);

sqlite> .schema stop_info
CREATE TABLE stop_info (  stop_id text, stop_name text, service1 text, service2 text, city text, latitude real, longitude real);

sqlite> .schema property_info
CREATE TABLE property_info (  address text, description text,  type text, link text, owner_type text, city text, latitude real, longitude real, new_prop text);
```

## Setting Up

In order to run the application, see below :

1. Install python 3 along with pip
2. Run the following command : ``` pip install requirements.txt```
3. Run the following command : ``` python3 start.py```
4. Wait till the program has finished running and open the newly generated file called ``` map.html ``` to view the analysed information
