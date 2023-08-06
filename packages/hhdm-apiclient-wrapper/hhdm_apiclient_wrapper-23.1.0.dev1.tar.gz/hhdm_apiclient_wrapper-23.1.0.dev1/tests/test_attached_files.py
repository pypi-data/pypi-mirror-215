import logging
from unittest import IsolatedAsyncioTestCase

from hhdm_apiclient_wrapper import *


# TODO: all of these tests should be auto generated for each entity definition generated in the api_client.py
# based on some config json/yaml file containing entity ids. Some environment config file should be setup as well
# with the API key/endpoint.

class TestAttachedFiles(IsolatedAsyncioTestCase):

    account_id = '6d22f6d9-4b35-41dd-86c5-713b1d2cc765'

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s', level=logging.INFO)

    @classmethod
    def setUpClass(self) -> None:
        self.auth_settings = AuthenticationSettings(
            api_key='4b1e2320-7494-4372-a6ab-613292d23593',
            authentication_mode=AuthenticationMode.API_KEY,
        )
        self.client = ApiClient(
            authentication_manager=AuthenticationManager(self.auth_settings),
            api_host='https://hhdm-api.hh-dev.com/'
        )
    
    async def test_get_attachments_by_id(self) -> None:
        pass
        # response = await self.client.get_championship_attachments_by_id(
        #     account_id=self.account_id,
        #     championshipId="",
        #     attachment_ids=[]
        # )

        # self.assertEqual(response.success, True, 'Call to get championship attachments by id failed')
        # self.assertGreater(len(response.return_value[0]['Events']), 0, 'Received no championship events')

    async def test_get_attachments_by_name(self) -> None:
        pass
        # response = await self.client.get_championship_attachments_by_id(
        #     account_id=self.account_id,
        #     championshipId="",
        #     attachment_ids=[]
        # )

        # self.assertEqual(response.success, True, 'Call to get championship attachments by id failed')
        # self.assertGreater(len(response.return_value[0]['Events']), 0, 'Received no championship events')

    async def test_get_invalid_attachment_by_id(self) -> None:
        pass

    async def test_get_invalid_attachment_by_name(self) -> None:
        pass

    async def test_upload_attachment_uncompressed(self) -> None:
        pass

    async def test_upload_attachment_compressed(self) -> None:
        pass

    async def test_upload_attachment_to_wrong_custom_property(self) -> None:
        pass

    async def test_update_attachment(self) -> None:
        pass

    async def test_update_invalid_attachment(self) -> None:
        pass

    async def test_delete_attachment(self) -> None:
        pass

    async def test_delete_invalid_attachment(self) -> None:
        pass
    