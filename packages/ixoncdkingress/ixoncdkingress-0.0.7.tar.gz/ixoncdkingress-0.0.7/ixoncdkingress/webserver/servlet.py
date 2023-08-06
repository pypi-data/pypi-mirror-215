"""CBC servlet module."""
from typing import Tuple, Dict

import os
import json

from ixoncdkingress.utils import handle_exception
from ixoncdkingress.cbc.caller import call_cbc
from ixoncdkingress.webserver.config import load_json_file
from ixoncdkingress.cbc.context import CbcContext
from ixoncdkingress.webserver.config import Config
from ixoncdkingress.webserver.form import generate_form, parse_form_input
from ixoncdkingress.webserver.response import Response
from ixoncdkingress.webserver.request import Request
from ixoncdkingress.webserver.utils import read_qs_as_dict, parse_json_input

from ixoncdkingress.types import ResponseCode, ContentType, FunctionLocation, FunctionArguments


class Servlet:
    """Servlet handling CBC calls."""
    config: Config

    def __init__(self, config: Config) -> None:
        self.config = config

    def do_options(self, request: Request, response: Response) -> None:
        """
        Handle an OPTIONS request
        """
        del request

        response.status_code = ResponseCode.NO_CONTENT
        response.content_type = ContentType.HTML
        response.headers = [
            # Only useful for testing with swagger
            # when not running behind a production nginx
            ('Access-Control-Allow-Credentials', 'false'),
            ('Access-Control-Allow-Headers', '*'),
            ('Access-Control-Allow-Methods', '*'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Expose-Headers', '*'),
            ('Access-Control-Max-Age', '30'),  # cache time of the above
        ]

    def do_get(self, request: Request, response: Response) -> None:
        """
        Handle a GET request
        """
        response.status_code = ResponseCode.OK
        response.headers = [('Content-Type', ContentType.HTML.value)]

        pre_fill = {}

        if request.cookies:
            pre_fill = {k: v.value for k, v in request.cookies.items()}

        response.set_body(bytes(generate_form(pre_fill), 'utf-8'))

    def do_post(self, request: Request, response: Response) -> None:
        """
        Handle a POST request
        """
        available_content_types = [ContentType.JSON]

        context_config = {}

        if not self.config.production_mode:
            # Only JSON requests are allowed in production mode
            available_content_types.append(ContentType.FORM)
            try:
                context_config = load_json_file(
                    os.environ.get('CONTEXT_CONFIG_PATH', './context_config.json'), {}
                )
            except json.JSONDecodeError as exception:
                handle_exception(exception, response)
                return

            logger = self.config.get_logger()
            logger.info(
                'Default context.config: %s', context_config
            )

        if request.content_type not in available_content_types:
            raise NotImplementedError()

        out_put = call_cbc(
                self.config,
                *(self._parse_body(request.request_body, request.content_type, context_config)),
                response
            )

        if response.status_code == ResponseCode.INTERNAL_ERROR:
            return

        if ContentType.FORM == request.content_type:
            pre_fill = read_qs_as_dict(request.request_body)
            response.set_body(
                bytes(generate_form(pre_fill, json.dumps(out_put, indent=4)), 'utf-8')
            )
            response.content_type = ContentType.HTML
            response.cookie = {k: f'{v}; Max-Age=28800' for k, v in pre_fill.items()}
        else: # ContentType.JSON by exclusion
            response.set_body(bytes(json.dumps(out_put), 'utf-8'))
            response.content_type = request.content_type
            response.headers.append(('Access-Control-Allow-Origin', '*'))

    def _parse_body(
        self,
        in_put: bytes,
        content_type: ContentType,
        context_config: Dict[str, str],
    ) -> Tuple[CbcContext, FunctionLocation, FunctionArguments]:
        """
        Parses the request body to a key-value dictionary.
        """
        body = in_put.decode('utf-8')

        if content_type == ContentType.FORM:
            return parse_form_input(self.config, context_config, body)

        if content_type == ContentType.JSON:
            return parse_json_input(self.config, context_config, body)

        raise NotImplementedError()
