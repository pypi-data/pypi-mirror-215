import logging
from unittest import IsolatedAsyncioTestCase

from hhdm_apiclient_wrapper import *


class TestMileages(IsolatedAsyncioTestCase):

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
    
    async def test_get_part_item_mileage(self) -> None:
        pass

    async def test_get_assembly_iteration_mileage(self) -> None:
        pass

    async def test_get_all_mileages(self) -> None:
        pass

    async def test_get_non_existant_part_item_mileage(self) -> None:
        pass

    async def test_get_non_existant_assembly_iteration_mileage(self) -> None:
        pass

    async def test_get_invalid_item_mileage(self) -> None:
        pass

    