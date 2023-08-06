# coding: utf-8

"""
    SnapTrade

    Connect brokerage accounts to your app for live positions and trading

    The version of the OpenAPI document: 1.0.0
    Contact: api@snaptrade.com
    Created by: https://snaptrade.com/
"""

from dataclasses import dataclass
import typing_extensions
import urllib3
from snaptrade_client.request_before_hook import request_before_hook
import json
from urllib3._collections import HTTPHeaderDict

from snaptrade_client.api_response import AsyncGeneratorResponse
from snaptrade_client import api_client, exceptions
from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from snaptrade_client import schemas  # noqa: F401

from snaptrade_client.model.model_portfolio import ModelPortfolio as ModelPortfolioSchema
from snaptrade_client.model.model_portfolio_security import ModelPortfolioSecurity as ModelPortfolioSecuritySchema
from snaptrade_client.model.model_portfolio_details import ModelPortfolioDetails as ModelPortfolioDetailsSchema
from snaptrade_client.model.model_portfolio_asset_class import ModelPortfolioAssetClass as ModelPortfolioAssetClassSchema

from snaptrade_client.type.model_portfolio_details import ModelPortfolioDetails
from snaptrade_client.type.model_portfolio_asset_class import ModelPortfolioAssetClass
from snaptrade_client.type.model_portfolio import ModelPortfolio
from snaptrade_client.type.model_portfolio_security import ModelPortfolioSecurity

from . import path

# Path params
ModelPortfolioIdSchema = schemas.UUIDSchema
RequestRequiredPathParams = typing_extensions.TypedDict(
    'RequestRequiredPathParams',
    {
        'modelPortfolioId': typing.Union[ModelPortfolioIdSchema, str, uuid.UUID, ],
    }
)
RequestOptionalPathParams = typing_extensions.TypedDict(
    'RequestOptionalPathParams',
    {
    },
    total=False
)


class RequestPathParams(RequestRequiredPathParams, RequestOptionalPathParams):
    pass


request_path_model_portfolio_id = api_client.PathParameter(
    name="modelPortfolioId",
    style=api_client.ParameterStyle.SIMPLE,
    schema=ModelPortfolioIdSchema,
    required=True,
)
# body param
SchemaForRequestBodyApplicationJson = ModelPortfolioDetailsSchema


request_body_model_portfolio_details = api_client.RequestBody(
    content={
        'application/json': api_client.MediaType(
            schema=SchemaForRequestBodyApplicationJson),
    },
    required=True,
)
_auth = [
    'PartnerClientId',
    'PartnerSignature',
    'PartnerTimestamp',
]


@dataclass
class ApiResponseFor200(api_client.ApiResponse):
    body: schemas.Unset = schemas.unset


@dataclass
class ApiResponseFor200Async(api_client.AsyncApiResponse):
    body: schemas.Unset = schemas.unset


_response_for_200 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor200,
    response_cls_async=ApiResponseFor200Async,
)
_status_code_to_response = {
    '200': _response_for_200,
}


