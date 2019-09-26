__author__ = 'patley'
from utils.constants import ResponseStatusCode

def get_plain_response(response):
    # Can add headers and stuff
    return response

def get_failed_response(response):
    response["status"] = "fail"
    response["code"] = ResponseStatusCode.SUCCESS
    return get_plain_response(response)


def get_success_response(response):
    response["status"] = "success"
    response["code"] = ResponseStatusCode.SUCCESS
    return get_plain_response(response)


def get_bad_request_response(response):
    response["status"] = "fail"
    response["code"] = ResponseStatusCode.BAD_REQUEST
    return get_plain_response(response)

def get_internal_error_response(response):
    response["status"] = "fail"
    response["code"] = ResponseStatusCode.INTERNAL_ERROR
    return get_plain_response(response)
