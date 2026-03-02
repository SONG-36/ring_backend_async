def success(data=None, message="success"):
    return {
        "code": 0,
        "message": message,
        "data": data
    }