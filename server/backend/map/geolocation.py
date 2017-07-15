import googlemaps

import pandas as pd


def geocode(gmaps,location):
    # Geocoding an address
    geocode_result = gmaps.geocode(location)

    location = geocode_result[0]["geometry"]["location"]
    return location


def execute():

    # read csv
    entities_df = pd.read_csv("../../files/entities.csv")

    # for testing reasons just use 50 locations
    #later on this will be 50 locations per second
    entities_df = entities_df.head(50)
    places = entities_df.entity.values

    # prepare gmaps
    gmaps = googlemaps.Client(key='AIzaSyDii8HwHTwPH5vHYile-uNOQexmeOoMS74')
    # places =[
    #     "colonia Tepeyac, Tegucigalpa, Honduras",
    #     "colonia Loarque, Tegucigalpa, Honduras",
    #     "colonia Florencia Norte, Tegucigalpa, Honduras",
    # ]

    # get the geocode location
    data = []
    for ix, place in enumerate(places):
        entity = entities_df.iloc[ix]
        result = geocode(gmaps,place)
        data.append([entity.art_id, entity.entity, result["lat"], result["lng"] ])

    df = pd.DataFrame(data,columns=["art_id","entity", "lat", "long"])
    df.to_csv("../../files/geopoints.csv", index=False)

    
    



