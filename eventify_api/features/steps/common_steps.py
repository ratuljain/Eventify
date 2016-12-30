import json
import urlparse

import requests
from django.utils.six import BytesIO
from lettuce import step, world
from nose.tools import assert_equals
from rest_framework.parsers import JSONParser

baseURL = "http://127.0.0.1:9000"
# Asserting the expected status code of the request


def response_to_dict(json_response):
    stream = BytesIO(json_response)
    data = JSONParser().parse(stream)
    return data


@step('I get a (\d+) response')
def step_impl(step, expected_status_code):
    """
    :type step: lettuce.core.Step
    """
    assert_equals(int(expected_status_code), world.r.status_code)

# Retrieve a list of resources given an endpoint


@step('I send a GET request to "(.*)"')
def step_impl(step, endpoint):
    """
    :type step: lettuce.core.Step
    """
    url = urlparse.urljoin(baseURL, endpoint)
    world.r = requests.get(url)


@step('I send a POST request to "(.*)"')
def step_impl(step, endpoint):
    """
    :type step: lettuce.core.Step
    """
    url = urlparse.urljoin(baseURL, endpoint)
    world.r = requests.post(url, data=world.payload)


@step('the response should be JSON "(.*)":')
def step_impl(step, respone_text):
    """
    :type step: lettuce.core.Step
    """
    json_response_string =  world.r.text
    assert_equals(json.loads(json_response_string), json.loads(respone_text))


# Retrieve a resource given an endpoint with resource and an ID


# @step('I send a GET a "(.*)" with id "(.*)"')
# def step_impl(step, endpoint, id):
#     """
#     :type step: lettuce.core.Step
#     """
#     url = baseURL + endpoint + id
#     # print(url)
#     world.r = requests.get(url)


# Checking the type of response body and it's length
# @step("response body is a (\w+) of JSON containing (\d+) (\w+)")
# def step_impl(step, type, count, item):
#     """
#     :type step: lettuce.core.Step
#     """
#     json_response = world.r.text
#
#     stream = BytesIO(json_response)
#     data = JSONParser().parse(stream)
#
#     validate_list(data, type=type, count=count)


# Verify returned resource with the values in the step table
# @step("response body has attributes:")
# def step_impl(step):
#     """
#     :type step: lettuce.core.Step
#     """
#     json_response = world.r.text
#
#     stream = BytesIO(json_response)
#     data = JSONParser().parse(stream)
#
#     table_dict = table_to_hash(step.hashes)
#     keys = table_dict.keys()
#
#     for key in keys:
#         assert_equal(data[key], table_dict[key])
