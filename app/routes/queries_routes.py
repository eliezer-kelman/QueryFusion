from flask import Blueprint, abort
import app.services.servics_routes as services_routes
import app.maps.build_maps as build_maps
from app.utils.path_utils import ensure_directory_exists

query_blueprint = Blueprint('/query', __name__)

@query_blueprint.route('/<int:query_id>', methods=['GET'])
def execute_query(query_id: int, filters: dict = None):
    try:
        result = services_routes.run_query(query_id, filters)
        return {"query_id": query_id, "result": result}
    except Exception as e:
        print(f"Error: {str(e)}")
        abort(500, description=str(e))


@query_blueprint.route('/attack_types_severity/<top_5>', methods=['GET'])
def get_attack_types_severity(top_5: str = 'false'):
    top_5 = top_5.lower() == 'true'
    result = services_routes.get_attack_types_severity(top_5)
    return {"result": result}


@query_blueprint.route("/top_terror_groups")
def get_top_terror_groups():
    result = services_routes.get_top_5_terror_groups()
    return {"result": result}


@query_blueprint.route("/expanding_groups")
def get_expanding_groups():
    result = services_routes.get_expanding_groups()
    return {"result": result}


@query_blueprint.route("/frequent_attackers_by_target")
def get_frequent_attackers_by_target():
    result = services_routes.get_frequent_attackers_by_target()
    return {"result": result}