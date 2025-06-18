def api_response(success=True, message="", data=None, status_code=200):
    if data is None:
        data = {}
    return {
        "success": success,
        "message": message,
        "data": data,
        "status_code": status_code
    }