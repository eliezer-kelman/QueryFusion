import uuid

from flask import request, render_template, Blueprint
import os
from app.maps.build_maps import create_map_with_real_locations
from app.queries.mongo_queries import average_casualties_by_region, top_5_groups_per_region, yearly_change_by_region
from app.queries.neo4j_queries import get_shared_targets_all_regions, get_groups_by_country, \
    get_attack_strategies_by_country
import pandas as pd

index_blueprint = Blueprint('/', __name__)

csv_path = os.path.join(os.getcwd(), "templates", "countries_codes_and_coordinates.csv")

@index_blueprint.route("/")
def index():
    return render_template("index.html")

@index_blueprint.route("/query", methods=["POST"])
def run_query():
    query_type = request.form.get("query")
    print(f"Running query: {query_type}")
    if query_type == "casualties":
        data = average_casualties_by_region()
        map_object = create_map_with_real_locations(data, map_type="casualties")
    elif query_type == "activity":
        data = top_5_groups_per_region()
        map_object = create_map_with_real_locations(data, map_type="activity")
    elif query_type == "yearly_change":
        data = yearly_change_by_region()
        map_object = create_map_with_real_locations(data, map_type="yearly_change")
    elif query_type == "shared_targets":
        data = get_shared_targets_all_regions()
        map_object = create_map_with_real_locations(data, map_type="shared_targets", df_country=pd.read_csv(csv_path))
    elif query_type == "groups_by_country":
        data = get_groups_by_country()
        map_object = create_map_with_real_locations(data, map_type="groups_by_country", df_country=pd.read_csv(csv_path))
    elif query_type == "attack_strategies":
        data = get_attack_strategies_by_country()
        map_object = create_map_with_real_locations(data, map_type="attack_strategies", df_country=pd.read_csv(csv_path))
    else:
        return "Invalid query type", 400

    unique_id = str(uuid.uuid4())
    map_path = os.path.join("templates", f"result_map_{unique_id}.html")
    map_object.save(map_path)

    return render_template(f"result_map_{unique_id}.html")
