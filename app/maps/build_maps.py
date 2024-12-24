import time
import folium
from app.utils.coordinates_from_region import get_coordinates_with_opencage, get_country_coordinates


def create_map_with_real_locations(data, map_type="casualties", df_country=None):

    map_object = folium.Map(location=[20, 0], zoom_start=2)

    for entry in data:
        # time.sleep(1)

        if map_type == "shared_targets":

            country = entry["country"]
            coords = get_country_coordinates(country, df_country)

            if coords is None:
                print(f"Skipping country {country}: coordinates not found.")
                continue

            print(coords)
            targets = entry.get("targets", [])
            popup_content = f"<b>{country}</b><br>Shared Targets:<br>"
            for target in targets:
                popup_content += f"Target: {target['target']}<br>Groups: {', '.join(target['groups'])}<br><br>"

            folium.Marker(
                location=coords,
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color="purple", icon="info-sign")
            ).add_to(map_object)

        elif map_type == "casualties":

            region = entry["region"]
            coords = get_coordinates_with_opencage(region)

            avg_casualties = entry.get("average_casualties", 0)
            tooltip = f"{region}: {avg_casualties:.2f} Average Casualties"
            folium.Marker(
                location=coords,
                popup=tooltip,
                icon=folium.Icon(color="red" if avg_casualties > 10 else "green")
            ).add_to(map_object)

        elif map_type == "activity":

            region = entry["region"]
            coords = get_coordinates_with_opencage(region)

            top_groups = entry.get("top_groups", [])
            popup_content = f"<b>{region}</b><br>Top 5 Groups:<br>"
            for group in top_groups:
                popup_content += f"{group['group']}: {group['event_count']} events<br>"
            folium.Marker(
                location=coords,
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(map_object)

        elif map_type == "yearly_change":

            region = entry["region"]
            coords = get_coordinates_with_opencage(region)

            yearly_change = entry.get("yearly_change", [])
            popup_content = f"<b>{region}</b><br>Yearly Change:<br>"
            for year_data in yearly_change:
                year = year_data["year"]
                change = year_data["change_percentage"]
                popup_content += f"{year}: {change:.2f}%<br>"
            folium.Marker(
                location=coords,
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(map_object)

        elif map_type == "groups_by_country":

            country = entry["country"]
            coords = get_country_coordinates(country, df_country)

            if coords is None:
                print(f"Skipping country {country}: coordinates not found.")
                continue

            groups = entry.get("groups", [])
            group_count = entry.get("group_count", 0)

            popup_content = f"<b>{country}</b><br>Number of Groups: {group_count}<br>"
            popup_content += f"Groups: {', '.join(groups)}"

            folium.Marker(
                location=coords,
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(map_object)

        elif map_type == "attack_strategies":

            cached_coordinates = {}

            country = entry["country"]
            if country not in cached_coordinates:
                coords = get_country_coordinates(country, df_country)
                if coords is None:
                    print(f"Skipping country {country}: coordinates not found.")
                    continue
                cached_coordinates[country] = coords
            else:
                coords = cached_coordinates[country]

            attack_type = entry["attack_type"]
            groups = entry["groups"]
            group_count = entry["group_count"]

            popup_content = f"<b>{country}</b><br>Attack Type: {attack_type}<br>"
            popup_content += f"Number of Groups: {group_count}<br>"
            popup_content += f"Groups: {', '.join(groups)}"

            folium.Marker(
                location=coords,
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color="green", icon="info-sign")
            ).add_to(map_object)

    return map_object
