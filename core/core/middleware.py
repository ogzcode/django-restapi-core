import json
from django.http import JsonResponse
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class GraphQLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/graphql/'):
            authenticator = JWTAuthentication()
            try:
                auth_data = authenticator.authenticate(request)
                if auth_data is not None:
                    request.user = auth_data[0]
            except AuthenticationFailed:
                pass

        if request.path.startswith('/graphql/') and request.method == 'POST':
            if not request.user.is_authenticated:
                try:
                    body = json.loads(request.body)
                    query = body.get('query', '')

                    if 'IntrospectionQuery' not in query:
                        return JsonResponse(
                            {"errors": [
                                {"message": "You are not authorized to perform this action."}]},
                            status=status.HTTP_401_UNAUTHORIZED,
                        )
                except (json.JSONDecodeError, AttributeError):
                    return JsonResponse(
                        {"errors": [
                            {"message": "Invalid request or malformed JSON body."}]},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                except Exception as e:
                    return JsonResponse(
                        {"errors": [
                            {"message": f"An unexpected error occurred: {str(e)}"}]},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

        response = self.get_response(request)
        return response
