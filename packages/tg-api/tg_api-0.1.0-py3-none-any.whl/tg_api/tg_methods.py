import io
from typing import Any, Union, Iterable

from pydantic import BaseModel

from .client import AsyncTgClient, SyncTgClient, TgRuntimeError, raise_for_tg_response_status
from . import tg_types


class BaseTgRequest(BaseModel):

    class Config:
        extra = 'forbid'
        validate_assignment = True

    async def apost_as_json(self, api_method: str) -> bytes:
        client = AsyncTgClient.default_client.get(None)

        if not client:
            raise TgRuntimeError('Requires AsyncTgClient to be specified before call.')

        http_response = await client.session.post(
            f'{client.api_root}{api_method}',
            headers={
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            content=self.json(exclude_none=True).encode('utf-8'),
        )
        raise_for_tg_response_status(http_response)
        return http_response.content

    def post_as_json(self, api_method: str) -> bytes:
        client = SyncTgClient.default_client.get(None)

        if not client:
            raise TgRuntimeError('Requires SyncTgClient to be specified before call.')

        http_response = client.session.post(
            f'{client.api_root}{api_method}',
            headers={
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            content=self.json(exclude_none=True).encode('utf-8'),
        )
        raise_for_tg_response_status(http_response)
        return http_response.content

    async def apost_multipart_form_data(self, api_method: str, content: dict, files: dict) -> bytes:
        client = AsyncTgClient.default_client.get(None)

        if not client:
            raise TgRuntimeError('Requires AsyncTgClient to be specified before call.')

        http_response = await client.session.post(
            f'{client.api_root}{api_method}',
            files=files,
            data=content,
        )
        raise_for_tg_response_status(http_response)
        return http_response.content

    def post_multipart_form_data(self, api_method: str, content: dict, files: dict) -> bytes:
        client = SyncTgClient.default_client.get(None)

        if not client:
            raise TgRuntimeError('Requires SyncTgClient to be specified before call.')

        http_response = client.session.post(
            f'{client.api_root}{api_method}',
            files=files,
            data=content,
        )
        raise_for_tg_response_status(http_response)
        return http_response.content


class BaseTgResponse(BaseModel):
    ok: bool
    error_code: int | None = None
    description: str = ''

    result: Any

    class Config:
        extra = 'ignore'
        allow_mutation = False

    # TODO Some errors may also have an optional field 'parameters' of the type ResponseParameters, which can
    # help to automatically handle the error.


class SendMessageResponse(BaseTgResponse):
    result: tg_types.Message


class SendMessageRequest(BaseTgRequest):
    """Object encapsulates data for calling web API endpoint `sendMessage`.

    Telegram web API docs:
        See here https://core.telegram.org/bots/api#sendmessage
    """

    chat_id: int
    text: str
    parse_mode: tg_types.ParseMode | None
    entities: list[tg_types.MessageEntity] | None
    disable_web_page_preview: bool | None
    disable_notification: bool | None
    protect_content: bool | None
    message_thread_id: bool | None
    allow_sending_without_reply: bool | None
    reply_markup: Union[
        tg_types.InlineKeyboardMarkup,
        tg_types.ReplyKeyboardMarkup,
        tg_types.ReplyKeyboardRemove,
        tg_types.ForceReply,
    ] | None = None

    async def asend(self) -> SendMessageResponse:
        """Shortcut method to call sendMessage Tg web API endpoint."""
        json_payload = await self.apost_as_json('sendMessage')
        response = SendMessageResponse.parse_raw(json_payload)
        # TODO check for response.ok ?
        return response

    def send(self) -> SendMessageResponse:
        """Shortcut method to call sendMessage Tg web API endpoint."""
        json_payload = self.post_as_json('sendMessage')
        response = SendMessageResponse.parse_raw(json_payload)
        return response


class SendPhotoResponse(BaseTgResponse):
    result: tg_types.Message


class SendBytesPhotoRequest(BaseTgRequest):
    """Object encapsulates data for calling web API endpoint `sendPhoto`.

    Telegram web API docs:
        See here https://core.telegram.org/bots/api#sendphoto
    """

    chat_id: int
    photo: Union[
        bytes,
        Iterable[bytes],
        # TODO: httx supports AsyncIterable[bytes], but pydantic doesnt
    ]
    filename: str | None
    # TODO: message_thread_id: int | None
    # TODO: caption: str | None
    # TODO: parse_mode: str | None
    # TODO: caption_entities: list[tg_types.MessageEntity] | None
    # TODO: has_spoiler: bool | None
    # TODO: disable_notification: bool | None
    # TODO: protect_content: bool | None
    # TODO: reply_to_message_id: int | None
    # TODO: allow_sending_without_reply: bool | None
    # TODO: reply_markup: Union[
    #     tg_types.InlineKeyboardMarkup,
    #     tg_types.ReplyKeyboardMarkup,
    #     tg_types.ReplyKeyboardRemove,
    #     tg_types.ForceReply,
    # ] | None = None

    async def asend(self) -> SendPhotoResponse:
        """Shortcut method to call sendPhoto Tg web API endpoint."""
        content = self.dict(exclude_none=True, exclude={'photo'})
        photo_bytes = io.BytesIO(self.photo)
        photo_bytes.name = self.filename
        files = {'photo': photo_bytes}
        json_payload = await self.apost_multipart_form_data('sendPhoto', content, files)
        response = SendPhotoResponse.parse_raw(json_payload)
        return response

    def send(self) -> SendPhotoResponse:
        """Shortcut method to call sendPhoto Tg web API endpoint."""
        content = self.dict(exclude_none=True, exclude={'photo'})
        photo_bytes = io.BytesIO(self.photo)
        photo_bytes.name = self.filename
        files = {'photo': photo_bytes}
        json_payload = self.post_multipart_form_data('sendPhoto', content, files)
        response = SendPhotoResponse.parse_raw(json_payload)
        return response


class SendUrlPhotoRequest(BaseTgRequest):
    """Object encapsulates data for calling web API endpoint `sendPhoto`.

    Telegram web API docs:
        See here https://core.telegram.org/bots/api#sendphoto
    """

    chat_id: int
    photo: str
    filename: str | None
    # TODO: message_thread_id: int | None
    # TODO: caption: str | None
    # TODO: parse_mode: str | None
    # TODO: caption_entities: list[tg_types.MessageEntity] | None
    # TODO: has_spoiler: bool | None
    # TODO: disable_notification: bool | None
    # TODO: protect_content: bool | None
    # TODO: reply_to_message_id: int | None
    # TODO: allow_sending_without_reply: bool | None
    # TODO: reply_markup: Union[
    #     tg_types.InlineKeyboardMarkup,
    #     tg_types.ReplyKeyboardMarkup,
    #     tg_types.ReplyKeyboardRemove,
    #     tg_types.ForceReply,
    # ] | None = None

    async def asend(self) -> SendPhotoResponse:
        """Shortcut method to call sendPhoto Tg web API endpoint."""
        json_payload = await self.apost_as_json('sendPhoto')
        response = SendPhotoResponse.parse_raw(json_payload)
        return response

    def send(self) -> SendPhotoResponse:
        """Shortcut method to call sendPhoto Tg web API endpoint."""
        json_payload = self.post_as_json('sendPhoto')
        response = SendPhotoResponse.parse_raw(json_payload)
        return response


class SendDocumentResponse(BaseTgResponse):
    result: tg_types.Message


class SendBytesDocumentRequest(BaseTgRequest):
    """Object encapsulates data for calling web API endpoint `sendPhoto`.

    Telegram web API docs:
        See here https://core.telegram.org/bots/api#sendphoto
    """

    chat_id: int
    document: Union[
        bytes,
        Iterable[bytes],
        # TODO: httx supports AsyncIterable[bytes], but pydantic doesnt
    ]
    filename: str | None
    # TODO: message_thread_id: int | None
    # TODO: thumbnail: tg_types.InputFile | str | None
    # TODO: caption: str | None
    # TODO: parse_mode: str | None
    # TODO: caption_entities: list[tg_types.MessageEntity] | None
    # TODO: disable_content_type_detection: bool | None
    # TODO: disable_notification: bool | None
    # TODO: protect_content: bool | None
    # TODO: reply_to_message_id: int | None
    # TODO: allow_sending_without_reply: bool | None
    # TODO: reply_markup: Union[
    #     tg_types.InlineKeyboardMarkup,
    #     tg_types.ReplyKeyboardMarkup,
    #     tg_types.ReplyKeyboardRemove,
    #     tg_types.ForceReply,
    # ] | None = None

    async def asend(self) -> SendDocumentResponse:
        """Shortcut method to call sendDocument Tg web API endpoint."""
        content = self.dict(exclude_none=True, exclude={'document'})
        document_bytes = io.BytesIO(self.document)
        document_bytes.name = self.filename
        files = {'document': document_bytes}
        json_payload = await self.apost_multipart_form_data('sendDocument', content, files)
        response = SendDocumentResponse.parse_raw(json_payload)
        return response

    def send(self) -> SendDocumentResponse:
        """Shortcut method to call sendDocument Tg web API endpoint."""
        content = self.dict(exclude_none=True, exclude={'document'})
        document_bytes = io.BytesIO(self.document)
        document_bytes.name = self.filename
        files = {'document': document_bytes}
        json_payload = self.post_multipart_form_data('sendDocument', content, files)
        response = SendDocumentResponse.parse_raw(json_payload)
        return response


class SendUrlDocumentRequest(BaseTgRequest):
    """Object encapsulates data for calling web API endpoint `sendPhoto`.

    Telegram web API docs:
        See here https://core.telegram.org/bots/api#sendphoto
    """

    chat_id: int
    document: str
    filename: str | None
    # TODO: message_thread_id: int | None
    # TODO: thumbnail: tg_types.InputFile | str | None
    # TODO: caption: str | None
    # TODO: parse_mode: str | None
    # TODO: caption_entities: list[tg_types.MessageEntity] | None
    # TODO: disable_content_type_detection: bool | None
    # TODO: disable_notification: bool | None
    # TODO: protect_content: bool | None
    # TODO: reply_to_message_id: int | None
    # TODO: allow_sending_without_reply: bool | None
    # TODO: reply_markup: Union[
    #     tg_types.InlineKeyboardMarkup,
    #     tg_types.ReplyKeyboardMarkup,
    #     tg_types.ReplyKeyboardRemove,
    #     tg_types.ForceReply,
    # ] | None = None

    async def asend(self) -> SendDocumentResponse:
        """Shortcut method to call sendDocument Tg web API endpoint."""
        json_payload = await self.apost_as_json('sendDocument')
        response = SendDocumentResponse.parse_raw(json_payload)
        return response

    def send(self) -> SendDocumentResponse:
        """Shortcut method to call sendDocument Tg web API endpoint."""
        json_payload = self.post_as_json('sendDocument')
        response = SendDocumentResponse.parse_raw(json_payload)
        return response
