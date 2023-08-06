from asyncio import Future
from contextlib import suppress
from http import HTTPStatus
import importlib.metadata
import json
import lz4.frame
from pathlib import Path
import requests
from typing import Dict
import validators

from hhdm_apiclient_wrapper.authentication_manager import AuthenticationManager
from hhdm_apiclient_wrapper.models import *

class ApiClient:
    # By default requests library will not timeout if timeout is set to None
    # Timeout can also be passed as a tuple (connect_timeout_seconds, response_timeout_seconds)
    MAX_TIMEOUT_SECONDS = None # 20 * 60

    def __init__(self, authentication_manager: AuthenticationManager, api_host: str) -> None:
        if api_host:
            if validators.url(api_host):
                self._api_endpoint = api_host
            elif validators.url('https://' + api_host):
                self._api_endpoint = 'https://' + api_host
            else:
                raise ValueError(f'Passed argument apiHost ({api_host}) is not a valid URI.')
            if self._api_endpoint[-1] != '/':
                self._api_endpoint += '/'
        else:
            self._api_endpoint = 'https://hhdm-api.hh-dev.com/'

        self._authentication_manager = authentication_manager

#region Manual Endpoints

    async def get_part_item_mileages_by_event(self, account_id: str, part_item_ids: List[str]) -> Future[ApiGetResult[List[MileageRecordByEvent]]]:
        if isinstance(part_item_ids, str):
            part_item_ids = [part_item_ids]
        if isinstance(part_item_ids, List) == False:
            raise TypeError('part_item_ids must be either a list of ids or a string containing a single id')
        
        return self._get_item_mileages_by_event(account_id, ItemMileageRequest(part_item_ids=part_item_ids))
        
    async def get_assembly_iteration_mileages_by_event(self, account_id: str, assembly_iteration_ids: List[str]) -> Future[ApiGetResult[List[MileageRecordByEvent]]]:
        if isinstance(assembly_iteration_ids, str):
            assembly_iteration_ids = [assembly_iteration_ids]
        if isinstance(assembly_iteration_ids, List) == False:
            raise TypeError('assembly_iteration_ids must be either a list of ids or a string containing a single id')
        
        return self._get_item_mileages_by_event(account_id, ItemMileageRequest(assembly_iteration_ids=assembly_iteration_ids))

    async def _get_item_mileages_by_event(self, account_id: str, item_mileage_request: ItemMileageRequest) -> Future[ApiGetResult[List[MileageRecordByEvent]]]:
        try:
            url = f'{self._api_endpoint}Mileage/PartItems?{self.build_url_parameters(None, {"byEvent": True})}'
            response = await self.get_request(account_id, url, item_mileage_request, self.MAX_TIMEOUT_SECONDS)

            if response.ok == False:
                return ApiGetResult(None, False, response.reason, response.status_code)

            response_string = response.content.decode()
            if not response_string:
                return ApiGetResult(None, False, 'The mileage items requested were not found.', response.status_code)
            
            response_json = json.loads(response_string)
            response_object = [MileageRecordByEvent.deserialize(o) for o in response_json]

            return ApiGetResult(response_object, True, None, response.status_code)
        except Exception as e:
            return ApiGetResult(None, False, f'Internal server error: {e}', HTTPStatus.INTERNAL_SERVER_ERROR)
        
    async def get_all_mileages_by_event(self, account_id: str) -> Future[ApiGetResult[MileagesResult[MileageRecordByEvent]]]:
        try:
            url = f'{self._api_endpoint}Mileage/All?{self.build_url_parameters(None, {"accountId": account_id, "byEvent": True})}'
            response = await self.get_request(account_id, url, timeout=self.MAX_TIMEOUT_SECONDS)

            if response.ok == False:
                return ApiGetResult(None, False, response.reason, response.status_code)

            response_string = response.content.decode()
            if not response_string:
                return ApiGetResult(None, False, 'No items with mileages were found on the requested account.', response.status_code)

            response_json = json.loads(response_string)
            response_object = MileagesResult.deserialize(response_json)

            return ApiGetResult(response_object, True, None, response.status_code)
        except Exception as e:
            return ApiGetResult(None, False, f'Internal server error: {e}', HTTPStatus.INTERNAL_SERVER_ERROR)

