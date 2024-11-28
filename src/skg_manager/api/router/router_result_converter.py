from flask import Response, jsonify, make_response

from skg_manager import Result


def convert_result_into_response(result: Result) -> Response:
    if result.data is not None:
        return jsonify(result.data)
    else:
        mapping_to_code = {
            Result.Status.SUCCESS: 200,
            Result.Status.FAILURE: 500,
            Result.Status.NOT_IMPLEMENTED: 501
        }

        return make_response(
            result.message,
            mapping_to_code[result.status],
        )
