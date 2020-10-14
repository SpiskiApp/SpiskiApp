from django.db import connections
from django.db.utils import OperationalError
from django.http import HttpRequest, HttpResponseServerError, HttpResponse


def healthcheck(request: HttpRequest) -> HttpResponse:
    main_db = connections["default"]

    try:
        main_db.ensure_connection()
    except OperationalError:
        return HttpResponseServerError()
    return HttpResponse("OK")
