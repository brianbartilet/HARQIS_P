from Applications.Lazada.references.web.base_api_service import *
from Applications.Lazada.references.dto import *
from requests_oauth2 import OAuth2
import datetime
import hmac, hashlib

class LazadaAuthClient(OAuth2):
    site = "https://auth.lazada.com"
    authorization_url = "/oauth/authorize"
    token_url = "/rest/token/create"
    scope_sep = " "


def sign(secret, api, parameters):
    # ===========================================================================
    # @param secret
    # @param parameters
    # ===========================================================================
    sort_dict = sorted(parameters)

    parameters_str = "%s%s" % (api,
                               str().join('%s%s' % (key, parameters[key]) for key in sort_dict))

    h = hmac.new(secret.encode(encoding="utf-8"), parameters_str.encode(encoding="utf-8"), digestmod=hashlib.sha256)

    return h.hexdigest().upper()



class ApiServiceLazadaAuth(BaseApiServiceOANDA):

    def __init__(self, source_id):
        super(ApiServiceLazadaAuth, self).__init__(source_id=source_id)
        self.initialize()



        self.auth = LazadaAuthClient(
            client_id='123137',
            client_secret='NqsJ32hSJ4O6LZNwWGyO073JjdMQAYva',
            redirect_uri = "https://www.lazada.com.ph/"
        )



    def initialize(self):
        super(ApiServiceLazadaAuth, self).initialize()
        self.request.\
            add_uri_parameter('oauth/authorize')

    @deserialized(dict)
    def get_authorization_url(self, client_id,
                              redirect_uri,
                              response_type='code',
                              force_auth='false',
                              uuid=None,
                              country='ph'):
        self.request \
            .add_query_string('client_id', client_id) \
            .add_query_string('redirect_uri', redirect_uri) \
            .add_query_string('response_type', response_type)\
            .add_query_string('force_auth', force_auth)\
            .add_query_string('uuid', uuid)\
            .add_query_string('country', country)



        return self.send_post_request(self.request.build())

    @deserialized(dict)
    def get_token(self, app_key, app_secret, code, sign_method='sha256'):
        ts = str(int(round(time.time()))) + '000'
        parameters = {
            'app_key': app_key,
            'sign_method': sign_method,
            'timestamp': ts,
            'partner_id': 'lazop-sdk-python-20181207',
            'api_id': "1",

        }
        sig = sign(app_secret, '/auth/token/create', parameters)

        self.request.add_header('Content-Type', 'application/json')
        self.request\
            .add_query_string('app_key', app_key)\
            .add_query_string('app_secret', app_secret)\
            .add_query_string('code', code)\
            .add_query_string('timestamp', "")\
            .add_query_string('sign_method', 'sha256')\
            .add_query_string('sign', sig)
        x = self.send_post_request(self.request.build())

        return x


    def test_authorize(self):
        authorization_url = self.auth.authorize_url(
            scope=["email"],
            response_type="code",
        )
        x=0