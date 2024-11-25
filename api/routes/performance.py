from flask import Blueprint, current_app, make_response, json
from api.exceptions.exception_handler import db_exception_handler

from api.util.util import get_methods

# Define the performance_routes blueprint
performance_routes = Blueprint('performance', __name__, url_prefix='/performance')


@performance_routes.route('/run', methods=['POST'])
@db_exception_handler
def evaluate_perf():
    try:
        methods = get_methods(is_simulation_data=False)
        methods.add_performance_metrics()

        return make_response(json.jsonify({"message": "Performance evaluated successfully!"}), 200)

    except ValueError as e:
        # Catch errors related to missing configurations and return an appropriate response
        current_app.logger.error(f"Configuration error: {str(e)}")
        return make_response(json.jsonify({"error": str(e), "status": "Aborted mission!"}), 500)

    except Exception as e:
        # Catch any other unexpected errors
        current_app.logger.error(f"Error during performance evaluation: {str(e)}")
        return make_response(json.jsonify({
            "error": str(e),
            "status": "Aborted mission due to an error during performance evaluation!"
        }), 500)
