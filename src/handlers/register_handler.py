import json
import logging

from requests_toolbelt.multipart import decoder
from starlette import status
from starlette.exceptions import HTTPException

from rowantree.auth.service.controllers.token import TokenController
from rowantree.auth.service.services.auth import AuthService
from rowantree.auth.service.services.db.dao import DBDAO
from rowantree.auth.service.services.db.utils import WrappedConnectionPool

# Creating database connection pool, and DAO
wrapped_cnxpool: WrappedConnectionPool = WrappedConnectionPool()
dao: DBDAO = DBDAO(cnxpool=wrapped_cnxpool.cnxpool)
auth_service: AuthService = AuthService(dao=dao)

token_controller: TokenController = TokenController(auth_service=auth_service)


def handler(event, context):
    logging.error(event)
    logging.error(context)
    multipart_data = decoder.MultipartDecoder.from_response(event["body"], event["headers"]["content-type"])
    # from requests_toolbelt import MultipartDecoder
    #
    # decoder = MultipartDecoder(content, content_type)
    # for part in decoder.parts:
    #     print(part.headers['content-type'])

    for part in multipart_data.parts:
        logging.error(part.content)  # Alternatively, part.text if you want unicode
        logging.error(part.headers)

    try:
        return token_controller.execute(request=event).json(by_alias=True)
    except HTTPException as error:
        logging.error(str(error))
        # raise error from error
        return {"statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, "body": json.dumps(error)}
    except Exception as error:
        # Caught all other uncaught errors.
        logging.error(str(error))
        return {"statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR, "body": json.dumps(error)}
