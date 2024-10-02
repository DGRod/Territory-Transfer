# Territory-Transfer

A program to integrate geo-spatial (GIS) data from the local area into our congregation's existing territory records before converting them into a convenient data format for export.

## Features

- Support for batch upload of territory records
- Excel files converted automatically to CSV's
- Accurate location data for each address obtained from FEMA
- Efficient data management using HeapSort and BinarySearch
- Convenient output for import into Hourglass


## Installation

1. Latest release available on [GitHub](https://github.com/DGRod/Territory-Transfer)
2. Make sure that Pandas is installed in your local environment:
`pip install pandas`


## Usage

1. Import Excel territory file(s) into 'input' folder
2. Files will be automatically converted to CSV's
3. Relevant data will be integrated into each address
4. The modified addresses will be returned as an Hourglass-compatible CSV
5. A list of addresses that caused errors will be returned as a .txt file

## Data
GIS data sourced from [FEMA](https://gis-fema.hub.arcgis.com/pages/usa-structures)