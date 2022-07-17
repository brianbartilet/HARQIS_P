from Applications.Trello.references.web.base_api_service import *
from Applications.Trello.references.dto import *


class ApiServiceCards(BaseApiServiceTrello):

    def initialize(self):
        super(ApiServiceCards, self).initialize()
        self.request.\
            add_uri_parameter('cards')

    @deserialized(DtoCard)
    def add_card(self, card: DtoCard):
        self.request.add_query_object(card)

        return self.send_post_request(self.request.build())

    @deserialized(DtoCard)
    def archive_card(self, card: DtoCard):
        self.request\
            .add_uri_parameter(card.id)\
            .add_uri_parameter('closed')\
            .add_query_string('value', 'true')

        return self.send_put_request(self.request.build())

    @deserialized(DtoCard)
    def update_card(self, card: DtoCard):
        self.request\
            .add_uri_parameter('id', card.id)\
            .add_query_object(card)

        return self.send_put_request(self.request.build())

    @deserialized(DtoCard)
    def get_card(self, card_id: str):
        self.request\
            .add_uri_parameter('id', card_id)\

        return self.send_get_request(self.request.build())

    @deserialized(DtoCard)
    def add_attachment_to_card(self, card_id : str, attachment_info: DtoAttachment):
        self.request\
            .add_uri_parameter(card_id)\
            .add_uri_parameter('attachments')\
            .add_query_object(attachment_info)

        return self.send_post_request(self.request.build())

    @deserialized(DtoCard)
    def add_file_attachment_to_card(self, card_id : str, attachment_info: DtoAttachment):
        self.request\
            .add_uri_parameter(card_id)\
            .add_uri_parameter('attachments')\
            .add_query_string('name', attachment_info.name)\
            .add_query_string('mimeType', attachment_info.mimeType)

        files = {'file': open(str(attachment_info.file), 'rb')}

        return self.send_post_request(self.request.build(), files=files)

    @deserialized(DtoAttachment)
    def get_attachments(self, card_id : str):
        self.request\
            .add_uri_parameter(card_id)\
            .add_uri_parameter('attachments')\

        return self.send_get_request(self.request.build())

    @deserialized(DtoAttachment)
    def get_attachment(self, card_id : str, attachment_id: str):
        self.request\
            .add_uri_parameter(card_id)\
            .add_uri_parameter('attachments')\
            .add_uri_parameter(attachment_id)

        return self.send_get_request(self.request.build())

    def download_attachment(self, attachment_url: str, attachment_id: str, file_type: str, location_path=None):
        response = requests.get(attachment_url, allow_redirects=True, proxies=self.client.config['proxies'])
        lp = location_path if location_path is not None else ''
        file_name = '{0}{1}'.format(attachment_id, file_type)
        open(os.path.join(lp, file_name), 'wb').write(response.content)

        return file_name
