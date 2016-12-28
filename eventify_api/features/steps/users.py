import requests
import rest_auth
from django.core.urlresolvers import reverse
from lettuce import step, world
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser

from rest_auth import urls
import urlparse

baseURL = "http://127.0.0.1:9000"


def response_to_dict(json_response):
    stream = BytesIO(json_response)
    data = JSONParser().parse(stream)
    return data


@step("I have the following unregistered user with given information:")
def step_impl(step):
    """
    :type step: lettuce.core.Step
    """
    world.payload = step.hashes[0]


@step('I send a POST request to "(.*)"')
def step_impl(step, endpoint):
    """
    :type step: lettuce.core.Step
    """
    url = urlparse.urljoin(baseURL, endpoint)
    world.r = requests.post(url, data = world.payload)

