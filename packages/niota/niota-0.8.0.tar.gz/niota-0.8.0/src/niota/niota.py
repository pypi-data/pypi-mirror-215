import json
import logging
from datetime import datetime
from typing import Dict, Optional

from niota import exceptions, signature
from niota.iota_client import IotaClient

logger = logging.getLogger(__name__)


class Niota():
    DEFAULT_PROVIDER = 'NUMBERSPROTOCOL'

    def __init__(
        self,
        private_key: str,
        public_key: str,
        base_url: Optional[str] = None,
        jwt_token: Optional[str] = None,
    ):
        self.iota_client = IotaClient(base_url, jwt_token)
        self.private_key = private_key
        self.public_key = public_key

    def create_message(
        self,
        raw_cid: str,
        ida_cid='',
        ida_mid='',
        ida_sha256sum='',
        metadata_cid='',
        provider=DEFAULT_PROVIDER,
        service_message='',
    ):
        """Create message on IOTA

        Args:
            raw_cid (str)
            ida_cid (str, optional): Defaults to ''.
            ida_mid (str, optional): Defaults to ''.
            ida_sha256sum (str, optional): Defaults to ''.
            metadata_cid (str, optional): Defaults to ''.
            provider (_type_, optional): Defaults to DEFAULT_PROVIDER.
            service_message (str, optional): Defaults to ''.

        Returns:
            str: message_id
            str: index(raw_cid)
        """
        index = raw_cid
        ida_message = {
            'timestamp': self.get_current_timestamp(),
            'raw_cid': raw_cid,
            'ida_cid': ida_cid,
            'ida_mid': ida_mid,
            'ida_sha256sum': ida_sha256sum,
            'metadata_cid': metadata_cid,
            'provider': provider,
            'service_message': service_message,
        }
        serialized_payload = self.create_serialized_payload(ida_message)
        message = self.iota_client.create_message(index, serialized_payload)
        return message.data.messageId, index

    def get_message_payload_string(self, message_id: str):
        message_resp = self.iota_client.get_message(message_id)
        return self.iota_client.retrieve_payload_content(message_resp.data.payload).data

    def get_message_data(self, message_id: str, verify=True):
        message_resp = self.iota_client.get_message(message_id)
        payload_string = self.iota_client.retrieve_payload_content(message_resp.data.payload).data
        if verify:
            self.verify_message_payload_string(payload_string)
        return json.loads(payload_string)['data']

    def get_current_timestamp(self):
        return int(datetime.utcnow().timestamp())

    def create_serialized_payload(self, data: Dict):
        serialized_data = json.dumps(data, sort_keys=True)
        base64_signature = signature.sign_message(self.private_key, serialized_data)
        serialized_payload = json.dumps({
            'data': serialized_data,
            'signature': base64_signature,
        })
        return serialized_payload

    def get_message_ids_from_index(self, index: str):
        search_message_resp = self.iota_client.search_message(index)
        return search_message_resp.data.messageIds

    def get_verified_data_from_index(self, index: str):
        search_message_resp = self.iota_client.search_message(index)
        payload_strings = [self.get_message_payload_string(id) for id in search_message_resp.data.messageIds]
        verified_data = []
        for payload_string in payload_strings:
            try:
                self.verify_message_payload_string(payload_string)
            except Exception as e:
                logger.warning('Payload string verification fails. Detail: %s', e)
            else:
                try:
                    data_str = json.loads(payload_string)['data']
                    verified_data.append(json.loads(data_str))
                except Exception as e:
                    logger.warning('Failed to collect data from verified message. Detail: %s', e)
        return verified_data

    def verify_message_payload_string(self, payload_string: str):
        try:
            payload = json.loads(payload_string)
            signature.verify_signature(self.public_key, payload['signature'], payload['data'])
        except Exception as e:
            raise exceptions.MessageVerificationFailed from e
