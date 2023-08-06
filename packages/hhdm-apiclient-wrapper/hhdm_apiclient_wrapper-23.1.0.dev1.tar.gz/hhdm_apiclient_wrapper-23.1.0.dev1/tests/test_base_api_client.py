from unittest import IsolatedAsyncioTestCase

from hhdm_apiclient_wrapper import *

class TestBaseApiClient(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.auth_settings = AuthenticationSettings(
            api_key='4b1e2320-7494-4372-a6ab-613292d23593',
            authentication_mode=AuthenticationMode.API_KEY,
        )
        self.client = ApiClient(
            authentication_manager=AuthenticationManager(self.auth_settings),
            api_host='https://hhdm-api.hh-dev.com/'
        )

    def test_valid_api_host_str(self) -> None:
        expected_str = 'https://hhdm-api.hh-dev.com/'
        test_client = ApiClient(
            authentication_manager=AuthenticationManager(self.auth_settings),
            api_host='https://hhdm-api.hh-dev.com/'
        )
        self.assertEqual(expected_str, test_client._api_endpoint)

    def test_fix_api_host_str(self) -> None:
        expected_str = 'https://hhdm-api.hh-dev.com/'
        test_client = ApiClient(
            authentication_manager=AuthenticationManager(self.auth_settings),
            api_host='hhdm-api.hh-dev.com'
        )
        self.assertEqual(expected_str, test_client._api_endpoint)
    
    def test_invalid_api_host_str(self) -> None:
        self.assertRaises(
            ValueError,
            ApiClient,
            authentication_manager=AuthenticationManager(self.auth_settings),
            api_host='htttps://hhdm-api.hh-dev.com'
        )


    def test_build_url_parameters_empty(self) -> None:
        expected_str = ''
        built_parameters = self.client.build_url_parameters(ApiGetOptions(parameters_to_include=[]))

        self.assertEqual(expected_str, built_parameters, 'Built url parameter string is not expected')

    def test_build_url_parameters_only_options(self) -> None:
        expected_str = 'parametersToInclude=Id,Events'
        built_parameters = self.client.build_url_parameters(ApiGetOptions(parameters_to_include=['Id', 'Events']))

        self.assertEqual(expected_str, built_parameters, 'Built url parameter string is not expected')
    
    def test_build_url_parameters_both_options_and_additional(self) -> None:
        expected_str = 'TestKey=TestValue&parametersToInclude=Id,Events'
        built_parameters = self.client.build_url_parameters(ApiGetOptions(parameters_to_include=['Id', 'Events']), additional_parameters={'TestKey': 'TestValue'})

        self.assertEqual(expected_str, built_parameters, 'Built url parameter string is not expected')
