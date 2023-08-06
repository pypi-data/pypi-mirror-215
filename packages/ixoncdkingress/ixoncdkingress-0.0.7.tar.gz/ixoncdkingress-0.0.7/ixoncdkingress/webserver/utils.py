"""
Utility functions.
"""
import json

from typing import Any, Dict, Tuple
from urllib.parse import parse_qs

from ixoncdkingress.cbc.api_client import ApiClient, Query
from ixoncdkingress.cbc.context import CbcIxapiResource, CbcContext
from ixoncdkingress.types import FunctionLocation, FunctionArguments
from ixoncdkingress.webserver.config import Config

def read_qs_as_dict(in_put: bytes) -> Dict[str, str]:
    """
    Reads and parses the URL query string, returns it as a dict with for each value only the first
    occurrence.
    """
    body = in_put.decode('utf-8')

    # parse_qs always returns non-empty lists!
    return {key: value[0] for (key,value) in parse_qs(body).items()}

def parse_function_location(in_put: str) -> FunctionLocation:
    """
    Parses the full function path into a module path and a function name.
    """

    function_path = in_put.split('.')

    function_name = function_path.pop()
    module_name = '.'.join(function_path)

    if not function_path:
        return 'functions', function_name

    return module_name, function_name

def _parse_context_values(context_items: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parses expected context_items into CbcIxapiResources
    and discards any unexpected context_items.
    """
    context_values = {}
    for context_name, context_resource in context_items.items():
        # context_values.apiApplication and .accessToken will be sent to the CbcContext
        # but are unused, they are only used to create the ApiClient.
        if (context_name not in
                ['user', 'company', 'agent', 'asset', 'apiApplication', 'accessToken']):
            continue

        if context_resource is None:
            continue

        # accessToken is not a CbcIxapiResource because it doesn't have
        # a publicId, name and custom field.
        if context_name == 'accessToken':
            context_values[context_name] = context_resource.get('headerValue')
            continue

        permissions = None
        if context_name in ['company', 'agent', 'asset']:
            permissions = set()
            if 'permissions' in context_resource:
                permissions.update(context_resource['permissions'])

        context_values[context_name] = CbcIxapiResource(
            context_resource['publicId'],
            context_resource['name'],
            context_resource['custom'],
            permissions,
        )

    return context_values

def parse_json_input(
        config: Config,
        context_config: Dict[str, str],
        body: str
    ) -> Tuple[CbcContext, FunctionLocation, FunctionArguments]:
    """
    Parses an application/json request body string into a context, function
    location and function arguments.
    """
    in_put = json.loads(body)

    function_location = parse_function_location(in_put.get('name', ''))

    # Get all context values, may be overwritten if a custom apiApplication is set
    # however this is then still needed for getting authentication values
    context_values = _parse_context_values(in_put.get('context', {}))

    context_config = context_config | {
        config_name: str(config_value)
        for config_name, config_value in in_put.get('config', {}).items()
    }

    api_client_kwargs = {}

    if api_application_res := context_values.get('apiApplication'):
        api_client_kwargs['api_application'] = api_application_res.public_id
    if api_company_res:= context_values.get('company'):
        api_client_kwargs['api_company'] = api_company_res.public_id
    if access_token := context_values.get('accessToken'):
        api_client_kwargs['authorization'] = access_token

    api_client = ApiClient(config.api_client_base_url, **api_client_kwargs)

    # Override the API application if it's set in context_config and not in production mode
    # and refetch custom properties of context_values for scoped custom properties.
    if not config.production_mode and (api_application_res := context_config.get('apiApplication')):
        query: Query = { 'fields': 'custom,name' }
        api_client.set_custom_api_application(api_application_res)

        # Without an access token we don't requery the custom properties
        # as the request will fail anyways.
        if context_values.get('accessToken'):
            api_data = {}
            user_res = api_client.get('MyUser', query=query)
            api_data['user'] = user_res['data']

            # Without a company we don't need to requery these properties
            # as the requests will fail anyways.
            if context_values.get('company'):
                company_res = api_client.get('MyCompany', query=query)
                api_data['company'] = company_res['data']

                if agent := context_values.get('agent'):
                    agent_res = api_client.get(
                        'Agent',
                        { 'publicId': agent.public_id },
                        query=query,
                    )
                    api_data['agent'] = agent_res['data']

                if asset := context_values.get('asset'):
                    asset_res = api_client.get(
                        'Asset',
                        { 'publicId': asset.public_id },
                        query=query,
                    )
                    api_data['asset'] = asset_res['data']

            # Overwrite existing context_values
            context_values = _parse_context_values(api_data)

    context = CbcContext(context_config, api_client, **context_values)

    function_arguments = in_put.get('arguments', {})

    return context, function_location, function_arguments