#endregion

    #### NOT REQUIRED FOR V1 ####
    '''
    async def get_account_options_by_id(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[ApiAccountOptionsModel]]:
        url = f'{self._api_endpoint}AccountOptions/{account_id}'

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += '?' + url_parameters

        response: requests.Response = await requests.get(url)

        if not response.ok:
            return ApiGetResult[ApiAccountOptionsModel](None, False, response.reason)

        response_string = response.content.decode()
        response_object = ApiAccountOptionsModel(**(json.loads(response_string)))
        return ApiGetResult[ApiAccountOptionsModel](response_object, True, None)
    '''


#region Network Functions

    async def get_request(self, account_id: str, uri: str, body: IApiModel = None, timeout: float | tuple[float] | None = None) -> Future[requests.Response]:
        content = body.serialize() if body is not None else {}
        headers = await self.prepare_request(account_id)

        return requests.get(uri, json=content, headers=headers, timeout=timeout) # verify=False is needed for requests to localhost

    async def post_request(self, account_id: str, uri: str, body: IApiModel = None) -> Future[requests.Response]:
        content = body.serialize() if body is not None else {}
        headers = await self.prepare_request(account_id)

        return requests.post(uri, json=content, headers=headers)

    async def put_request(self, account_id: str, uri: str, body: IApiModel = None) -> Future[requests.Response]:
        content = body.serialize() if body is not None else {}
        # Content-Type is only required for put request for some reason
        headers = await self.prepare_request(account_id, {'Content-Type': 'application/json'})

        return requests.put(uri, json=content, headers=headers)

    async def delete_request(self, account_id: str, uri: str) -> Future[requests.Response]:
        headers = await self.prepare_request(account_id)

        return requests.delete(uri, headers=headers)
    
    async def upload_file(self, uri: str, file_path: str, file_name: str, headers: Dict[str, object]):
        with open(file_path, 'rb') as f:
            response = requests.put(uri, files={'file': (file_name, f)}, headers=headers, stream=True)
            return response.ok
        
    async def compress_and_upload_file(self, uri: str, file_path: str, file_name: str, headers: Dict[str, object]):
        with open(file_path, 'rb') as f:
            compressed = lz4.frame.compress(f.read())
            response = requests.put(uri, files={'file': (file_name, compressed)}, headers=headers, stream=True)
            return response.ok
    

    async def prepare_request(self, account_id: str, other_headers: Dict = None) -> Future[Dict]:
        headers = {
            "AccountId": account_id,
            **(await self._authentication_manager.get_http_request_auth())
        }
        if other_headers:
            headers = { **headers, **other_headers }
        
        return headers


    def _serialize_body(self, body: Dict) -> bytes:
        return json.dumps(body).encode('utf8') if body is not None else None

    def build_url_parameters(self, options: ApiGetOptions, additional_parameters: Dict[str, str] = {}) -> str:
        if options is not None:
            if options.parameters_to_include is not None and len(options.parameters_to_include) > 0:
                additional_parameters['parametersToInclude'] = ','.join(options.parameters_to_include)
        
        return '&'.join([f'{k}={v}' for k, v in list(additional_parameters.items())])

    def _send_debug_request(self, method: str, uri: str, json: Dict, headers: Dict) -> requests.Response:
        request = requests.Request(method, uri, json=json, headers=headers)
        prepared = request.prepare()

        print('{}\n{}\r\n{}\r\n\r\n{}'.format(
                '-----------START-----------',
                prepared.method + ' ' + prepared.url,
                '\r\n'.join('{}: {}'.format(k, v) for k, v in prepared.headers.items()),
                prepared.body,
            ))

        s = requests.Session()
        return s.send(prepared)

#endregion


    def get_version(self, include_found_dir: bool = False) -> str:
        """Returns either the version found in the parent pyproject.toml file, or the installed package"""
        with suppress(FileNotFoundError, StopIteration):
            with open(f'{(root_dir := Path(__file__).parent.parent)}/pyproject.toml', encoding='utf-8') as pyproject_toml:
                version = (
                    next(line for line in pyproject_toml if line.startswith('version'))
                    .split('=')[1]
                    .strip('\'"\n ')
                )
                return f'{version} (local dev){f" ({root_dir})" if include_found_dir else ""}'
        return importlib.metadata.version(__name__.split(".", maxsplit=1)[0])

    
