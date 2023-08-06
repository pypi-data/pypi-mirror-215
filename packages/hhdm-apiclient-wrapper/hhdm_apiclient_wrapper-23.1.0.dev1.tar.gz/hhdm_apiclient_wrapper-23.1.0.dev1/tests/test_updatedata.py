import asyncio
from datetime import datetime, timedelta
import logging
import unittest

from hhdm_apiclient_wrapper import *


class TestUpdatedata(unittest.IsolatedAsyncioTestCase):

    account_id = '6d22f6d9-4b35-41dd-86c5-713b1d2cc765'
    championship_id = None
    tyre_id = None

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
    
    @classmethod
    async def asyncTearDown(self) -> None:
        if TestUpdatedata.championship_id is not None:
            delete_success = await self.client.delete_championship(
                account_id=self.account_id,
                championship_id=TestUpdatedata.championship_id
            )
            
            if not delete_success:
                self.logger.warning(f'FAILED TO CLEAN UP CHAMPIONSHIP ({TestUpdatedata.championship_id}), please manually log in and delete it.')
        
        if TestUpdatedata.tyre_id is not None:
            delete_success = await self.client.delete_tyre(tyre_id=TestUpdatedata.tyre_id)
            
            if not delete_success:
                self.logger.warning(f'FAILED TO CLEAN UP TYRE ({TestUpdatedata.tyre_id}), please manually delete it.')


    async def test_modify_championship(self) -> None:
        response = await self.client.add_championship(
            account_id=TestUpdatedata.account_id,
            create_model=CreateModel(
                copy_from_last=True,
                copy_all=True,
                index=0,
                parameter_updates=[
                    ParameterUpdateModel('Name', 'TestChampionship'),
                    ParameterUpdateModel('Description', 'Test Description')
                ]
            )
        )
        
        self.assertEqual(response.success, True, f'Call to create championship failed: {response.message}')
        self.assertIsNotNone(response.return_value['Id'], 'Created championship not returned')

        TestUpdatedata.championship_id = response.return_value['Id']

        # We must wait a couple seconds because otherwise the API request to delete the championship will fail.
        await asyncio.sleep(3)

        update_success = await self.client.update_championship(
            account_id=self.account_id,
            championship_id=TestUpdatedata.championship_id,
            update_model=UpdateModel(
                last_modified_time_max_allowed_value=(datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%dT%H:%M:%S;%fZ'),
                parameter_updates=[
                    ParameterUpdateModel('Description', 'Modified test description')
                ]
            )
        )

        self.assertEqual(update_success, True, f'Call to update championship ({TestUpdatedata.championship_id}) failed')

        await asyncio.sleep(1)

        updated_championship = await self.client.get_championship_by_id(
            account_id=self.account_id,
            championship_id=TestUpdatedata.championship_id,
            options=ApiGetOptions(parameters_to_include=['Description'])
        )

        self.assertEqual(updated_championship.return_value['Parameters']['Description'], 'Modified test description', 'Championship not updated properly')

        # We must wait a couple seconds because otherwise the API request to delete the championship will fail.
        await asyncio.sleep(2)

        delete_success = await self.client.delete_championship(
            account_id=self.account_id,
            championship_id=TestUpdatedata.championship_id
        )

        self.assertEqual(delete_success, True, f'Call to delete championship ({TestUpdatedata.championship_id}) failed')

        # Unassign Championship ID so teardown does not try to delete it twice
        TestUpdatedata.championship_id = None

    @unittest.skip('Ability to delete tyres via the API is not yet deployed to production. Wait until EOY release to run.')
    async def test_modify_tyre(self) -> None:
        tyre_spec = 'f63b56c1-7fb2-4a5c-b1a3-812e12af9546'
        response = await self.client.add_tyre(
            account_id=TestUpdatedata.account_id,
            url_params={'tyreSpecificationId': tyre_spec},
            create_model=AssociationCreateModel(
                copy_from_last=True,
                copy_all=True,
                index=0,
                parameter_updates=[
                    ParameterUpdateModel('Name', 'Test Tyre'),
                    ParameterUpdateModel('Condition', 'New'),
                    ParameterUpdateModel('TyreSpecificationId', tyre_spec)
                ],
                ChampionshipAssociationsToAdd=[{
                    'ChampionshipId': '9e27a320-fe78-4609-b15c-9e4b0a7241e5',
                    'ParameterUpdates': [{
                        'Name': 'Name',
                        'Value': 'Test Championship Association Name'
                    }]
                }]
            )
        )

        self.assertEqual(response.success, True, f'Call to create tyre failed: {response.message}')
        self.assertIsNotNone(response.return_value['Id'], 'Created tyre not returned')

        TestUpdatedata.tyre_id = response.return_value['Id']

        await asyncio.sleep(3)

        update_success = await self.client.update_tyre(
            account_id=self.account_id,
            tyre_id=TestUpdatedata.tyre_id,
            update_model=AssociationUpdateModel(
                last_modified_time_max_allowed_value=(datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%dT%H:%M:%S;%fZ'),
                parameter_updates=[
                    ParameterUpdateModel('Name', 'Modified Test Tyre')
                ]
            )
        )

        self.assertEqual(update_success, True, f'Call to update tyre ({TestUpdatedata.tyre_id}) failed')

        await asyncio.sleep(2)

        delete_success = await self.client.delete_tyre(tyre_id=TestUpdatedata.tyre_id)

        self.assertEqual(delete_success, True, f'Call to delete tyre ({TestUpdatedata.tyre_id}) failed')

        # Unassign Tyre ID so teardown does not try to delete it twice
        TestUpdatedata.tyre_id = None

