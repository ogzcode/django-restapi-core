from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import traceback


def _extract_error_message(data):
    if isinstance(data, dict):
        if 'detail' in data and isinstance(data['detail'], str):
            return data['detail']

        error_messages = []
        for key, value in data.items():
            if isinstance(value, list) and value:
                error_messages.append(f"{key}: {value[0]}")
            elif isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    if isinstance(nested_value, list) and nested_value:
                        error_messages.append(
                            f"{nested_key}: {nested_value[0]}")
            else:
                error_messages.append(str(value))

        if error_messages:
            return ", ".join(error_messages)
    elif isinstance(data, list) and data:
        return ", ".join(str(item) for item in data)

    return "An unknown error occurred"


def _handle_server_error(exc, status_code, context=None):
    error_message = f"Server error: {str(exc)}"
    print(
        f"Server error details (Status code {status_code}): {error_message}")
    print(f"Traceback: {traceback.format_exc()}")

    # Context'ten view bilgilerini çıkar
    view_name = context.get("view").__class__.__name__ if context and context.get("view") else None
    view_desc = context.get("view").__class__.__doc__ if context and context.get("view") else None

    return Response({
        'message': error_message,
        'error_type': type(exc).__name__,
        'status_code': status_code,
        'view_name': view_name,
        'view_desc': view_desc
    }, status=status_code)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code >= 500:
            return _handle_server_error(exc, response.status_code, context)
        else:
            message = _extract_error_message(response.data)
            
            # Context'ten view bilgilerini çıkar
            view_name = context.get("view").__class__.__name__ if context.get("view") else None
            view_desc = context.get("view").__class__.__doc__ if context.get("view") else None
            
            response_data = {
                'message': message,
                'view_name': view_name,
                'view_desc': view_desc
            }
            
            return Response(response_data, status=response.status_code)
    else:
        return _handle_server_error(exc, status.HTTP_500_INTERNAL_SERVER_ERROR, context)
