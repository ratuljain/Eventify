import urllib
import json
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
