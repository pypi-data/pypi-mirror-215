
from asyncio import Future
import json
from typing import Dict, List

from .. import base_api_client
from ..models import *

# Inherit from the manually written ApiClient class with utility methods and context
class ApiClient(base_api_client.ApiClient):

    async def get_ambient_measurement_by_id(self, account_id: str, ambient_measurement_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}AmbientMeasurements/{ambient_measurement_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_ambient_measurements_for_event(self, account_id: str, event_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}AmbientMeasurements"

        param_lookup = dict()
        param_lookup["eventId"] = event_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_ambient_measurement(self, account_id: str, event_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}AmbientMeasurements?eventId={event_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_ambient_measurement(self, account_id: str, ambient_measurement_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}AmbientMeasurements/{ambient_measurement_id}", update_model)
        return response.ok


    async def delete_ambient_measurement(self, account_id: str, ambient_measurement_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}AmbientMeasurements/{ambient_measurement_id}")
        return response.ok



    async def get_ambient_measurement_attachments_by_id(self, account_id: str, ambient_measurement_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}AmbientMeasurements/{ambient_measurement_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}AmbientMeasurements/{ambient_measurement_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_ambient_measurement_attachments_by_name(self, account_id: str, ambient_measurement_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}AmbientMeasurements/{ambient_measurement_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_ambient_measurement_attachment(self, account_id: str, ambient_measurement_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}AmbientMeasurements/{ambient_measurement_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_ambient_measurement_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, ambient_measurement_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_ambient_measurement_attachment(
            add_attached_file_response.account_id,
            ambient_measurement_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, ambient_measurement_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, ambient_measurement_id, None, None)


    async def _upload_ambient_measurement_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, ambient_measurement_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, ambient_measurement_id, file_path, file_name)

            return await self._set_ambient_measurement_attachment_server_state_to_completed(add_attached_file_response, ambient_measurement_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, ambient_measurement_id, file_path, file_name, message=e)


    async def add_attachment_to_ambient_measurement(self, account_id: str, ambient_measurement_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}AmbientMeasurements/{ambient_measurement_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, ambient_measurement_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, ambient_measurement_id, file_path, model.file_name)

        return await self._upload_ambient_measurement_attachment(parsed_response, ambient_measurement_id, file_path, model.file_name)


    async def retry_ambient_measurement_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_ambient_measurement_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_ambient_measurement_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_ambient_measurement_attachment(self, account_id: str, ambient_measurement_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}AmbientMeasurements/{ambient_measurement_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_car_by_id(self, account_id: str, car_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}Cars/{car_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_cars(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}Cars"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_car(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Cars?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_car(self, account_id: str, car_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Cars/{car_id}", update_model)
        return response.ok


    async def delete_car(self, account_id: str, car_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Cars/{car_id}")
        return response.ok



    async def get_car_attachments_by_id(self, account_id: str, car_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}Cars/{car_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}Cars/{car_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_car_attachments_by_name(self, account_id: str, car_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}Cars/{car_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_car_attachment(self, account_id: str, car_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Cars/{car_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_car_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, car_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_car_attachment(
            add_attached_file_response.account_id,
            car_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, car_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, car_id, None, None)


    async def _upload_car_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, car_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, car_id, file_path, file_name)

            return await self._set_car_attachment_server_state_to_completed(add_attached_file_response, car_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, car_id, file_path, file_name, message=e)


    async def add_attachment_to_car(self, account_id: str, car_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Cars/{car_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, car_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, car_id, file_path, model.file_name)

        return await self._upload_car_attachment(parsed_response, car_id, file_path, model.file_name)


    async def retry_car_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_car_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_car_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_car_attachment(self, account_id: str, car_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Cars/{car_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_championship_by_id(self, account_id: str, championship_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}Championships/{championship_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_championships(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}Championships"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_championship(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Championships?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_championship(self, account_id: str, championship_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Championships/{championship_id}", update_model)
        return response.ok


    async def delete_championship(self, account_id: str, championship_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Championships/{championship_id}")
        return response.ok



    async def get_championship_attachments_by_id(self, account_id: str, championship_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}Championships/{championship_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}Championships/{championship_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_championship_attachments_by_name(self, account_id: str, championship_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}Championships/{championship_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_championship_attachment(self, account_id: str, championship_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Championships/{championship_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_championship_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, championship_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_championship_attachment(
            add_attached_file_response.account_id,
            championship_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, championship_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, championship_id, None, None)


    async def _upload_championship_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, championship_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, championship_id, file_path, file_name)

            return await self._set_championship_attachment_server_state_to_completed(add_attached_file_response, championship_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, championship_id, file_path, file_name, message=e)


    async def add_attachment_to_championship(self, account_id: str, championship_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Championships/{championship_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, championship_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, championship_id, file_path, model.file_name)

        return await self._upload_championship_attachment(parsed_response, championship_id, file_path, model.file_name)


    async def retry_championship_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_championship_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_championship_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_championship_attachment(self, account_id: str, championship_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Championships/{championship_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_event_by_id(self, account_id: str, event_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}Events/{event_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def add_event(self, account_id: str, championship_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Events?championshipId={championship_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_event(self, account_id: str, event_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Events/{event_id}", update_model)
        return response.ok


    async def delete_event(self, account_id: str, event_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Events/{event_id}")
        return response.ok



    async def get_event_attachments_by_id(self, account_id: str, event_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}Events/{event_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}Events/{event_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_event_attachments_by_name(self, account_id: str, event_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}Events/{event_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_event_attachment(self, account_id: str, event_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Events/{event_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_event_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, event_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_event_attachment(
            add_attached_file_response.account_id,
            event_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, event_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, event_id, None, None)


    async def _upload_event_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, event_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, event_id, file_path, file_name)

            return await self._set_event_attachment_server_state_to_completed(add_attached_file_response, event_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, event_id, file_path, file_name, message=e)


    async def add_attachment_to_event(self, account_id: str, event_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Events/{event_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, event_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, event_id, file_path, model.file_name)

        return await self._upload_event_attachment(parsed_response, event_id, file_path, model.file_name)


    async def retry_event_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_event_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_event_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_event_attachment(self, account_id: str, event_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Events/{event_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_event_car_data_by_id(self, account_id: str, event_car_data_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}EventCarDatas/{event_car_data_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_event_car_data_for_event_car(self, account_id: str, event_id: str, car_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}EventCarDatas"

        param_lookup = dict()
        param_lookup["eventId"] = event_id
        param_lookup["carId"] = car_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[Dict](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = response_json
        return ApiGetResult(response_object, True, None)

    async def update_event_car_data(self, account_id: str, event_car_data_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}EventCarDatas/{event_car_data_id}", update_model)
        return response.ok


    async def get_event_car_data_attachments_by_id(self, account_id: str, event_car_data_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}EventCarDatas/{event_car_data_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}EventCarDatas/{event_car_data_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[Dict](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = response_json
        return ApiGetResult(response_object, True, None)


    async def get_event_car_data_attachments_by_name(self, account_id: str, event_car_data_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}EventCarDatas/{event_car_data_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[Dict](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = response_json
        return ApiGetResult(response_object, True, None)


    async def update_event_car_data_attachment(self, account_id: str, event_car_data_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}EventCarDatas/{event_car_data_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_event_car_data_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, event_car_data_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_event_car_data_attachment(
            add_attached_file_response.account_id,
            event_car_data_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, event_car_data_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, event_car_data_id, None, None)


    async def _upload_event_car_data_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, event_car_data_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, event_car_data_id, file_path, file_name)

            return await self._set_event_car_data_attachment_server_state_to_completed(add_attached_file_response, event_car_data_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, event_car_data_id, file_path, file_name, message=e)


    async def add_attachment_to_event_car_data(self, account_id: str, event_car_data_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}EventCarDatas/{event_car_data_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, event_car_data_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, event_car_data_id, file_path, model.file_name)

        return await self._upload_event_car_data_attachment(parsed_response, event_car_data_id, file_path, model.file_name)


    async def retry_event_car_data_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_event_car_data_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_event_car_data_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_event_car_data_attachment(self, account_id: str, event_car_data_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}EventCarDatas/{event_car_data_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_lap_by_id(self, account_id: str, lap_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}Laps/{lap_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def add_lap(self, account_id: str, run_sheet_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Laps?runSheetId={run_sheet_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_lap(self, account_id: str, lap_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Laps/{lap_id}", update_model)
        return response.ok


    async def delete_lap(self, account_id: str, lap_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Laps/{lap_id}")
        return response.ok



    async def get_lap_attachments_by_id(self, account_id: str, lap_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}Laps/{lap_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}Laps/{lap_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_lap_attachments_by_name(self, account_id: str, lap_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}Laps/{lap_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_lap_attachment(self, account_id: str, lap_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Laps/{lap_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_lap_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, lap_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_lap_attachment(
            add_attached_file_response.account_id,
            lap_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, lap_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, lap_id, None, None)


    async def _upload_lap_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, lap_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, lap_id, file_path, file_name)

            return await self._set_lap_attachment_server_state_to_completed(add_attached_file_response, lap_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, lap_id, file_path, file_name, message=e)


    async def add_attachment_to_lap(self, account_id: str, lap_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Laps/{lap_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, lap_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, lap_id, file_path, model.file_name)

        return await self._upload_lap_attachment(parsed_response, lap_id, file_path, model.file_name)


    async def retry_lap_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_lap_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_lap_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_lap_attachment(self, account_id: str, lap_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Laps/{lap_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_part_by_id(self, account_id: str, part_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}Parts/{part_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def add_part(self, account_id: str, part_category_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Parts?partCategoryId={part_category_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_part(self, account_id: str, part_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Parts/{part_id}", update_model)
        return response.ok


    async def delete_part(self, account_id: str, part_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Parts/{part_id}")
        return response.ok



    async def get_part_attachments_by_id(self, account_id: str, part_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}Parts/{part_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}Parts/{part_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_part_attachments_by_name(self, account_id: str, part_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}Parts/{part_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_part_attachment(self, account_id: str, part_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Parts/{part_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_part_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, part_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_part_attachment(
            add_attached_file_response.account_id,
            part_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, part_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, part_id, None, None)


    async def _upload_part_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, part_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, part_id, file_path, file_name)

            return await self._set_part_attachment_server_state_to_completed(add_attached_file_response, part_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, part_id, file_path, file_name, message=e)


    async def add_attachment_to_part(self, account_id: str, part_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Parts/{part_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, part_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, part_id, file_path, model.file_name)

        return await self._upload_part_attachment(parsed_response, part_id, file_path, model.file_name)


    async def retry_part_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_part_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_part_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_part_attachment(self, account_id: str, part_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Parts/{part_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_part_category_by_id(self, account_id: str, part_category_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}PartCategories/{part_category_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_part_categories(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}PartCategories"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def update_part_category(self, account_id: str, part_category_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}PartCategories/{part_category_id}", update_model)
        return response.ok


    async def delete_part_category(self, account_id: str, part_category_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}PartCategories/{part_category_id}")
        return response.ok



    async def get_part_category_attachments_by_id(self, account_id: str, part_category_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}PartCategories/{part_category_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}PartCategories/{part_category_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_part_category_attachments_by_name(self, account_id: str, part_category_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}PartCategories/{part_category_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_part_category_attachment(self, account_id: str, part_category_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}PartCategories/{part_category_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_part_category_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, part_category_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_part_category_attachment(
            add_attached_file_response.account_id,
            part_category_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, part_category_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, part_category_id, None, None)


    async def _upload_part_category_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, part_category_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, part_category_id, file_path, file_name)

            return await self._set_part_category_attachment_server_state_to_completed(add_attached_file_response, part_category_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, part_category_id, file_path, file_name, message=e)


    async def add_attachment_to_part_category(self, account_id: str, part_category_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}PartCategories/{part_category_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, part_category_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, part_category_id, file_path, model.file_name)

        return await self._upload_part_category_attachment(parsed_response, part_category_id, file_path, model.file_name)


    async def retry_part_category_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_part_category_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_part_category_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_part_category_attachment(self, account_id: str, part_category_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}PartCategories/{part_category_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_planned_run_by_id(self, account_id: str, planned_run_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}PlannedRuns/{planned_run_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def add_planned_run(self, account_id: str, run_plan_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}PlannedRuns?runPlanId={run_plan_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_planned_run(self, account_id: str, planned_run_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}PlannedRuns/{planned_run_id}", update_model)
        return response.ok


    async def delete_planned_run(self, account_id: str, planned_run_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}PlannedRuns/{planned_run_id}")
        return response.ok



    async def get_planned_run_attachments_by_id(self, account_id: str, planned_run_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}PlannedRuns/{planned_run_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}PlannedRuns/{planned_run_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_planned_run_attachments_by_name(self, account_id: str, planned_run_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}PlannedRuns/{planned_run_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_planned_run_attachment(self, account_id: str, planned_run_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}PlannedRuns/{planned_run_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_planned_run_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, planned_run_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_planned_run_attachment(
            add_attached_file_response.account_id,
            planned_run_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, planned_run_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, planned_run_id, None, None)


    async def _upload_planned_run_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, planned_run_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, planned_run_id, file_path, file_name)

            return await self._set_planned_run_attachment_server_state_to_completed(add_attached_file_response, planned_run_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, planned_run_id, file_path, file_name, message=e)


    async def add_attachment_to_planned_run(self, account_id: str, planned_run_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}PlannedRuns/{planned_run_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, planned_run_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, planned_run_id, file_path, model.file_name)

        return await self._upload_planned_run_attachment(parsed_response, planned_run_id, file_path, model.file_name)


    async def retry_planned_run_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_planned_run_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_planned_run_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_planned_run_attachment(self, account_id: str, planned_run_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}PlannedRuns/{planned_run_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_reference_pressure_run_by_id(self, account_id: str, reference_pressure_run_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}ReferencePressureRuns/{reference_pressure_run_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_reference_pressure_runs_for_event_car(self, account_id: str, event_id: str, car_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}ReferencePressureRuns"

        param_lookup = dict()
        param_lookup["eventId"] = event_id
        param_lookup["carId"] = car_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_reference_pressure_run(self, account_id: str, event_id: str, car_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}ReferencePressureRuns?eventId={event_id}&carId={car_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_reference_pressure_run(self, account_id: str, reference_pressure_run_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}ReferencePressureRuns/{reference_pressure_run_id}", update_model)
        return response.ok


    async def delete_reference_pressure_run(self, account_id: str, reference_pressure_run_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}ReferencePressureRuns/{reference_pressure_run_id}")
        return response.ok



    async def get_reference_pressure_run_attachments_by_id(self, account_id: str, reference_pressure_run_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}ReferencePressureRuns/{reference_pressure_run_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}ReferencePressureRuns/{reference_pressure_run_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_reference_pressure_run_attachments_by_name(self, account_id: str, reference_pressure_run_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}ReferencePressureRuns/{reference_pressure_run_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_reference_pressure_run_attachment(self, account_id: str, reference_pressure_run_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}ReferencePressureRuns/{reference_pressure_run_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_reference_pressure_run_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, reference_pressure_run_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_reference_pressure_run_attachment(
            add_attached_file_response.account_id,
            reference_pressure_run_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, reference_pressure_run_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, reference_pressure_run_id, None, None)


    async def _upload_reference_pressure_run_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, reference_pressure_run_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, reference_pressure_run_id, file_path, file_name)

            return await self._set_reference_pressure_run_attachment_server_state_to_completed(add_attached_file_response, reference_pressure_run_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, reference_pressure_run_id, file_path, file_name, message=e)


    async def add_attachment_to_reference_pressure_run(self, account_id: str, reference_pressure_run_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}ReferencePressureRuns/{reference_pressure_run_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, reference_pressure_run_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, reference_pressure_run_id, file_path, model.file_name)

        return await self._upload_reference_pressure_run_attachment(parsed_response, reference_pressure_run_id, file_path, model.file_name)


    async def retry_reference_pressure_run_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_reference_pressure_run_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_reference_pressure_run_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_reference_pressure_run_attachment(self, account_id: str, reference_pressure_run_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}ReferencePressureRuns/{reference_pressure_run_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_run_plan_by_id(self, account_id: str, run_plan_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}RunPlans/{run_plan_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_run_plans_for_session_car(self, account_id: str, session_id: str, car_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}RunPlans"

        param_lookup = dict()
        param_lookup["sessionId"] = session_id
        param_lookup["carId"] = car_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_run_plan(self, account_id: str, session_id: str, car_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}RunPlans?sessionId={session_id}&carId={car_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_run_plan(self, account_id: str, run_plan_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}RunPlans/{run_plan_id}", update_model)
        return response.ok


    async def delete_run_plan(self, account_id: str, run_plan_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}RunPlans/{run_plan_id}")
        return response.ok



    async def get_run_plan_attachments_by_id(self, account_id: str, run_plan_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}RunPlans/{run_plan_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}RunPlans/{run_plan_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_run_plan_attachments_by_name(self, account_id: str, run_plan_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}RunPlans/{run_plan_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_run_plan_attachment(self, account_id: str, run_plan_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}RunPlans/{run_plan_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_run_plan_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, run_plan_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_run_plan_attachment(
            add_attached_file_response.account_id,
            run_plan_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, run_plan_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, run_plan_id, None, None)


    async def _upload_run_plan_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, run_plan_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, run_plan_id, file_path, file_name)

            return await self._set_run_plan_attachment_server_state_to_completed(add_attached_file_response, run_plan_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, run_plan_id, file_path, file_name, message=e)


    async def add_attachment_to_run_plan(self, account_id: str, run_plan_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}RunPlans/{run_plan_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, run_plan_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, run_plan_id, file_path, model.file_name)

        return await self._upload_run_plan_attachment(parsed_response, run_plan_id, file_path, model.file_name)


    async def retry_run_plan_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_run_plan_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_run_plan_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_run_plan_attachment(self, account_id: str, run_plan_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}RunPlans/{run_plan_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_run_sheet_by_id(self, account_id: str, run_sheet_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}RunSheets/{run_sheet_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_run_sheets_for_session_car(self, account_id: str, session_id: str, car_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}RunSheets"

        param_lookup = dict()
        param_lookup["sessionId"] = session_id
        param_lookup["carId"] = car_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_run_sheet(self, account_id: str, session_id: str, car_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}RunSheets?sessionId={session_id}&carId={car_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_run_sheet(self, account_id: str, run_sheet_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}RunSheets/{run_sheet_id}", update_model)
        return response.ok


    async def delete_run_sheet(self, account_id: str, run_sheet_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}RunSheets/{run_sheet_id}")
        return response.ok



    async def get_run_sheet_attachments_by_id(self, account_id: str, run_sheet_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}RunSheets/{run_sheet_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}RunSheets/{run_sheet_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_run_sheet_attachments_by_name(self, account_id: str, run_sheet_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}RunSheets/{run_sheet_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_run_sheet_attachment(self, account_id: str, run_sheet_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}RunSheets/{run_sheet_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_run_sheet_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, run_sheet_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_run_sheet_attachment(
            add_attached_file_response.account_id,
            run_sheet_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, run_sheet_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, run_sheet_id, None, None)


    async def _upload_run_sheet_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, run_sheet_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, run_sheet_id, file_path, file_name)

            return await self._set_run_sheet_attachment_server_state_to_completed(add_attached_file_response, run_sheet_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, run_sheet_id, file_path, file_name, message=e)


    async def add_attachment_to_run_sheet(self, account_id: str, run_sheet_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}RunSheets/{run_sheet_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, run_sheet_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, run_sheet_id, file_path, model.file_name)

        return await self._upload_run_sheet_attachment(parsed_response, run_sheet_id, file_path, model.file_name)


    async def retry_run_sheet_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_run_sheet_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_run_sheet_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_run_sheet_attachment(self, account_id: str, run_sheet_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}RunSheets/{run_sheet_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_session_car_data_by_id(self, account_id: str, session_car_data_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}SessionCarDatas/{session_car_data_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_session_car_data_for_session_car(self, account_id: str, session_id: str, car_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}SessionCarDatas"

        param_lookup = dict()
        param_lookup["sessionId"] = session_id
        param_lookup["carId"] = car_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[Dict](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = response_json
        return ApiGetResult(response_object, True, None)

    async def update_session_car_data(self, account_id: str, session_car_data_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}SessionCarDatas/{session_car_data_id}", update_model)
        return response.ok


    async def get_session_car_data_attachments_by_id(self, account_id: str, session_car_data_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}SessionCarDatas/{session_car_data_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}SessionCarDatas/{session_car_data_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[Dict](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = response_json
        return ApiGetResult(response_object, True, None)


    async def get_session_car_data_attachments_by_name(self, account_id: str, session_car_data_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}SessionCarDatas/{session_car_data_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[Dict](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = response_json
        return ApiGetResult(response_object, True, None)


    async def update_session_car_data_attachment(self, account_id: str, session_car_data_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}SessionCarDatas/{session_car_data_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_session_car_data_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, session_car_data_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_session_car_data_attachment(
            add_attached_file_response.account_id,
            session_car_data_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, session_car_data_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, session_car_data_id, None, None)


    async def _upload_session_car_data_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, session_car_data_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, session_car_data_id, file_path, file_name)

            return await self._set_session_car_data_attachment_server_state_to_completed(add_attached_file_response, session_car_data_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, session_car_data_id, file_path, file_name, message=e)


    async def add_attachment_to_session_car_data(self, account_id: str, session_car_data_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}SessionCarDatas/{session_car_data_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, session_car_data_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, session_car_data_id, file_path, model.file_name)

        return await self._upload_session_car_data_attachment(parsed_response, session_car_data_id, file_path, model.file_name)


    async def retry_session_car_data_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_session_car_data_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_session_car_data_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_session_car_data_attachment(self, account_id: str, session_car_data_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}SessionCarDatas/{session_car_data_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_setup_by_id(self, account_id: str, setup_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}Setups/{setup_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_setups_for_event_car(self, account_id: str, event_id: str, car_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}Setups"

        param_lookup = dict()
        param_lookup["eventId"] = event_id
        param_lookup["carId"] = car_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_setup(self, account_id: str, event_id: str, car_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Setups?eventId={event_id}&carId={car_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_setup(self, account_id: str, setup_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Setups/{setup_id}", update_model)
        return response.ok


    async def delete_setup(self, account_id: str, setup_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Setups/{setup_id}")
        return response.ok



    async def get_setup_attachments_by_id(self, account_id: str, setup_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}Setups/{setup_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}Setups/{setup_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_setup_attachments_by_name(self, account_id: str, setup_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}Setups/{setup_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_setup_attachment(self, account_id: str, setup_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Setups/{setup_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_setup_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, setup_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_setup_attachment(
            add_attached_file_response.account_id,
            setup_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, setup_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, setup_id, None, None)


    async def _upload_setup_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, setup_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, setup_id, file_path, file_name)

            return await self._set_setup_attachment_server_state_to_completed(add_attached_file_response, setup_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, setup_id, file_path, file_name, message=e)


    async def add_attachment_to_setup(self, account_id: str, setup_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Setups/{setup_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, setup_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, setup_id, file_path, model.file_name)

        return await self._upload_setup_attachment(parsed_response, setup_id, file_path, model.file_name)


    async def retry_setup_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_setup_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_setup_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_setup_attachment(self, account_id: str, setup_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Setups/{setup_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_track_by_id(self, account_id: str, track_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}Tracks/{track_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_tracks(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}Tracks"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_track(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Tracks?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_track(self, account_id: str, track_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Tracks/{track_id}", update_model)
        return response.ok


    async def delete_track(self, account_id: str, track_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Tracks/{track_id}")
        return response.ok



    async def get_track_attachments_by_id(self, account_id: str, track_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}Tracks/{track_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}Tracks/{track_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_track_attachments_by_name(self, account_id: str, track_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}Tracks/{track_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_track_attachment(self, account_id: str, track_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Tracks/{track_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_track_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, track_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_track_attachment(
            add_attached_file_response.account_id,
            track_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, track_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, track_id, None, None)


    async def _upload_track_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, track_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, track_id, file_path, file_name)

            return await self._set_track_attachment_server_state_to_completed(add_attached_file_response, track_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, track_id, file_path, file_name, message=e)


    async def add_attachment_to_track(self, account_id: str, track_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Tracks/{track_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, track_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, track_id, file_path, model.file_name)

        return await self._upload_track_attachment(parsed_response, track_id, file_path, model.file_name)


    async def retry_track_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_track_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_track_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_track_attachment(self, account_id: str, track_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Tracks/{track_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_tyre_by_id(self, account_id: str, tyre_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}Tyres/{tyre_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def search_for_tyres(self, account_id: str, search_info: AssociatedModelSeachObject, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}Tyres/Search"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url, search_info)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_tyre(self, account_id: str, create_model: AssociationCreateModel, url_params: Dict[str, str]={}) -> Future[ApiGetResult[Dict]]:
        url_params["accountId"] = account_id
        response = await self.post_request(account_id, f"{self._api_endpoint}Tyres?{'&'.join(f'{k}={v}' for k, v in url_params.items())}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_tyre(self, account_id: str, tyre_id: str, update_model: AssociationUpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Tyres/{tyre_id}", update_model)
        return response.ok


    async def delete_tyre(self, account_id: str, tyre_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Tyres/{tyre_id}")
        return response.ok



    async def get_tyre_attachments_by_id(self, account_id: str, tyre_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}Tyres/{tyre_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}Tyres/{tyre_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_tyre_attachments_by_name(self, account_id: str, tyre_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}Tyres/{tyre_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_tyre_attachment(self, account_id: str, tyre_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Tyres/{tyre_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_tyre_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, tyre_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_tyre_attachment(
            add_attached_file_response.account_id,
            tyre_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, tyre_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, tyre_id, None, None)


    async def _upload_tyre_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, tyre_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, tyre_id, file_path, file_name)

            return await self._set_tyre_attachment_server_state_to_completed(add_attached_file_response, tyre_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, tyre_id, file_path, file_name, message=e)


    async def add_attachment_to_tyre(self, account_id: str, tyre_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Tyres/{tyre_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, tyre_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, tyre_id, file_path, model.file_name)

        return await self._upload_tyre_attachment(parsed_response, tyre_id, file_path, model.file_name)


    async def retry_tyre_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_tyre_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_tyre_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_tyre_attachment(self, account_id: str, tyre_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Tyres/{tyre_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_tyre_set_by_id(self, account_id: str, tyre_set_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}TyreSets/{tyre_set_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_tyre_sets_for_event_car(self, account_id: str, event_id: str, car_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}TyreSets"

        param_lookup = dict()
        param_lookup["eventId"] = event_id
        param_lookup["carId"] = car_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_tyre_set(self, account_id: str, event_id: str, car_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}TyreSets?eventId={event_id}&carId={car_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_tyre_set(self, account_id: str, tyre_set_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}TyreSets/{tyre_set_id}", update_model)
        return response.ok


    async def delete_tyre_set(self, account_id: str, tyre_set_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}TyreSets/{tyre_set_id}")
        return response.ok



    async def get_tyre_set_attachments_by_id(self, account_id: str, tyre_set_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}TyreSets/{tyre_set_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}TyreSets/{tyre_set_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_tyre_set_attachments_by_name(self, account_id: str, tyre_set_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}TyreSets/{tyre_set_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_tyre_set_attachment(self, account_id: str, tyre_set_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}TyreSets/{tyre_set_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_tyre_set_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, tyre_set_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_tyre_set_attachment(
            add_attached_file_response.account_id,
            tyre_set_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, tyre_set_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, tyre_set_id, None, None)


    async def _upload_tyre_set_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, tyre_set_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, tyre_set_id, file_path, file_name)

            return await self._set_tyre_set_attachment_server_state_to_completed(add_attached_file_response, tyre_set_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, tyre_set_id, file_path, file_name, message=e)


    async def add_attachment_to_tyre_set(self, account_id: str, tyre_set_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}TyreSets/{tyre_set_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, tyre_set_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, tyre_set_id, file_path, model.file_name)

        return await self._upload_tyre_set_attachment(parsed_response, tyre_set_id, file_path, model.file_name)


    async def retry_tyre_set_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_tyre_set_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_tyre_set_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_tyre_set_attachment(self, account_id: str, tyre_set_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}TyreSets/{tyre_set_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_tyre_set_pressure_adjustment_by_id(self, account_id: str, tyre_set_pressure_adjustment_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}TyreSetPressureAdjustments/{tyre_set_pressure_adjustment_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def add_tyre_set_pressure_adjustment(self, account_id: str, tyre_set_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}TyreSetPressureAdjustments?tyreSetId={tyre_set_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_tyre_set_pressure_adjustment(self, account_id: str, tyre_set_pressure_adjustment_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}TyreSetPressureAdjustments/{tyre_set_pressure_adjustment_id}", update_model)
        return response.ok


    async def delete_tyre_set_pressure_adjustment(self, account_id: str, tyre_set_pressure_adjustment_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}TyreSetPressureAdjustments/{tyre_set_pressure_adjustment_id}")
        return response.ok



    async def get_tyre_set_pressure_adjustment_attachments_by_id(self, account_id: str, tyre_set_pressure_adjustment_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}TyreSetPressureAdjustments/{tyre_set_pressure_adjustment_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}TyreSetPressureAdjustments/{tyre_set_pressure_adjustment_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_tyre_set_pressure_adjustment_attachments_by_name(self, account_id: str, tyre_set_pressure_adjustment_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}TyreSetPressureAdjustments/{tyre_set_pressure_adjustment_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_tyre_set_pressure_adjustment_attachment(self, account_id: str, tyre_set_pressure_adjustment_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}TyreSetPressureAdjustments/{tyre_set_pressure_adjustment_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_tyre_set_pressure_adjustment_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, tyre_set_pressure_adjustment_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_tyre_set_pressure_adjustment_attachment(
            add_attached_file_response.account_id,
            tyre_set_pressure_adjustment_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, tyre_set_pressure_adjustment_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, tyre_set_pressure_adjustment_id, None, None)


    async def _upload_tyre_set_pressure_adjustment_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, tyre_set_pressure_adjustment_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, tyre_set_pressure_adjustment_id, file_path, file_name)

            return await self._set_tyre_set_pressure_adjustment_attachment_server_state_to_completed(add_attached_file_response, tyre_set_pressure_adjustment_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, tyre_set_pressure_adjustment_id, file_path, file_name, message=e)


    async def add_attachment_to_tyre_set_pressure_adjustment(self, account_id: str, tyre_set_pressure_adjustment_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}TyreSetPressureAdjustments/{tyre_set_pressure_adjustment_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, tyre_set_pressure_adjustment_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, tyre_set_pressure_adjustment_id, file_path, model.file_name)

        return await self._upload_tyre_set_pressure_adjustment_attachment(parsed_response, tyre_set_pressure_adjustment_id, file_path, model.file_name)


    async def retry_tyre_set_pressure_adjustment_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_tyre_set_pressure_adjustment_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_tyre_set_pressure_adjustment_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_tyre_set_pressure_adjustment_attachment(self, account_id: str, tyre_set_pressure_adjustment_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}TyreSetPressureAdjustments/{tyre_set_pressure_adjustment_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_tyre_specification_by_id(self, account_id: str, tyre_specification_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}TyreSpecifications/{tyre_specification_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_tyre_specifications(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}TyreSpecifications"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_tyre_specification(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}TyreSpecifications?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_tyre_specification(self, account_id: str, tyre_specification_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}TyreSpecifications/{tyre_specification_id}", update_model)
        return response.ok


    async def delete_tyre_specification(self, account_id: str, tyre_specification_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}TyreSpecifications/{tyre_specification_id}")
        return response.ok



    async def get_tyre_specification_attachments_by_id(self, account_id: str, tyre_specification_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}TyreSpecifications/{tyre_specification_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}TyreSpecifications/{tyre_specification_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_tyre_specification_attachments_by_name(self, account_id: str, tyre_specification_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}TyreSpecifications/{tyre_specification_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_tyre_specification_attachment(self, account_id: str, tyre_specification_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}TyreSpecifications/{tyre_specification_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_tyre_specification_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, tyre_specification_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_tyre_specification_attachment(
            add_attached_file_response.account_id,
            tyre_specification_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, tyre_specification_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, tyre_specification_id, None, None)


    async def _upload_tyre_specification_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, tyre_specification_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, tyre_specification_id, file_path, file_name)

            return await self._set_tyre_specification_attachment_server_state_to_completed(add_attached_file_response, tyre_specification_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, tyre_specification_id, file_path, file_name, message=e)


    async def add_attachment_to_tyre_specification(self, account_id: str, tyre_specification_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}TyreSpecifications/{tyre_specification_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, tyre_specification_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, tyre_specification_id, file_path, model.file_name)

        return await self._upload_tyre_specification_attachment(parsed_response, tyre_specification_id, file_path, model.file_name)


    async def retry_tyre_specification_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_tyre_specification_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_tyre_specification_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_tyre_specification_attachment(self, account_id: str, tyre_specification_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}TyreSpecifications/{tyre_specification_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_tyre_wear_sheet_by_id(self, account_id: str, tyre_wear_sheet_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}TyreWearSheets/{tyre_wear_sheet_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_tyre_wear_sheets_for_event_car(self, account_id: str, event_id: str, car_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}TyreWearSheets"

        param_lookup = dict()
        param_lookup["eventId"] = event_id
        param_lookup["carId"] = car_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_tyre_wear_sheet(self, account_id: str, event_id: str, car_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}TyreWearSheets?eventId={event_id}&carId={car_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_tyre_wear_sheet(self, account_id: str, tyre_wear_sheet_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}TyreWearSheets/{tyre_wear_sheet_id}", update_model)
        return response.ok


    async def delete_tyre_wear_sheet(self, account_id: str, tyre_wear_sheet_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}TyreWearSheets/{tyre_wear_sheet_id}")
        return response.ok



    async def get_tyre_wear_sheet_attachments_by_id(self, account_id: str, tyre_wear_sheet_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}TyreWearSheets/{tyre_wear_sheet_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}TyreWearSheets/{tyre_wear_sheet_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_tyre_wear_sheet_attachments_by_name(self, account_id: str, tyre_wear_sheet_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}TyreWearSheets/{tyre_wear_sheet_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_tyre_wear_sheet_attachment(self, account_id: str, tyre_wear_sheet_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}TyreWearSheets/{tyre_wear_sheet_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_tyre_wear_sheet_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, tyre_wear_sheet_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_tyre_wear_sheet_attachment(
            add_attached_file_response.account_id,
            tyre_wear_sheet_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, tyre_wear_sheet_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, tyre_wear_sheet_id, None, None)


    async def _upload_tyre_wear_sheet_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, tyre_wear_sheet_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, tyre_wear_sheet_id, file_path, file_name)

            return await self._set_tyre_wear_sheet_attachment_server_state_to_completed(add_attached_file_response, tyre_wear_sheet_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, tyre_wear_sheet_id, file_path, file_name, message=e)


    async def add_attachment_to_tyre_wear_sheet(self, account_id: str, tyre_wear_sheet_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}TyreWearSheets/{tyre_wear_sheet_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, tyre_wear_sheet_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, tyre_wear_sheet_id, file_path, model.file_name)

        return await self._upload_tyre_wear_sheet_attachment(parsed_response, tyre_wear_sheet_id, file_path, model.file_name)


    async def retry_tyre_wear_sheet_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_tyre_wear_sheet_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_tyre_wear_sheet_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_tyre_wear_sheet_attachment(self, account_id: str, tyre_wear_sheet_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}TyreWearSheets/{tyre_wear_sheet_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_account_options_by_id(self, account_id: str, account_options_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}AccountOptions/{account_options_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_account_options(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}AccountOptions"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_account_options(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}AccountOptions?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_account_options(self, account_id: str, account_options_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}AccountOptions/{account_options_id}", update_model)
        return response.ok


    async def get_account_options_attachments_by_id(self, account_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}AccountOptions/{account_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}AccountOptions/{account_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_account_options_attachments_by_name(self, account_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}AccountOptions/{account_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_account_options_attachment(self, account_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}AccountOptions/{account_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_account_options_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_account_options_attachment(
            add_attached_file_response.account_id,
            "",
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, add_attached_file_response.account_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, add_attached_file_response.account_id, None, None)


    async def _upload_account_options_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, add_attached_file_response.account_id, file_path, file_name)

            return await self._set_account_options_attachment_server_state_to_completed(add_attached_file_response)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, add_attached_file_response.account_id, file_path, file_name, message=e)


    async def add_attachment_to_account_options(self, account_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}AccountOptions/{account_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, file_path, model.file_name)

        return await self._upload_account_options_attachment(parsed_response, file_path, model.file_name)


    async def retry_account_options_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_account_options_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_account_options_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_account_options_attachment(self, account_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}AccountOptions/{account_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_driver_by_id(self, account_id: str, driver_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}Drivers/{driver_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_drivers(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}Drivers"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_driver(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Drivers?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_driver(self, account_id: str, driver_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Drivers/{driver_id}", update_model)
        return response.ok


    async def delete_driver(self, account_id: str, driver_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Drivers/{driver_id}")
        return response.ok



    async def get_driver_attachments_by_id(self, account_id: str, driver_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}Drivers/{driver_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}Drivers/{driver_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_driver_attachments_by_name(self, account_id: str, driver_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}Drivers/{driver_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_driver_attachment(self, account_id: str, driver_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Drivers/{driver_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_driver_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, driver_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_driver_attachment(
            add_attached_file_response.account_id,
            driver_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, driver_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, driver_id, None, None)


    async def _upload_driver_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, driver_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, driver_id, file_path, file_name)

            return await self._set_driver_attachment_server_state_to_completed(add_attached_file_response, driver_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, driver_id, file_path, file_name, message=e)


    async def add_attachment_to_driver(self, account_id: str, driver_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Drivers/{driver_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, driver_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, driver_id, file_path, model.file_name)

        return await self._upload_driver_attachment(parsed_response, driver_id, file_path, model.file_name)


    async def retry_driver_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_driver_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_driver_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_driver_attachment(self, account_id: str, driver_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Drivers/{driver_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_lap_sector_by_id(self, account_id: str, lap_sector_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}LapSectors/{lap_sector_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def update_lap_sector(self, account_id: str, lap_sector_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}LapSectors/{lap_sector_id}", update_model)
        return response.ok


    async def get_lap_sector_attachments_by_id(self, account_id: str, lap_sector_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}LapSectors/{lap_sector_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}LapSectors/{lap_sector_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_lap_sector_attachments_by_name(self, account_id: str, lap_sector_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}LapSectors/{lap_sector_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_lap_sector_attachment(self, account_id: str, lap_sector_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}LapSectors/{lap_sector_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_lap_sector_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, lap_sector_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_lap_sector_attachment(
            add_attached_file_response.account_id,
            lap_sector_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, lap_sector_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, lap_sector_id, None, None)


    async def _upload_lap_sector_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, lap_sector_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, lap_sector_id, file_path, file_name)

            return await self._set_lap_sector_attachment_server_state_to_completed(add_attached_file_response, lap_sector_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, lap_sector_id, file_path, file_name, message=e)


    async def add_attachment_to_lap_sector(self, account_id: str, lap_sector_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}LapSectors/{lap_sector_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, lap_sector_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, lap_sector_id, file_path, model.file_name)

        return await self._upload_lap_sector_attachment(parsed_response, lap_sector_id, file_path, model.file_name)


    async def retry_lap_sector_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_lap_sector_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_lap_sector_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_lap_sector_attachment(self, account_id: str, lap_sector_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}LapSectors/{lap_sector_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_car_manufacturer_by_id(self, account_id: str, car_manufacturer_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}CarManufacturers/{car_manufacturer_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_car_manufacturers(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}CarManufacturers"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_car_manufacturer(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}CarManufacturers?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_car_manufacturer(self, account_id: str, car_manufacturer_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}CarManufacturers/{car_manufacturer_id}", update_model)
        return response.ok


    async def delete_car_manufacturer(self, account_id: str, car_manufacturer_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}CarManufacturers/{car_manufacturer_id}")
        return response.ok



    async def get_car_manufacturer_attachments_by_id(self, account_id: str, car_manufacturer_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}CarManufacturers/{car_manufacturer_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}CarManufacturers/{car_manufacturer_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_car_manufacturer_attachments_by_name(self, account_id: str, car_manufacturer_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}CarManufacturers/{car_manufacturer_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_car_manufacturer_attachment(self, account_id: str, car_manufacturer_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}CarManufacturers/{car_manufacturer_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_car_manufacturer_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, car_manufacturer_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_car_manufacturer_attachment(
            add_attached_file_response.account_id,
            car_manufacturer_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, car_manufacturer_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, car_manufacturer_id, None, None)


    async def _upload_car_manufacturer_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, car_manufacturer_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, car_manufacturer_id, file_path, file_name)

            return await self._set_car_manufacturer_attachment_server_state_to_completed(add_attached_file_response, car_manufacturer_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, car_manufacturer_id, file_path, file_name, message=e)


    async def add_attachment_to_car_manufacturer(self, account_id: str, car_manufacturer_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}CarManufacturers/{car_manufacturer_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, car_manufacturer_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, car_manufacturer_id, file_path, model.file_name)

        return await self._upload_car_manufacturer_attachment(parsed_response, car_manufacturer_id, file_path, model.file_name)


    async def retry_car_manufacturer_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_car_manufacturer_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_car_manufacturer_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_car_manufacturer_attachment(self, account_id: str, car_manufacturer_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}CarManufacturers/{car_manufacturer_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_car_model_by_id(self, account_id: str, car_model_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}CarModels/{car_model_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def add_car_model(self, account_id: str, car_manufacturer_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}CarModels?carManufacturerId={car_manufacturer_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_car_model(self, account_id: str, car_model_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}CarModels/{car_model_id}", update_model)
        return response.ok


    async def delete_car_model(self, account_id: str, car_model_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}CarModels/{car_model_id}")
        return response.ok



    async def get_car_model_attachments_by_id(self, account_id: str, car_model_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}CarModels/{car_model_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}CarModels/{car_model_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_car_model_attachments_by_name(self, account_id: str, car_model_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}CarModels/{car_model_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_car_model_attachment(self, account_id: str, car_model_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}CarModels/{car_model_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_car_model_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, car_model_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_car_model_attachment(
            add_attached_file_response.account_id,
            car_model_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, car_model_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, car_model_id, None, None)


    async def _upload_car_model_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, car_model_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, car_model_id, file_path, file_name)

            return await self._set_car_model_attachment_server_state_to_completed(add_attached_file_response, car_model_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, car_model_id, file_path, file_name, message=e)


    async def add_attachment_to_car_model(self, account_id: str, car_model_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}CarModels/{car_model_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, car_model_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, car_model_id, file_path, model.file_name)

        return await self._upload_car_model_attachment(parsed_response, car_model_id, file_path, model.file_name)


    async def retry_car_model_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_car_model_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_car_model_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_car_model_attachment(self, account_id: str, car_model_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}CarModels/{car_model_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_category_by_id(self, account_id: str, category_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}Categories/{category_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_categories(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}Categories"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_category(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Categories?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_category(self, account_id: str, category_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Categories/{category_id}", update_model)
        return response.ok


    async def delete_category(self, account_id: str, category_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Categories/{category_id}")
        return response.ok



    async def get_category_attachments_by_id(self, account_id: str, category_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}Categories/{category_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}Categories/{category_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_category_attachments_by_name(self, account_id: str, category_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}Categories/{category_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_category_attachment(self, account_id: str, category_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Categories/{category_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_category_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, category_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_category_attachment(
            add_attached_file_response.account_id,
            category_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, category_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, category_id, None, None)


    async def _upload_category_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, category_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, category_id, file_path, file_name)

            return await self._set_category_attachment_server_state_to_completed(add_attached_file_response, category_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, category_id, file_path, file_name, message=e)


    async def add_attachment_to_category(self, account_id: str, category_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Categories/{category_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, category_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, category_id, file_path, model.file_name)

        return await self._upload_category_attachment(parsed_response, category_id, file_path, model.file_name)


    async def retry_category_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_category_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_category_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_category_attachment(self, account_id: str, category_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Categories/{category_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_issue_list_category_by_id(self, account_id: str, issue_list_category_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}IssueListCategories/{issue_list_category_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_issue_list_categories(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}IssueListCategories"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_issue_list_category(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}IssueListCategories?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_issue_list_category(self, account_id: str, issue_list_category_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}IssueListCategories/{issue_list_category_id}", update_model)
        return response.ok


    async def delete_issue_list_category(self, account_id: str, issue_list_category_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}IssueListCategories/{issue_list_category_id}")
        return response.ok



    async def get_issue_list_category_attachments_by_id(self, account_id: str, issue_list_category_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}IssueListCategories/{issue_list_category_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}IssueListCategories/{issue_list_category_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_issue_list_category_attachments_by_name(self, account_id: str, issue_list_category_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}IssueListCategories/{issue_list_category_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_issue_list_category_attachment(self, account_id: str, issue_list_category_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}IssueListCategories/{issue_list_category_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_issue_list_category_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, issue_list_category_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_issue_list_category_attachment(
            add_attached_file_response.account_id,
            issue_list_category_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, issue_list_category_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, issue_list_category_id, None, None)


    async def _upload_issue_list_category_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, issue_list_category_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, issue_list_category_id, file_path, file_name)

            return await self._set_issue_list_category_attachment_server_state_to_completed(add_attached_file_response, issue_list_category_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, issue_list_category_id, file_path, file_name, message=e)


    async def add_attachment_to_issue_list_category(self, account_id: str, issue_list_category_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}IssueListCategories/{issue_list_category_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, issue_list_category_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, issue_list_category_id, file_path, model.file_name)

        return await self._upload_issue_list_category_attachment(parsed_response, issue_list_category_id, file_path, model.file_name)


    async def retry_issue_list_category_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_issue_list_category_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_issue_list_category_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_issue_list_category_attachment(self, account_id: str, issue_list_category_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}IssueListCategories/{issue_list_category_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_job_list_category_by_id(self, account_id: str, job_list_category_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}JobListCategories/{job_list_category_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_job_list_categories(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}JobListCategories"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_job_list_category(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}JobListCategories?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_job_list_category(self, account_id: str, job_list_category_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}JobListCategories/{job_list_category_id}", update_model)
        return response.ok


    async def delete_job_list_category(self, account_id: str, job_list_category_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}JobListCategories/{job_list_category_id}")
        return response.ok



    async def get_job_list_category_attachments_by_id(self, account_id: str, job_list_category_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}JobListCategories/{job_list_category_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}JobListCategories/{job_list_category_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_job_list_category_attachments_by_name(self, account_id: str, job_list_category_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}JobListCategories/{job_list_category_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_job_list_category_attachment(self, account_id: str, job_list_category_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}JobListCategories/{job_list_category_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_job_list_category_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, job_list_category_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_job_list_category_attachment(
            add_attached_file_response.account_id,
            job_list_category_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, job_list_category_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, job_list_category_id, None, None)


    async def _upload_job_list_category_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, job_list_category_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, job_list_category_id, file_path, file_name)

            return await self._set_job_list_category_attachment_server_state_to_completed(add_attached_file_response, job_list_category_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, job_list_category_id, file_path, file_name, message=e)


    async def add_attachment_to_job_list_category(self, account_id: str, job_list_category_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}JobListCategories/{job_list_category_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, job_list_category_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, job_list_category_id, file_path, model.file_name)

        return await self._upload_job_list_category_attachment(parsed_response, job_list_category_id, file_path, model.file_name)


    async def retry_job_list_category_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_job_list_category_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_job_list_category_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_job_list_category_attachment(self, account_id: str, job_list_category_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}JobListCategories/{job_list_category_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_job_list_template_by_id(self, account_id: str, job_list_template_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}JobListTemplates/{job_list_template_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_job_list_templates(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}JobListTemplates"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_job_list_template(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}JobListTemplates?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_job_list_template(self, account_id: str, job_list_template_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}JobListTemplates/{job_list_template_id}", update_model)
        return response.ok


    async def delete_job_list_template(self, account_id: str, job_list_template_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}JobListTemplates/{job_list_template_id}")
        return response.ok



    async def get_job_list_template_attachments_by_id(self, account_id: str, job_list_template_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}JobListTemplates/{job_list_template_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}JobListTemplates/{job_list_template_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_job_list_template_attachments_by_name(self, account_id: str, job_list_template_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}JobListTemplates/{job_list_template_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_job_list_template_attachment(self, account_id: str, job_list_template_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}JobListTemplates/{job_list_template_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_job_list_template_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, job_list_template_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_job_list_template_attachment(
            add_attached_file_response.account_id,
            job_list_template_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, job_list_template_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, job_list_template_id, None, None)


    async def _upload_job_list_template_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, job_list_template_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, job_list_template_id, file_path, file_name)

            return await self._set_job_list_template_attachment_server_state_to_completed(add_attached_file_response, job_list_template_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, job_list_template_id, file_path, file_name, message=e)


    async def add_attachment_to_job_list_template(self, account_id: str, job_list_template_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}JobListTemplates/{job_list_template_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, job_list_template_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, job_list_template_id, file_path, model.file_name)

        return await self._upload_job_list_template_attachment(parsed_response, job_list_template_id, file_path, model.file_name)


    async def retry_job_list_template_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_job_list_template_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_job_list_template_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_job_list_template_attachment(self, account_id: str, job_list_template_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}JobListTemplates/{job_list_template_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_job_list_template_item_by_id(self, account_id: str, job_list_template_item_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}JobListTemplateItems/{job_list_template_item_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def add_job_list_template_item(self, account_id: str, job_list_template_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}JobListTemplateItems?jobListTemplateId={job_list_template_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_job_list_template_item(self, account_id: str, job_list_template_item_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}JobListTemplateItems/{job_list_template_item_id}", update_model)
        return response.ok


    async def delete_job_list_template_item(self, account_id: str, job_list_template_item_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}JobListTemplateItems/{job_list_template_item_id}")
        return response.ok



    async def get_job_list_template_item_attachments_by_id(self, account_id: str, job_list_template_item_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}JobListTemplateItems/{job_list_template_item_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}JobListTemplateItems/{job_list_template_item_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_job_list_template_item_attachments_by_name(self, account_id: str, job_list_template_item_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}JobListTemplateItems/{job_list_template_item_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_job_list_template_item_attachment(self, account_id: str, job_list_template_item_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}JobListTemplateItems/{job_list_template_item_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_job_list_template_item_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, job_list_template_item_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_job_list_template_item_attachment(
            add_attached_file_response.account_id,
            job_list_template_item_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, job_list_template_item_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, job_list_template_item_id, None, None)


    async def _upload_job_list_template_item_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, job_list_template_item_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, job_list_template_item_id, file_path, file_name)

            return await self._set_job_list_template_item_attachment_server_state_to_completed(add_attached_file_response, job_list_template_item_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, job_list_template_item_id, file_path, file_name, message=e)


    async def add_attachment_to_job_list_template_item(self, account_id: str, job_list_template_item_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}JobListTemplateItems/{job_list_template_item_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, job_list_template_item_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, job_list_template_item_id, file_path, model.file_name)

        return await self._upload_job_list_template_item_attachment(parsed_response, job_list_template_item_id, file_path, model.file_name)


    async def retry_job_list_template_item_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_job_list_template_item_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_job_list_template_item_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_job_list_template_item_attachment(self, account_id: str, job_list_template_item_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}JobListTemplateItems/{job_list_template_item_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_session_by_id(self, account_id: str, session_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}Sessions/{session_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def add_session(self, account_id: str, event_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Sessions?eventId={event_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_session(self, account_id: str, session_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Sessions/{session_id}", update_model)
        return response.ok


    async def delete_session(self, account_id: str, session_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Sessions/{session_id}")
        return response.ok



    async def get_session_attachments_by_id(self, account_id: str, session_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}Sessions/{session_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}Sessions/{session_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_session_attachments_by_name(self, account_id: str, session_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}Sessions/{session_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_session_attachment(self, account_id: str, session_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Sessions/{session_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_session_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, session_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_session_attachment(
            add_attached_file_response.account_id,
            session_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, session_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, session_id, None, None)


    async def _upload_session_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, session_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, session_id, file_path, file_name)

            return await self._set_session_attachment_server_state_to_completed(add_attached_file_response, session_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, session_id, file_path, file_name, message=e)


    async def add_attachment_to_session(self, account_id: str, session_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Sessions/{session_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, session_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, session_id, file_path, model.file_name)

        return await self._upload_session_attachment(parsed_response, session_id, file_path, model.file_name)


    async def retry_session_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_session_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_session_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_session_attachment(self, account_id: str, session_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Sessions/{session_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_team_by_id(self, account_id: str, team_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}Teams/{team_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_teams(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}Teams"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_team(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Teams?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_team(self, account_id: str, team_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Teams/{team_id}", update_model)
        return response.ok


    async def delete_team(self, account_id: str, team_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Teams/{team_id}")
        return response.ok



    async def get_team_attachments_by_id(self, account_id: str, team_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}Teams/{team_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}Teams/{team_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_team_attachments_by_name(self, account_id: str, team_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}Teams/{team_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_team_attachment(self, account_id: str, team_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}Teams/{team_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_team_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, team_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_team_attachment(
            add_attached_file_response.account_id,
            team_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, team_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, team_id, None, None)


    async def _upload_team_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, team_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, team_id, file_path, file_name)

            return await self._set_team_attachment_server_state_to_completed(add_attached_file_response, team_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, team_id, file_path, file_name, message=e)


    async def add_attachment_to_team(self, account_id: str, team_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}Teams/{team_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, team_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, team_id, file_path, model.file_name)

        return await self._upload_team_attachment(parsed_response, team_id, file_path, model.file_name)


    async def retry_team_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_team_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_team_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_team_attachment(self, account_id: str, team_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}Teams/{team_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_track_sector_definition_by_id(self, account_id: str, track_sector_definition_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}TrackSectorDefinitions/{track_sector_definition_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def add_track_sector_definition(self, account_id: str, track_configuration_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}TrackSectorDefinitions?trackConfigurationId={track_configuration_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_track_sector_definition(self, account_id: str, track_sector_definition_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}TrackSectorDefinitions/{track_sector_definition_id}", update_model)
        return response.ok


    async def delete_track_sector_definition(self, account_id: str, track_sector_definition_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}TrackSectorDefinitions/{track_sector_definition_id}")
        return response.ok



    async def get_session_object_issue_by_id(self, account_id: str, session_object_issue_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}SessionObjectIssues/{session_object_issue_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_session_object_issues_for_session_car(self, account_id: str, session_id: str, car_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}SessionObjectIssues"

        param_lookup = dict()
        param_lookup["sessionId"] = session_id
        param_lookup["carId"] = car_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_session_object_issue(self, account_id: str, session_id: str, car_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}SessionObjectIssues?sessionId={session_id}&carId={car_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_session_object_issue(self, account_id: str, session_object_issue_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}SessionObjectIssues/{session_object_issue_id}", update_model)
        return response.ok


    async def delete_session_object_issue(self, account_id: str, session_object_issue_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}SessionObjectIssues/{session_object_issue_id}")
        return response.ok



    async def get_session_object_issue_attachments_by_id(self, account_id: str, session_object_issue_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}SessionObjectIssues/{session_object_issue_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}SessionObjectIssues/{session_object_issue_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_session_object_issue_attachments_by_name(self, account_id: str, session_object_issue_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}SessionObjectIssues/{session_object_issue_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_session_object_issue_attachment(self, account_id: str, session_object_issue_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}SessionObjectIssues/{session_object_issue_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_session_object_issue_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, session_object_issue_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_session_object_issue_attachment(
            add_attached_file_response.account_id,
            session_object_issue_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, session_object_issue_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, session_object_issue_id, None, None)


    async def _upload_session_object_issue_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, session_object_issue_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, session_object_issue_id, file_path, file_name)

            return await self._set_session_object_issue_attachment_server_state_to_completed(add_attached_file_response, session_object_issue_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, session_object_issue_id, file_path, file_name, message=e)


    async def add_attachment_to_session_object_issue(self, account_id: str, session_object_issue_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}SessionObjectIssues/{session_object_issue_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, session_object_issue_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, session_object_issue_id, file_path, model.file_name)

        return await self._upload_session_object_issue_attachment(parsed_response, session_object_issue_id, file_path, model.file_name)


    async def retry_session_object_issue_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_session_object_issue_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_session_object_issue_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_session_object_issue_attachment(self, account_id: str, session_object_issue_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}SessionObjectIssues/{session_object_issue_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_session_object_job_by_id(self, account_id: str, session_object_job_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}SessionObjectJobs/{session_object_job_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_session_object_jobs_for_session_car(self, account_id: str, session_id: str, car_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}SessionObjectJobs"

        param_lookup = dict()
        param_lookup["sessionId"] = session_id
        param_lookup["carId"] = car_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_session_object_job(self, account_id: str, session_id: str, car_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}SessionObjectJobs?sessionId={session_id}&carId={car_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_session_object_job(self, account_id: str, session_object_job_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}SessionObjectJobs/{session_object_job_id}", update_model)
        return response.ok


    async def delete_session_object_job(self, account_id: str, session_object_job_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}SessionObjectJobs/{session_object_job_id}")
        return response.ok



    async def get_session_object_job_attachments_by_id(self, account_id: str, session_object_job_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}SessionObjectJobs/{session_object_job_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}SessionObjectJobs/{session_object_job_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_session_object_job_attachments_by_name(self, account_id: str, session_object_job_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}SessionObjectJobs/{session_object_job_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_session_object_job_attachment(self, account_id: str, session_object_job_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}SessionObjectJobs/{session_object_job_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_session_object_job_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, session_object_job_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_session_object_job_attachment(
            add_attached_file_response.account_id,
            session_object_job_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, session_object_job_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, session_object_job_id, None, None)


    async def _upload_session_object_job_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, session_object_job_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, session_object_job_id, file_path, file_name)

            return await self._set_session_object_job_attachment_server_state_to_completed(add_attached_file_response, session_object_job_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, session_object_job_id, file_path, file_name, message=e)


    async def add_attachment_to_session_object_job(self, account_id: str, session_object_job_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}SessionObjectJobs/{session_object_job_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, session_object_job_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, session_object_job_id, file_path, model.file_name)

        return await self._upload_session_object_job_attachment(parsed_response, session_object_job_id, file_path, model.file_name)


    async def retry_session_object_job_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_session_object_job_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_session_object_job_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_session_object_job_attachment(self, account_id: str, session_object_job_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}SessionObjectJobs/{session_object_job_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_data_analysis_profile_by_id(self, account_id: str, data_analysis_profile_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}DataAnalysisProfiles/{data_analysis_profile_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_data_analysis_profiles(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}DataAnalysisProfiles"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_data_analysis_profile(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}DataAnalysisProfiles?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_data_analysis_profile(self, account_id: str, data_analysis_profile_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}DataAnalysisProfiles/{data_analysis_profile_id}", update_model)
        return response.ok


    async def delete_data_analysis_profile(self, account_id: str, data_analysis_profile_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}DataAnalysisProfiles/{data_analysis_profile_id}")
        return response.ok



    async def get_brake_disc_specification_by_id(self, account_id: str, brake_disc_specification_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}BrakeDiscSpecifications/{brake_disc_specification_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_brake_disc_specifications(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}BrakeDiscSpecifications"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_brake_disc_specification(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}BrakeDiscSpecifications?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_brake_disc_specification(self, account_id: str, brake_disc_specification_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}BrakeDiscSpecifications/{brake_disc_specification_id}", update_model)
        return response.ok


    async def delete_brake_disc_specification(self, account_id: str, brake_disc_specification_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}BrakeDiscSpecifications/{brake_disc_specification_id}")
        return response.ok



    async def get_brake_disc_specification_attachments_by_id(self, account_id: str, brake_disc_specification_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}BrakeDiscSpecifications/{brake_disc_specification_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}BrakeDiscSpecifications/{brake_disc_specification_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_brake_disc_specification_attachments_by_name(self, account_id: str, brake_disc_specification_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}BrakeDiscSpecifications/{brake_disc_specification_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_brake_disc_specification_attachment(self, account_id: str, brake_disc_specification_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}BrakeDiscSpecifications/{brake_disc_specification_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_brake_disc_specification_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, brake_disc_specification_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_brake_disc_specification_attachment(
            add_attached_file_response.account_id,
            brake_disc_specification_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, brake_disc_specification_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, brake_disc_specification_id, None, None)


    async def _upload_brake_disc_specification_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, brake_disc_specification_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, brake_disc_specification_id, file_path, file_name)

            return await self._set_brake_disc_specification_attachment_server_state_to_completed(add_attached_file_response, brake_disc_specification_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, brake_disc_specification_id, file_path, file_name, message=e)


    async def add_attachment_to_brake_disc_specification(self, account_id: str, brake_disc_specification_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}BrakeDiscSpecifications/{brake_disc_specification_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, brake_disc_specification_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, brake_disc_specification_id, file_path, model.file_name)

        return await self._upload_brake_disc_specification_attachment(parsed_response, brake_disc_specification_id, file_path, model.file_name)


    async def retry_brake_disc_specification_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_brake_disc_specification_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_brake_disc_specification_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_brake_disc_specification_attachment(self, account_id: str, brake_disc_specification_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}BrakeDiscSpecifications/{brake_disc_specification_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_brake_pad_specification_by_id(self, account_id: str, brake_pad_specification_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}BrakePadSpecifications/{brake_pad_specification_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_brake_pad_specifications(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}BrakePadSpecifications"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_brake_pad_specification(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}BrakePadSpecifications?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_brake_pad_specification(self, account_id: str, brake_pad_specification_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}BrakePadSpecifications/{brake_pad_specification_id}", update_model)
        return response.ok


    async def delete_brake_pad_specification(self, account_id: str, brake_pad_specification_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}BrakePadSpecifications/{brake_pad_specification_id}")
        return response.ok



    async def get_brake_pad_specification_attachments_by_id(self, account_id: str, brake_pad_specification_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}BrakePadSpecifications/{brake_pad_specification_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}BrakePadSpecifications/{brake_pad_specification_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_brake_pad_specification_attachments_by_name(self, account_id: str, brake_pad_specification_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}BrakePadSpecifications/{brake_pad_specification_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_brake_pad_specification_attachment(self, account_id: str, brake_pad_specification_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}BrakePadSpecifications/{brake_pad_specification_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_brake_pad_specification_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, brake_pad_specification_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_brake_pad_specification_attachment(
            add_attached_file_response.account_id,
            brake_pad_specification_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, brake_pad_specification_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, brake_pad_specification_id, None, None)


    async def _upload_brake_pad_specification_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, brake_pad_specification_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, brake_pad_specification_id, file_path, file_name)

            return await self._set_brake_pad_specification_attachment_server_state_to_completed(add_attached_file_response, brake_pad_specification_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, brake_pad_specification_id, file_path, file_name, message=e)


    async def add_attachment_to_brake_pad_specification(self, account_id: str, brake_pad_specification_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}BrakePadSpecifications/{brake_pad_specification_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, brake_pad_specification_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, brake_pad_specification_id, file_path, model.file_name)

        return await self._upload_brake_pad_specification_attachment(parsed_response, brake_pad_specification_id, file_path, model.file_name)


    async def retry_brake_pad_specification_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_brake_pad_specification_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_brake_pad_specification_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_brake_pad_specification_attachment(self, account_id: str, brake_pad_specification_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}BrakePadSpecifications/{brake_pad_specification_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_brake_disc_by_id(self, account_id: str, brake_disc_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}BrakeDiscs/{brake_disc_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def search_for_brake_discs(self, account_id: str, search_info: AssociatedModelSeachObject, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}BrakeDiscs/Search"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url, search_info)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_brake_disc(self, account_id: str, create_model: AssociationCreateModel, url_params: Dict[str, str]={}) -> Future[ApiGetResult[Dict]]:
        url_params["accountId"] = account_id
        response = await self.post_request(account_id, f"{self._api_endpoint}BrakeDiscs?{'&'.join(f'{k}={v}' for k, v in url_params.items())}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_brake_disc(self, account_id: str, brake_disc_id: str, update_model: AssociationUpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}BrakeDiscs/{brake_disc_id}", update_model)
        return response.ok


    async def delete_brake_disc(self, account_id: str, brake_disc_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}BrakeDiscs/{brake_disc_id}")
        return response.ok



    async def get_brake_disc_attachments_by_id(self, account_id: str, brake_disc_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}BrakeDiscs/{brake_disc_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}BrakeDiscs/{brake_disc_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_brake_disc_attachments_by_name(self, account_id: str, brake_disc_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}BrakeDiscs/{brake_disc_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_brake_disc_attachment(self, account_id: str, brake_disc_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}BrakeDiscs/{brake_disc_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_brake_disc_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, brake_disc_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_brake_disc_attachment(
            add_attached_file_response.account_id,
            brake_disc_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, brake_disc_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, brake_disc_id, None, None)


    async def _upload_brake_disc_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, brake_disc_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, brake_disc_id, file_path, file_name)

            return await self._set_brake_disc_attachment_server_state_to_completed(add_attached_file_response, brake_disc_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, brake_disc_id, file_path, file_name, message=e)


    async def add_attachment_to_brake_disc(self, account_id: str, brake_disc_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}BrakeDiscs/{brake_disc_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, brake_disc_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, brake_disc_id, file_path, model.file_name)

        return await self._upload_brake_disc_attachment(parsed_response, brake_disc_id, file_path, model.file_name)


    async def retry_brake_disc_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_brake_disc_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_brake_disc_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_brake_disc_attachment(self, account_id: str, brake_disc_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}BrakeDiscs/{brake_disc_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_brake_pad_by_id(self, account_id: str, brake_pad_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}BrakePads/{brake_pad_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def search_for_brake_pads(self, account_id: str, search_info: AssociatedModelSeachObject, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}BrakePads/Search"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url, search_info)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_brake_pad(self, account_id: str, create_model: AssociationCreateModel, url_params: Dict[str, str]={}) -> Future[ApiGetResult[Dict]]:
        url_params["accountId"] = account_id
        response = await self.post_request(account_id, f"{self._api_endpoint}BrakePads?{'&'.join(f'{k}={v}' for k, v in url_params.items())}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_brake_pad(self, account_id: str, brake_pad_id: str, update_model: AssociationUpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}BrakePads/{brake_pad_id}", update_model)
        return response.ok


    async def delete_brake_pad(self, account_id: str, brake_pad_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}BrakePads/{brake_pad_id}")
        return response.ok



    async def get_brake_pad_attachments_by_id(self, account_id: str, brake_pad_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}BrakePads/{brake_pad_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}BrakePads/{brake_pad_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_brake_pad_attachments_by_name(self, account_id: str, brake_pad_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}BrakePads/{brake_pad_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_brake_pad_attachment(self, account_id: str, brake_pad_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}BrakePads/{brake_pad_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_brake_pad_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, brake_pad_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_brake_pad_attachment(
            add_attached_file_response.account_id,
            brake_pad_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, brake_pad_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, brake_pad_id, None, None)


    async def _upload_brake_pad_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, brake_pad_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, brake_pad_id, file_path, file_name)

            return await self._set_brake_pad_attachment_server_state_to_completed(add_attached_file_response, brake_pad_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, brake_pad_id, file_path, file_name, message=e)


    async def add_attachment_to_brake_pad(self, account_id: str, brake_pad_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}BrakePads/{brake_pad_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, brake_pad_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, brake_pad_id, file_path, model.file_name)

        return await self._upload_brake_pad_attachment(parsed_response, brake_pad_id, file_path, model.file_name)


    async def retry_brake_pad_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_brake_pad_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_brake_pad_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_brake_pad_attachment(self, account_id: str, brake_pad_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}BrakePads/{brake_pad_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_brake_set_by_id(self, account_id: str, brake_set_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}BrakeSets/{brake_set_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def search_for_brake_sets(self, account_id: str, search_info: AssociatedModelSeachObject, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}BrakeSets/Search"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url, search_info)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_brake_set(self, account_id: str, create_model: AssociationCreateModel, url_params: Dict[str, str]={}) -> Future[ApiGetResult[Dict]]:
        url_params["accountId"] = account_id
        response = await self.post_request(account_id, f"{self._api_endpoint}BrakeSets?{'&'.join(f'{k}={v}' for k, v in url_params.items())}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_brake_set(self, account_id: str, brake_set_id: str, update_model: AssociationUpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}BrakeSets/{brake_set_id}", update_model)
        return response.ok


    async def delete_brake_set(self, account_id: str, brake_set_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}BrakeSets/{brake_set_id}")
        return response.ok



    async def get_brake_set_attachments_by_id(self, account_id: str, brake_set_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}BrakeSets/{brake_set_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}BrakeSets/{brake_set_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_brake_set_attachments_by_name(self, account_id: str, brake_set_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}BrakeSets/{brake_set_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_brake_set_attachment(self, account_id: str, brake_set_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}BrakeSets/{brake_set_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_brake_set_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, brake_set_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_brake_set_attachment(
            add_attached_file_response.account_id,
            brake_set_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, brake_set_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, brake_set_id, None, None)


    async def _upload_brake_set_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, brake_set_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, brake_set_id, file_path, file_name)

            return await self._set_brake_set_attachment_server_state_to_completed(add_attached_file_response, brake_set_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, brake_set_id, file_path, file_name, message=e)


    async def add_attachment_to_brake_set(self, account_id: str, brake_set_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}BrakeSets/{brake_set_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, brake_set_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, brake_set_id, file_path, model.file_name)

        return await self._upload_brake_set_attachment(parsed_response, brake_set_id, file_path, model.file_name)


    async def retry_brake_set_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_brake_set_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_brake_set_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_brake_set_attachment(self, account_id: str, brake_set_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}BrakeSets/{brake_set_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_part_item_by_id(self, account_id: str, part_item_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}PartItems/{part_item_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def add_part_item(self, account_id: str, part_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}PartItems?partId={part_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_part_item(self, account_id: str, part_item_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}PartItems/{part_item_id}", update_model)
        return response.ok


    async def delete_part_item(self, account_id: str, part_item_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}PartItems/{part_item_id}")
        return response.ok



    async def get_track_configuration_by_id(self, account_id: str, track_configuration_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}TrackConfigurations/{track_configuration_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def add_track_configuration(self, account_id: str, track_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}TrackConfigurations?trackId={track_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_track_configuration(self, account_id: str, track_configuration_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}TrackConfigurations/{track_configuration_id}", update_model)
        return response.ok


    async def delete_track_configuration(self, account_id: str, track_configuration_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}TrackConfigurations/{track_configuration_id}")
        return response.ok



    async def get_track_configuration_attachments_by_id(self, account_id: str, track_configuration_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}TrackConfigurations/{track_configuration_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}TrackConfigurations/{track_configuration_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_track_configuration_attachments_by_name(self, account_id: str, track_configuration_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}TrackConfigurations/{track_configuration_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_track_configuration_attachment(self, account_id: str, track_configuration_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}TrackConfigurations/{track_configuration_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_track_configuration_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, track_configuration_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_track_configuration_attachment(
            add_attached_file_response.account_id,
            track_configuration_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, track_configuration_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, track_configuration_id, None, None)


    async def _upload_track_configuration_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, track_configuration_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, track_configuration_id, file_path, file_name)

            return await self._set_track_configuration_attachment_server_state_to_completed(add_attached_file_response, track_configuration_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, track_configuration_id, file_path, file_name, message=e)


    async def add_attachment_to_track_configuration(self, account_id: str, track_configuration_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}TrackConfigurations/{track_configuration_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, track_configuration_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, track_configuration_id, file_path, model.file_name)

        return await self._upload_track_configuration_attachment(parsed_response, track_configuration_id, file_path, model.file_name)


    async def retry_track_configuration_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_track_configuration_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_track_configuration_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_track_configuration_attachment(self, account_id: str, track_configuration_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}TrackConfigurations/{track_configuration_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_track_speed_trap_definition_by_id(self, account_id: str, track_speed_trap_definition_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}TrackSpeedTrapDefinitions/{track_speed_trap_definition_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def add_track_speed_trap_definition(self, account_id: str, track_configuration_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}TrackSpeedTrapDefinitions?trackConfigurationId={track_configuration_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_track_speed_trap_definition(self, account_id: str, track_speed_trap_definition_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}TrackSpeedTrapDefinitions/{track_speed_trap_definition_id}", update_model)
        return response.ok


    async def delete_track_speed_trap_definition(self, account_id: str, track_speed_trap_definition_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}TrackSpeedTrapDefinitions/{track_speed_trap_definition_id}")
        return response.ok



    async def get_lap_speed_trap_by_id(self, account_id: str, lap_speed_trap_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}LapSpeedTraps/{lap_speed_trap_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def update_lap_speed_trap(self, account_id: str, lap_speed_trap_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}LapSpeedTraps/{lap_speed_trap_id}", update_model)
        return response.ok


    async def get_lap_marker_by_id(self, account_id: str, lap_marker_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}LapMarkers/{lap_marker_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_lap_markers(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}LapMarkers"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_lap_marker(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}LapMarkers?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_lap_marker(self, account_id: str, lap_marker_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}LapMarkers/{lap_marker_id}", update_model)
        return response.ok


    async def delete_lap_marker(self, account_id: str, lap_marker_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}LapMarkers/{lap_marker_id}")
        return response.ok



    async def get_lap_track_status_marker_by_id(self, account_id: str, lap_track_status_marker_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}LapTrackStatusMarkers/{lap_track_status_marker_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_lap_track_status_markers(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}LapTrackStatusMarkers"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_lap_track_status_marker(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}LapTrackStatusMarkers?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_lap_track_status_marker(self, account_id: str, lap_track_status_marker_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}LapTrackStatusMarkers/{lap_track_status_marker_id}", update_model)
        return response.ok


    async def delete_lap_track_status_marker(self, account_id: str, lap_track_status_marker_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}LapTrackStatusMarkers/{lap_track_status_marker_id}")
        return response.ok



    async def get_planned_lap_by_id(self, account_id: str, planned_lap_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}PlannedLaps/{planned_lap_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def add_planned_lap(self, account_id: str, planned_run_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}PlannedLaps?plannedRunId={planned_run_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_planned_lap(self, account_id: str, planned_lap_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}PlannedLaps/{planned_lap_id}", update_model)
        return response.ok


    async def delete_planned_lap(self, account_id: str, planned_lap_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}PlannedLaps/{planned_lap_id}")
        return response.ok



    async def get_planned_lap_attachments_by_id(self, account_id: str, planned_lap_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}PlannedLaps/{planned_lap_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}PlannedLaps/{planned_lap_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_planned_lap_attachments_by_name(self, account_id: str, planned_lap_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}PlannedLaps/{planned_lap_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_planned_lap_attachment(self, account_id: str, planned_lap_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}PlannedLaps/{planned_lap_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_planned_lap_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, planned_lap_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_planned_lap_attachment(
            add_attached_file_response.account_id,
            planned_lap_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, planned_lap_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, planned_lap_id, None, None)


    async def _upload_planned_lap_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, planned_lap_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, planned_lap_id, file_path, file_name)

            return await self._set_planned_lap_attachment_server_state_to_completed(add_attached_file_response, planned_lap_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, planned_lap_id, file_path, file_name, message=e)


    async def add_attachment_to_planned_lap(self, account_id: str, planned_lap_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}PlannedLaps/{planned_lap_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, planned_lap_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, planned_lap_id, file_path, model.file_name)

        return await self._upload_planned_lap_attachment(parsed_response, planned_lap_id, file_path, model.file_name)


    async def retry_planned_lap_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_planned_lap_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_planned_lap_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_planned_lap_attachment(self, account_id: str, planned_lap_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}PlannedLaps/{planned_lap_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_issue_list_issue_by_id(self, account_id: str, issue_list_issue_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}IssueListIssues/{issue_list_issue_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def search_for_issue_list_issues(self, account_id: str, search_info: AssociatedModelSeachObject, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}IssueListIssues/Search"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url, search_info)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_issue_list_issue(self, account_id: str, create_model: AssociationCreateModel, url_params: Dict[str, str]={}) -> Future[ApiGetResult[Dict]]:
        url_params["accountId"] = account_id
        response = await self.post_request(account_id, f"{self._api_endpoint}IssueListIssues?{'&'.join(f'{k}={v}' for k, v in url_params.items())}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_issue_list_issue(self, account_id: str, issue_list_issue_id: str, update_model: AssociationUpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}IssueListIssues/{issue_list_issue_id}", update_model)
        return response.ok


    async def delete_issue_list_issue(self, account_id: str, issue_list_issue_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}IssueListIssues/{issue_list_issue_id}")
        return response.ok



    async def get_issue_list_issue_attachments_by_id(self, account_id: str, issue_list_issue_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}IssueListIssues/{issue_list_issue_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}IssueListIssues/{issue_list_issue_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_issue_list_issue_attachments_by_name(self, account_id: str, issue_list_issue_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}IssueListIssues/{issue_list_issue_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_issue_list_issue_attachment(self, account_id: str, issue_list_issue_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}IssueListIssues/{issue_list_issue_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_issue_list_issue_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, issue_list_issue_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_issue_list_issue_attachment(
            add_attached_file_response.account_id,
            issue_list_issue_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, issue_list_issue_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, issue_list_issue_id, None, None)


    async def _upload_issue_list_issue_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, issue_list_issue_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, issue_list_issue_id, file_path, file_name)

            return await self._set_issue_list_issue_attachment_server_state_to_completed(add_attached_file_response, issue_list_issue_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, issue_list_issue_id, file_path, file_name, message=e)


    async def add_attachment_to_issue_list_issue(self, account_id: str, issue_list_issue_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}IssueListIssues/{issue_list_issue_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, issue_list_issue_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, issue_list_issue_id, file_path, model.file_name)

        return await self._upload_issue_list_issue_attachment(parsed_response, issue_list_issue_id, file_path, model.file_name)


    async def retry_issue_list_issue_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_issue_list_issue_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_issue_list_issue_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_issue_list_issue_attachment(self, account_id: str, issue_list_issue_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}IssueListIssues/{issue_list_issue_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_assembly_iteration_by_id(self, account_id: str, assembly_iteration_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}AssemblyIterations/{assembly_iteration_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def search_for_assembly_iterations(self, account_id: str, search_info: AssociatedModelSeachObject, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}AssemblyIterations/Search"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url, search_info)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_assembly_iteration(self, account_id: str, create_model: AssociationCreateModel, url_params: Dict[str, str]={}) -> Future[ApiGetResult[Dict]]:
        url_params["accountId"] = account_id
        response = await self.post_request(account_id, f"{self._api_endpoint}AssemblyIterations?{'&'.join(f'{k}={v}' for k, v in url_params.items())}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_assembly_iteration(self, account_id: str, assembly_iteration_id: str, update_model: AssociationUpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}AssemblyIterations/{assembly_iteration_id}", update_model)
        return response.ok


    async def delete_assembly_iteration(self, account_id: str, assembly_iteration_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}AssemblyIterations/{assembly_iteration_id}")
        return response.ok



    async def get_assembly_iteration_attachments_by_id(self, account_id: str, assembly_iteration_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}AssemblyIterations/{assembly_iteration_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}AssemblyIterations/{assembly_iteration_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_assembly_iteration_attachments_by_name(self, account_id: str, assembly_iteration_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}AssemblyIterations/{assembly_iteration_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_assembly_iteration_attachment(self, account_id: str, assembly_iteration_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}AssemblyIterations/{assembly_iteration_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_assembly_iteration_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, assembly_iteration_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_assembly_iteration_attachment(
            add_attached_file_response.account_id,
            assembly_iteration_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, assembly_iteration_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, assembly_iteration_id, None, None)


    async def _upload_assembly_iteration_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, assembly_iteration_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, assembly_iteration_id, file_path, file_name)

            return await self._set_assembly_iteration_attachment_server_state_to_completed(add_attached_file_response, assembly_iteration_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, assembly_iteration_id, file_path, file_name, message=e)


    async def add_attachment_to_assembly_iteration(self, account_id: str, assembly_iteration_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}AssemblyIterations/{assembly_iteration_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, assembly_iteration_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, assembly_iteration_id, file_path, model.file_name)

        return await self._upload_assembly_iteration_attachment(parsed_response, assembly_iteration_id, file_path, model.file_name)


    async def retry_assembly_iteration_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_assembly_iteration_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_assembly_iteration_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_assembly_iteration_attachment(self, account_id: str, assembly_iteration_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}AssemblyIterations/{assembly_iteration_id}/Attachments/{attached_file_id}")
        return response.ok


    async def get_session_type_by_id(self, account_id: str, session_type_id: str, options: ApiGetOptions) -> Future[ApiGetResult[Dict]]:
        url = f"{self._api_endpoint}SessionTypes/{session_type_id}"

        param_lookup = dict()
        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)

    async def get_all_session_types(self, account_id: str, options: ApiGetOptions) -> Future[ApiGetResult[List[Dict]]]:
        url = f"{self._api_endpoint}SessionTypes"

        param_lookup = dict()
        if account_id is not None and len(account_id) > 0:
            param_lookup["accountId"] = account_id

        url_parameters = self.build_url_parameters(options, param_lookup)

        if url_parameters is not None and len(url_parameters) > 0:
            url += "?" + url_parameters

        response = await self.get_request(account_id, url)

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)

    async def add_session_type(self, account_id: str, create_model: CreateModel) -> Future[ApiGetResult[Dict]]:
        response = await self.post_request(account_id, f"{self._api_endpoint}SessionTypes?accountId={account_id}", create_model)
        
        if response.ok == False:
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        return ApiGetResult(response_object, True, None)



    async def update_session_type(self, account_id: str, session_type_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}SessionTypes/{session_type_id}", update_model)
        return response.ok


    async def delete_session_type(self, account_id: str, session_type_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}SessionTypes/{session_type_id}")
        return response.ok



    async def get_session_type_attachments_by_id(self, account_id: str, session_type_id: str, attachment_ids: List[str]) -> Future[ApiGetResult[Dict]]:
        # We check this because even though we are suggesting a type in the function definition, in python this is never enforced.
        if isinstance(attachment_ids, str):
            url = f"{self._api_endpoint}SessionTypes/{session_type_id}/Attachments?attachmentsIds={attachment_ids}"
        elif isinstance(attachment_ids, List):
            url = f"{self._api_endpoint}SessionTypes/{session_type_id}/Attachments?attachmentsIds={','.join(attachment_ids)}"
        else:
            raise TypeError("attachment_ids must be either a list of ids or a string containing a single id")
        
        response = await self.get_request(account_id, url)
    
        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def get_session_type_attachments_by_name(self, account_id: str, session_type_id: str, group_name: str) -> Future[ApiGetResult[Dict]]:
        response = await self.get_request(account_id, f"{self._api_endpoint}SessionTypes/{session_type_id}/Attachments/{group_name}")

        
        if response.ok == False:
            # return ApiGetResult[List[Dict]](None, False, response.reason)
            return ApiGetResult(None, False, response.reason)

        response_string = response.content.decode()
        response_json = json.loads(response_string)
        
        response_object = [o for o in response_json]
        return ApiGetResult(response_object, True, None)


    async def update_session_type_attachment(self, account_id: str, session_type_id: str, attached_file_id: str, update_model: UpdateModel) -> Future[bool]:
        response = await self.put_request(account_id, f"{self._api_endpoint}SessionTypes/{session_type_id}/Attachments/{attached_file_id}", update_model)
        return response.ok


    async def _set_session_type_attachment_server_state_to_completed(self, add_attached_file_response: ApiAddAttachedFileResponse, session_type_id: str) -> Future[AddAttachmentResult]:
        # update the server attached file state to AvailableOnServer = 2
        update_result = await self.update_session_type_attachment(
            add_attached_file_response.account_id,
            session_type_id,
            add_attached_file_response.attached_file_id,
            UpdateModel(None, [ParameterUpdateModel("ServerAttachedFileState", "2")])
        )

        if update_result:
            return AddAttachmentResult(AddAttachmentStatus.SUCCESS, add_attached_file_response, session_type_id, None, None)
        return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS, add_attached_file_response, session_type_id, None, None)


    async def _upload_session_type_attachment(self, add_attached_file_response: ApiAddAttachedFileResponse, session_type_id: str, file_path: str, file_name: str) -> Future[AddAttachmentResult]:
        headers = {
            "x-amz-tagging": f"AccountId={add_attached_file_response.account_id}&UserId={add_attached_file_response.user_id}",
            "User-Agent": f"hhdm_apiclient_wrapper (python) {self.get_version()} {add_attached_file_response.user_id}"
        }

        try:
            if add_attached_file_response.use_compression:
                upload_result = await self.compress_and_upload_file(add_attached_file_response.url, file_path, file_name, headers)
            else:
                upload_result = await self.upload_file(add_attached_file_response.url, file_path, file_name, headers)

            if upload_result == False:
                return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, session_type_id, file_path, file_name)

            return await self._set_session_type_attachment_server_state_to_completed(add_attached_file_response, session_type_id)
        except Exception as e:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_UPLOAD, add_attached_file_response, session_type_id, file_path, file_name, message=e)


    async def add_attachment_to_session_type(self, account_id: str, session_type_id: str, model: ApiPrepareUploadModel, file_path: str) -> Future[AddAttachmentResult]:
        response = await self.post_request(account_id, f"{self._api_endpoint}SessionTypes/{session_type_id}/Attachments", model)

        if response.ok == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, None, session_type_id, file_path, model.file_name)

        response_string = response.content.decode()
        response_object = json.loads(response_string)
        parsed_response = ApiAddAttachedFileResponse.deserialize(**response_object)
        
        if parsed_response.is_valid == False:
            return AddAttachmentResult(AddAttachmentStatus.FAILED_TO_ADD, parsed_response, session_type_id, file_path, model.file_name)

        return await self._upload_session_type_attachment(parsed_response, session_type_id, file_path, model.file_name)


    async def retry_session_type_attachment(self, add_attachment_result: AddAttachmentResult) -> Future[AddAttachmentResult]:
        match add_attachment_result.add_attachment_status:
            case AddAttachmentStatus.SUCCESS:
                raise ValueError("Cannot retry a successful file attachment")
            case AddAttachmentStatus.FAILED_TO_ADD:
                raise ValueError("Cannot retry a file attachment that failed to add")
            case AddAttachmentStatus.FAILED_TO_UPLOAD:
                return await self._upload_session_type_attachment(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id, add_attachment_result.file_path, add_attachment_result.file_name)
            case AddAttachmentStatus.FAILED_TO_UPDATE_SERVER_STATUS:
                return await self._set_session_type_attachment_server_state_to_completed(add_attachment_result.add_attached_file_response, add_attachment_result.entity_id)
            case _:
                raise NotImplementedError(f"Retry for status {add_attachment_result.add_attachment_status} is not implemented.")
            

    async def delete_session_type_attachment(self, account_id: str, session_type_id: str, attached_file_id: str) -> Future[bool]:
        response = await self.delete_request(account_id, f"{self._api_endpoint}SessionTypes/{session_type_id}/Attachments/{attached_file_id}")
        return response.ok

