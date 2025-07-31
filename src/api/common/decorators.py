import logging
from functools import wraps

from django.db import IntegrityError
from django.http import Http404

from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValidationError as e:
            logger.warning("Validation error: %s", e.detail)
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "data": {
                    "message": "Validation failed.",
                    "errors": e.detail,
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError as e:
            logger.error("Integrity error: %s", str(e))
            msg = "Unique constraint violated." if "unique" in str(e).lower() else "Integrity error occurred."
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "data": {
                    "message": msg,
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except (Http404, NotFound):
            logger.warning("Resource not found.")
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "data": {
                    "message": "The requested resource was not found.",
                }
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception("Unhandled exception: %s", str(e))
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": {
                    "message": "Something went wrong. Please try again.",
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return wrapper
