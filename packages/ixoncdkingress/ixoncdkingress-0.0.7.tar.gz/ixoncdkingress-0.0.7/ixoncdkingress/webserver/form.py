"""
HTML form generator
"""
from typing import Optional, Dict, Set, Tuple, TYPE_CHECKING
from urllib.parse import parse_qs

from ixoncdkingress.cbc.api_client import ApiClient
from ixoncdkingress.cbc.context import CbcContext, CbcIxapiResource
from ixoncdkingress.types import FunctionLocation, FunctionArguments
from ixoncdkingress.webserver.config import Config
from ixoncdkingress.webserver.utils import parse_function_location

try:
    from dominate.document import document
    from dominate.tags import h1, form, div, label, input_, h3, table, thead, \
        th, tr, tbody, td, textarea

    HAS_DOMINATE = True # pragma: no cover
except ImportError: # pragma: no cover
    HAS_DOMINATE = False

if TYPE_CHECKING:
    from dominate import tags

def generate_form(pre_fill: Dict[str, str], form_output: Optional[str] = None) -> str:
    """
    Generates and renders the CDK Ingress HTML form
    """
    return _generate_form_document(pre_fill, form_output).render()

def _generate_form_document(
        pre_fill: Dict[str, str],
        form_output: Optional[str] = None
    ) -> 'document':
    """
    Generates the CDK Ingress HTML form document
    """
    if not HAS_DOMINATE:
        raise Exception('Requires dominate package. pip install dominate')

    doc = document(title='IXON CDK Ingress')

    with doc:
        h1('IXON CDK Ingress')
        with form(method='post'):
            with div(class_name='function'):
                label('Function', _for='function')
                input_(type='text', id='function', name='function', size='32', required='true',
                       value=pre_fill.get('function'))
            with div(class_name='arguments'):
                h3('Function input')
                _custom_properties(pre_fill, prefix='function_args__')

            with div(class_name='resource'):
                h3('User')
                _resource(pre_fill, prefix='user__', show_permission=False)
            with div(class_name='resource'):
                h3('Company')
                _resource(pre_fill, prefix='company__', show_permission=True)
            with div(class_name='resource'):
                h3('Asset')
                _resource(pre_fill, prefix='asset__', show_permission=True)
            with div(class_name='resource'):
                h3('Agent')
                _resource(pre_fill, prefix='agent__', show_permission=True)

            input_(type='submit', value='Run function')
            input_(type='reset', value='Clear form')

        h3('Function output')
        textarea(form_output or 'Function output goes here', rows='10', cols='80')

    return doc

def _custom_properties(pre_fill: Dict[str, str], prefix: str) -> 'tags.html_tag':
    """
    Generates a form fragment for custom properties.
    """
    table_tag = table()

    with table_tag:
        with thead():
            th('Key')
            th('Value')
        with tbody():
            for i in range(0, 9):
                with tr():
                    td(input_(type='text', name=f'{prefix}key{i}', id=f'{prefix}key{i}',
                              size='16', value=pre_fill.get(f'{prefix}key{i}')))
                    td(input_(type='text', name=f'{prefix}value{i}', id=f'{prefix}value{i}',
                              size='32', value=pre_fill.get(f'{prefix}value{i}')))

    return table_tag

def _permissions(pre_fill: Dict[str, str], prefix: str) -> 'tags.html_tag':
    """
    Generates a form fragment for permissions.
    """
    table_tag = table()

    with table_tag:
        with tbody():
            for i in range(0, 9):
                with tr():
                    td(input_(type='text', name=f'{prefix}value{i}', id=f'{prefix}value{i}',
                              size='32', value=pre_fill.get(f'{prefix}value{i}')))

    return table_tag

def _resource(pre_fill: Dict[str, str], prefix: str, show_permission: bool) -> 'tags.html_tag':
    """
    Generates a form fragment for a context resource.
    """
    table_tag = table()

    with table_tag:
        with tbody():
            with tr():
                td(label('PublicID', _for=f'{prefix}public_id'))
                td(input_(type='text', id=f'{prefix}public_id', name=f'{prefix}public_id',
                          size='12', value=pre_fill.get(f'{prefix}public_id')))
            with tr():
                td(label('Name', _for=f'{prefix}name'))
                td(input_(type='text', id=f'{prefix}name', name=f'{prefix}name', size='32',
                          value=pre_fill.get(f'{prefix}name')))
            with tr():
                td('Custom properties')
                td(_custom_properties(pre_fill, f'{prefix}custom_properties__'))

            if show_permission:
                td('Permissions')
                td(_permissions(pre_fill, f'{prefix}permissions__'))

    return table_tag

def parse_form_input(
        config: Config,
        context_config: Dict[str, str],
        body: str) -> Tuple[CbcContext, FunctionLocation, FunctionArguments]:
    """
    Parses an application/x-www-form-urlencoded request body string into a context, function
    location and function arguments.
    """

    in_put = parse_qs(body)

    context = CbcContext(
        context_config,
        api_client=ApiClient(config.api_client_base_url),
        user=_parse_resource('user__', in_put, False),
        company=_parse_resource('company__', in_put, True),
        asset=_parse_resource('asset__', in_put, True),
        agent=_parse_resource('agent__', in_put, True)
    )

    function_location = parse_function_location(in_put.get('function', [''])[0])
    function_arguments = _parse_function_args(in_put)

    return context, function_location, function_arguments

def _parse_function_args(in_put: dict[str, list[str]]) -> FunctionArguments:
    function_arguments = {}
    i = 0
    while in_put.get(f'function_args__key{i}') and in_put.get(f'function_args__value{i}'):
        function_arguments[in_put[f'function_args__key{i}'][0]] = \
            in_put[f'function_args__value{i}'][0]
        i += 1

    return function_arguments

def _parse_resource(
        prefix: str,
        in_put: dict[str, list[str]],
        has_permissions: bool
    ) -> Optional[CbcIxapiResource]:
    """
    Reads a resource description from the in_put and returns it as a CbcResource.
    """
    props = {}
    permissions: Optional[Set[str]] = None
    if not in_put.get(f'{prefix}public_id') or not in_put.get(f'{prefix}name'):
        return None

    prop_iterator = 0
    prop_prefix = f'{prefix}custom_properties__'
    while (in_put.get(f'{prop_prefix}key{prop_iterator}')
           and in_put.get(f'{prop_prefix}value{prop_iterator}')):
        permission = in_put[f'{prop_prefix}value{prop_iterator}'][0]
        props[in_put[f'{prop_prefix}key{prop_iterator}'][0]] = permission
        prop_iterator += 1

    if has_permissions:
        permissions = set()
        permission_iterator = 0
        permission_prefix = f'{prefix}permissions__'
        while in_put.get(f'{permission_prefix}value{permission_iterator}'):
            permissions.add(in_put[f'{permission_prefix}value{permission_iterator}'][0])
            permission_iterator += 1

    return CbcIxapiResource(in_put[f'{prefix}public_id'][0],
                            in_put[f'{prefix}name'][0],
                            props,
                            permissions)
