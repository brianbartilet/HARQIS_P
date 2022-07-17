from Core import *

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import socket
from httplib2 import socks

from urllib.parse import urlparse


class GoogleApiClient(BaseApiClient):

    def __init__(self,
                 scopes_list: [],
                 credentials=os.path.join(ENV_PATH_APP_CONFIG, 'credentials.json'),
                 storage=os.path.join(ENV_PATH_APP_CONFIG, 'storage.json'),
                 **kwargs):

        super(GoogleApiClient, self).__init__(**kwargs)
        socket.socket = socks.socksocket

        self.scopes = scopes_list
        self.credentials = credentials
        self.storage = storage

        if str(ENV_ENABLE_PROXY).lower() == "true":
            result = urlparse(kwargs.get('proxies')['http'])
            socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, result.hostname, result.port)

    def authorize(self):
        store = file.Storage(self.storage)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(self.credentials, self.scopes)  # put this in the config proj
            creds = tools.run_flow(flow=flow, storage=store)

        return creds.authorize(Http())

