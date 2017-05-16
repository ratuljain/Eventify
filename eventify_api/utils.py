import json
import urllib

from jose import jwt


def parse_firebase_token(id_token):

    target_audience = "eventifyapp-d5196"

    certificate_url = 'https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com'

    response = urllib.urlopen(certificate_url)
    certs = response.read()
    certs = json.loads(certs)

    # will throw error if not valid
    user = jwt.decode(id_token, certs, algorithms='RS256',
                      audience=target_audience)

    return user


def convertToBoolean(param):
    return param in ['true', '1', 'True']


def send_notification_to_multiple(push_service, users_fcm_queryset, message_title, message_body):
    result = push_service.notify_multiple_devices(registration_ids=users_fcm_queryset, message_title=message_title,
                                                  message_body=message_body)

    print result
