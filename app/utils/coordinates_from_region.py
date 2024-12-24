from opencage.geocoder import OpenCageGeocode
from app.settings.config import api_key_open_cage


def get_coordinates_with_opencage(region_name):

    key = api_key_open_cage
    geocoder = OpenCageGeocode(key)
    try:
        result = geocoder.geocode(region_name)
        if result:
            return [result[0]["geometry"]["lat"], result[0]["geometry"]["lng"]]
        else:
            return [0, 0]
    except Exception as e:
        print(f"Error getting coordinates for {region_name}: {e}")
        return [0, 0]


# def get_country_coordinates(country_name, df_country):
#     try:
#         print(df_country)
#         row = df_country[df_country["Country"].str.strip().str.lower() == country_name.strip().lower()]
#         if not row.empty:
#             latitude = float(row.iloc[0]["Latitude (average)"])
#             longitude = float(row.iloc[0]["Longitude (average)"])
#             return latitude, longitude
#         else:
#             return None
#     except Exception as e:
#         print(f"Error retrieving coordinates: {e}")
#         return None

def get_country_coordinates(country_name, df_country):
    try:
        if df_country["Latitude (average)"].dtype == "object":
            df_country["Latitude (average)"] = (
                df_country["Latitude (average)"].str.replace('"', '').str.strip().astype(float)
            )
        if df_country["Longitude (average)"].dtype == "object":
            df_country["Longitude (average)"] = (
                df_country["Longitude (average)"].str.replace('"', '').str.strip().astype(float)
            )

        row = df_country[df_country["Country"].str.strip().str.lower() == country_name.strip().lower()]
        if not row.empty:
            latitude = float(row.iloc[0]["Latitude (average)"])
            longitude = float(row.iloc[0]["Longitude (average)"])
            return latitude, longitude
        else:
            return None
    except Exception as e:
        print(f"Error retrieving coordinates: {e}")
        return None



