from django.utils.six import BytesIO
from lettuce import step, world
from rest_framework.parsers import JSONParser

baseURL = "http://127.0.0.1:9000"


def response_to_dict(json_response):
    stream = BytesIO(json_response)
    data = JSONParser().parse(stream)
    return data


@step("I have the following unregistered user with given information:")
def get_registration_info(step):
    """
    :type step: lettuce.core.Step
    """
    world.payload = step.hashes[0]
