import functools
import json
import logging
from typing import Callable

import azure.functions as func
from jose import JWTError

from src.authentication.bearer import AuthenticationTokenException
from src.authentication.bearer import extract_claims
from src.authentication.bearer import validate_claims


def authenticate_request(required_claims: dict[str, any]) -> func.HttpResponse:
    def argument_wrapper(callback: Callable[..., any]):
        @functools.wraps(callback)
        def wrapper(req: func.HttpRequest, *args, **kwargs) -> func.HttpResponse:
            try:
                logging.info(
                    f"KBRAIN Authentication. Required claims: {json.dumps(required_claims)}"
                )
                try:
                    auth = req.headers.get("Authorization", None)
                    token_claims = extract_claims(auth)
                    validate_claims(token_claims, required_claims)
                except (AuthenticationTokenException, JWTError) as ae:
                    return func.HttpResponse(str(ae), status_code=401)

                [data, status] = callback(req, *args, **kwargs)
                return func.HttpResponse(data, status_code=status)
            except Exception as ex:
                return func.HttpResponse(str(ex), status_code=500)

        return wrapper

    return argument_wrapper
