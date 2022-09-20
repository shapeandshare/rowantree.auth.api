import json
import logging
import traceback
from typing import Union

from starlette import status
from starlette.exceptions import HTTPException

from rowantree.auth.sdk import RegisterUserRequest, UserBase
from rowantree.auth.service.controllers.register import RegisterController
from rowantree.auth.service.services.auth import AuthService
from rowantree.auth.service.services.db.dao import DBDAO
from rowantree.auth.service.services.db.utils import WrappedConnectionPool
from src.contracts.dtos.lambda_response import LambdaResponse
from src.utils.form import parse_form_data

# Creating database connection pool, and DAO
wrapped_cnxpool: WrappedConnectionPool = WrappedConnectionPool()
dao: DBDAO = DBDAO(cnxpool=wrapped_cnxpool.cnxpool)
auth_service: AuthService = AuthService(dao=dao)

register_handler: RegisterController = RegisterController(auth_service=auth_service)


def handler(event, context):
    logging.error(event)
    logging.error(context)

    try:
        request: RegisterUserRequest = RegisterUserRequest.parse_obj(parse_form_data(event=event))
        response: UserBase = register_handler.execute(request=request)
        return LambdaResponse(status_code=status.HTTP_200_OK, body=response.json(by_alias=True)).dict(by_alias=True)
    except HTTPException as error:
        message_dict: dict[str, Union[dict, str]] = {
            "statusCode": error.status_code,
            "traceback": traceback.print_exc(),
            "error": str(error),
        }
        message: str = json.dumps(message_dict)
        logging.error(message)
        # raise error from error
        return LambdaResponse(status_code=error.status_code, body=message).dict(by_alias=True)
    except Exception as error:
        message_dict: dict[str, Union[dict, str]] = {
            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "traceback": traceback.print_exc(),
            "error": str(error),
        }
        message: str = json.dumps(message_dict)
        logging.error(message)
        # raise error from error
        return LambdaResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, body=message).dict(by_alias=True)
