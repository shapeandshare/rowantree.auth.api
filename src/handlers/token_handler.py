import json
import logging

from starlette import status
from starlette.exceptions import HTTPException

from rowantree.auth.service.controllers.register import RegisterController
from rowantree.auth.service.services.auth import AuthService
from rowantree.auth.service.services.db.dao import DBDAO
from rowantree.auth.service.services.db.utils import WrappedConnectionPool

# Creating database connection pool, and DAO
wrapped_cnxpool: WrappedConnectionPool = WrappedConnectionPool()
dao: DBDAO = DBDAO(cnxpool=wrapped_cnxpool.cnxpool)
auth_service: AuthService = AuthService(dao=dao)

register_controller: RegisterController = RegisterController(auth_service=auth_service)


def handler(event, context):
    logging.error(event)
    logging.error(context)
    try:
        return register_controller.execute(request=event).json(by_alias=True)
    except HTTPException as error:
        logging.error(str(error))
        # raise error from error
        return {"statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, "body": json.dumps(error)}
    except Exception as error:
        # Caught all other uncaught errors.
        logging.error(str(error))
        return {"statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, "body": json.dumps(error)}