class BaseApi(api_client.Api):

    def _modify_model_portfolio_by_id_mapped_args(
        self,
        body: typing.Optional[ModelPortfolioDetails] = None,
        model_portfolio_id: typing.Optional[str] = None,
        model_portfolio: typing.Optional[ModelPortfolio] = None,
        model_portfolio_security: typing.Optional[typing.List[ModelPortfolioSecurity]] = None,
        model_portfolio_asset_class: typing.Optional[typing.List[ModelPortfolioAssetClass]] = None,
        path_params: typing.Optional[dict] = {},
    ) -> api_client.MappedArgs:
        args: api_client.MappedArgs = api_client.MappedArgs()
        _path_params = {}
        _body = {}
        if model_portfolio is not None:
            _body["model_portfolio"] = model_portfolio
        if model_portfolio_security is not None:
            _body["model_portfolio_security"] = model_portfolio_security
        if model_portfolio_asset_class is not None:
            _body["model_portfolio_asset_class"] = model_portfolio_asset_class
        args.body = body if body is not None else _body
        if model_portfolio_id is not None:
            _path_params["modelPortfolioId"] = model_portfolio_id
        args.path = path_params if path_params else _path_params
        return args

    async def _amodify_model_portfolio_by_id_oapg(
        self,
        body: typing.Any = None,
        path_params: typing.Optional[dict] = {},
        skip_deserialization: bool = True,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        content_type: str = 'application/json',
        stream: bool = False,
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        """
        Updates model portfolio object
        :param skip_deserialization: If true then api_response.response will be set but
            api_response.body and api_response.headers will not be deserialized into schema
            class instances
        """
        self._verify_typed_dict_inputs_oapg(RequestPathParams, path_params)
        used_path = path.value
    
        _path_params = {}
        for parameter in (
            request_path_model_portfolio_id,
        ):
            parameter_data = path_params.get(parameter.name, schemas.unset)
            if parameter_data is schemas.unset:
                continue
            serialized_data = parameter.serialize(parameter_data)
            _path_params.update(serialized_data)
    
        for k, v in _path_params.items():
            used_path = used_path.replace('{%s}' % k, v)
    
        _headers = HTTPHeaderDict()
        # TODO add cookie handling
        method = 'post'.upper()
        _headers.add('Content-Type', content_type)
    
        if body is schemas.unset:
            raise exceptions.ApiValueError(
                'The required body parameter has an invalid value of: unset. Set a valid value instead')
        _fields = None
        _body = None
        request_before_hook(
            resource_path=used_path,
            method=method,
            configuration=self.api_client.configuration,
            body=body,
            auth_settings=_auth,
            headers=_headers,
        )
        serialized_data = request_body_model_portfolio_details.serialize(body, content_type)
        if 'fields' in serialized_data:
            _fields = serialized_data['fields']
        elif 'body' in serialized_data:
            _body = serialized_data['body']
    
        response = await self.api_client.async_call_api(
            resource_path=used_path,
            method=method,
            headers=_headers,
            fields=_fields,
            serialized_body=_body,
            body=body,
            auth_settings=_auth,
            timeout=timeout,
        )
    
        if stream:
            if not 200 <= response.http_response.status <= 299:
                body = (await response.http_response.content.read()).decode("utf-8")
                raise exceptions.ApiStreamingException(
                    status=response.http_response.status,
                    reason=response.http_response.reason,
                    body=body,
                )
    
            async def stream_iterator():
                """
                iterates over response.http_response.content and closes connection once iteration has finished
                """
                async for line in response.http_response.content:
                    if line == b'\r\n':
                        continue
                    yield line
                response.http_response.close()
                await response.session.close()
            return AsyncGeneratorResponse(
                content=stream_iterator(),
                headers=response.http_response.headers,
                status=response.http_response.status,
                response=response.http_response
            )
    
        response_for_status = _status_code_to_response.get(str(response.http_response.status))
        if response_for_status:
            api_response = await response_for_status.deserialize_async(
                                                    response,
                                                    self.api_client.configuration,
                                                    skip_deserialization=skip_deserialization
                                                )
        else:
            # If response data is JSON then deserialize for SDK consumer convenience
            is_json = api_client.JSONDetector._content_type_is_json(response.http_response.headers.get('Content-Type', ''))
            api_response = api_client.ApiResponseWithoutDeserializationAsync(
                body=await response.http_response.json() if is_json else await response.http_response.text(),
                response=response.http_response,
                round_trip_time=response.round_trip_time,
                status=response.http_response.status,
                headers=response.http_response.headers,
            )
    
        if not 200 <= api_response.status <= 299:
            raise exceptions.ApiException(api_response=api_response)
    
        # cleanup session / response
        response.http_response.close()
        await response.session.close()
    
        return api_response


    def _modify_model_portfolio_by_id_oapg(
        self,
        body: typing.Any = None,
        path_params: typing.Optional[dict] = {},
        skip_deserialization: bool = True,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        content_type: str = 'application/json',
        stream: bool = False,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        """
        Updates model portfolio object
        :param skip_deserialization: If true then api_response.response will be set but
            api_response.body and api_response.headers will not be deserialized into schema
            class instances
        """
        self._verify_typed_dict_inputs_oapg(RequestPathParams, path_params)
        used_path = path.value
    
        _path_params = {}
        for parameter in (
            request_path_model_portfolio_id,
        ):
            parameter_data = path_params.get(parameter.name, schemas.unset)
            if parameter_data is schemas.unset:
                continue
            serialized_data = parameter.serialize(parameter_data)
            _path_params.update(serialized_data)
    
        for k, v in _path_params.items():
            used_path = used_path.replace('{%s}' % k, v)
    
        _headers = HTTPHeaderDict()
        # TODO add cookie handling
        method = 'post'.upper()
        _headers.add('Content-Type', content_type)
    
        if body is schemas.unset:
            raise exceptions.ApiValueError(
                'The required body parameter has an invalid value of: unset. Set a valid value instead')
        _fields = None
        _body = None
        request_before_hook(
            resource_path=used_path,
            method=method,
            configuration=self.api_client.configuration,
            body=body,
            auth_settings=_auth,
            headers=_headers,
        )
        serialized_data = request_body_model_portfolio_details.serialize(body, content_type)
        if 'fields' in serialized_data:
            _fields = serialized_data['fields']
        elif 'body' in serialized_data:
            _body = serialized_data['body']
    
        response = self.api_client.call_api(
            resource_path=used_path,
            method=method,
            headers=_headers,
            fields=_fields,
            serialized_body=_body,
            body=body,
            auth_settings=_auth,
            timeout=timeout,
        )
    
        response_for_status = _status_code_to_response.get(str(response.http_response.status))
        if response_for_status:
            api_response = response_for_status.deserialize(
                                                    response,
                                                    self.api_client.configuration,
                                                    skip_deserialization=skip_deserialization
                                                )
        else:
            # If response data is JSON then deserialize for SDK consumer convenience
            is_json = api_client.JSONDetector._content_type_is_json(response.http_response.headers.get('Content-Type', ''))
            api_response = api_client.ApiResponseWithoutDeserialization(
                body=json.loads(response.http_response.data) if is_json else response.http_response.data,
                response=response.http_response,
                round_trip_time=response.round_trip_time,
                status=response.http_response.status,
                headers=response.http_response.headers,
            )
    
        if not 200 <= api_response.status <= 299:
            raise exceptions.ApiException(api_response=api_response)
    
        return api_response


class ModifyModelPortfolioById(BaseApi):
    # this class is used by api classes that refer to endpoints with operationId fn names

    async def amodify_model_portfolio_by_id(
        self,
        body: typing.Optional[ModelPortfolioDetails] = None,
        model_portfolio_id: typing.Optional[str] = None,
        model_portfolio: typing.Optional[ModelPortfolio] = None,
        model_portfolio_security: typing.Optional[typing.List[ModelPortfolioSecurity]] = None,
        model_portfolio_asset_class: typing.Optional[typing.List[ModelPortfolioAssetClass]] = None,
        path_params: typing.Optional[dict] = {},
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        args = self._modify_model_portfolio_by_id_mapped_args(
            body=body,
            path_params=path_params,
            model_portfolio_id=model_portfolio_id,
            model_portfolio=model_portfolio,
            model_portfolio_security=model_portfolio_security,
            model_portfolio_asset_class=model_portfolio_asset_class,
        )
        return await self._amodify_model_portfolio_by_id_oapg(
            body=args.body,
            path_params=args.path,
        )
    
    def modify_model_portfolio_by_id(
        self,
        body: typing.Optional[ModelPortfolioDetails] = None,
        model_portfolio_id: typing.Optional[str] = None,
        model_portfolio: typing.Optional[ModelPortfolio] = None,
        model_portfolio_security: typing.Optional[typing.List[ModelPortfolioSecurity]] = None,
        model_portfolio_asset_class: typing.Optional[typing.List[ModelPortfolioAssetClass]] = None,
        path_params: typing.Optional[dict] = {},
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        args = self._modify_model_portfolio_by_id_mapped_args(
            body=body,
            path_params=path_params,
            model_portfolio_id=model_portfolio_id,
            model_portfolio=model_portfolio,
            model_portfolio_security=model_portfolio_security,
            model_portfolio_asset_class=model_portfolio_asset_class,
        )
        return self._modify_model_portfolio_by_id_oapg(
            body=args.body,
            path_params=args.path,
        )

class ApiForpost(BaseApi):
    # this class is used by api classes that refer to endpoints by path and http method names

    async def apost(
        self,
        body: typing.Optional[ModelPortfolioDetails] = None,
        model_portfolio_id: typing.Optional[str] = None,
        model_portfolio: typing.Optional[ModelPortfolio] = None,
        model_portfolio_security: typing.Optional[typing.List[ModelPortfolioSecurity]] = None,
        model_portfolio_asset_class: typing.Optional[typing.List[ModelPortfolioAssetClass]] = None,
        path_params: typing.Optional[dict] = {},
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        args = self._modify_model_portfolio_by_id_mapped_args(
            body=body,
            path_params=path_params,
            model_portfolio_id=model_portfolio_id,
            model_portfolio=model_portfolio,
            model_portfolio_security=model_portfolio_security,
            model_portfolio_asset_class=model_portfolio_asset_class,
        )
        return await self._amodify_model_portfolio_by_id_oapg(
            body=args.body,
            path_params=args.path,
        )
    
    def post(
        self,
        body: typing.Optional[ModelPortfolioDetails] = None,
        model_portfolio_id: typing.Optional[str] = None,
        model_portfolio: typing.Optional[ModelPortfolio] = None,
        model_portfolio_security: typing.Optional[typing.List[ModelPortfolioSecurity]] = None,
        model_portfolio_asset_class: typing.Optional[typing.List[ModelPortfolioAssetClass]] = None,
        path_params: typing.Optional[dict] = {},
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        args = self._modify_model_portfolio_by_id_mapped_args(
            body=body,
            path_params=path_params,
            model_portfolio_id=model_portfolio_id,
            model_portfolio=model_portfolio,
            model_portfolio_security=model_portfolio_security,
            model_portfolio_asset_class=model_portfolio_asset_class,
        )
        return self._modify_model_portfolio_by_id_oapg(
            body=args.body,
            path_params=args.path,
        )

