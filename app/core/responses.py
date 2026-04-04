from rest_framework.response import Response


def success_response(data=None, message="", status=200):
    """Retorna resposta padronizada de sucesso."""
    payload = {"success": True, "data": data if data is not None else {}}
    if message:
        payload["message"] = message
    return Response(payload, status=status)


def error_response(error="", details=None, status=400):
    """Retorna resposta padronizada de erro."""
    payload = {"success": False, "error": error}
    if details is not None:
        payload["details"] = details
    return Response(payload, status=status)
