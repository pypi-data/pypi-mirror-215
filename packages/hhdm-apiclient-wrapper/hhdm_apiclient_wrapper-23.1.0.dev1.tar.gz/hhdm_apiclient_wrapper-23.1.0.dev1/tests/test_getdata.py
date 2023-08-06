import logging
from unittest import IsolatedAsyncioTestCase

from hhdm_apiclient_wrapper import *


class TestGetdata(IsolatedAsyncioTestCase):

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
    
    async def test_get_all_championships(self) -> None:
        response = await self.client.get_all_championships(
            account_id=self.account_id,
            options=ApiGetOptions(parameters_to_include=['Events'])
        )

        self.assertEqual(response.success, True, 'Call to get all championships failed')
        self.assertGreater(len(response.return_value[0]['Events']), 0, 'Received no championship events')

    async def test_get_event_by_id(self) -> None:
        response = await self.client.get_event_by_id(
            account_id=self.account_id,
            event_id='3a32b2cc-ce85-45f9-8abd-c94bfc686d89',
            options=ApiGetOptions(parameters_to_include=['Cars', 'Cars.Car.Id'])
        )

        self.assertEqual(response.success, True, 'Call to get event with id (3a32b2cc-ce85-45f9-8abd-c94bfc686d89) failed')
        self.assertIsNotNone(response.return_value['Cars'][0]['Parameters']['Car']['Id'], 'Received no car ids')

    async def test_get_all_setups_for_event_car(self) -> None:
        event_id = '3a32b2cc-ce85-45f9-8abd-c94bfc686d89'
        car_id = '3dc8c163-4929-42cd-9038-46f0ed0d552a'
        response = await self.client.get_all_setups_for_event_car(
            account_id=self.account_id,
            event_id=event_id,
            car_id=car_id,
            options=ApiGetOptions(parameters_to_include=[])
        )

        self.assertEqual(response.success, True, f'Call to get all setups for event ({event_id}) car ({car_id}) failed: {response.message}')
        self.assertGreater(len(response.return_value), 0, 'Received no setups')

    async def test_search_for_tyres(self) -> None:
        event_id = '3a32b2cc-ce85-45f9-8abd-c94bfc686d89'
        car_id = '3dc8c163-4929-42cd-9038-46f0ed0d552a'

        championships = await self.client.get_all_championships(
            account_id=self.account_id,
            options=ApiGetOptions(parameters_to_include=['Events'])
        )

        self.assertEqual(championships.success, True, 'Failed to retrieve championship to search by')
        championship_id = championships.return_value[0]['Id']

        response = await self.client.search_for_tyres(
            account_id=self.account_id,
            search_info=AssociatedModelSeachObject(
                associated_model_search_mode=AssociatedModelSearchMode.EVENT_CAR,
                account_id=self.account_id,
                championship_id=championship_id,
                event_id=event_id,
                car_id=car_id
            ),
            options=ApiGetOptions(parameters_to_include=[])
        )

        self.assertEqual(response.success, True, f'Call to search for tyres of event ({event_id}) car ({car_id}) failed: {response.message}')
        self.assertGreater(len(response.return_value), 0, f'No tyres found even though search request succeeded')

