__author__ = 'patley'


def get_plain_response(response):
    # Can add headers and stuff
    return response


def get_failed_response(response):
    response["status"] = "fail"
    return get_plain_response(response)


def get_success_response(response):
    response["status"] = "success"
    return get_plain_response(response)
