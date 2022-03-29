from rest_framework import response, status


class ResponseUtils(object):
    @staticmethod
    def method_not_allowed():
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @staticmethod
    def not_found(err):
        return response.Response(err, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def unauthorized(data):
        return response.Response(data, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def bad_request(data=None, return_status=status.HTTP_400_BAD_REQUEST):
        return response.Response(data if data else {}, status=return_status)

    @staticmethod
    def simple_response(data):
        return response.Response(data)

    @staticmethod
    def no_content(msg):
        return response.Response(msg, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def failed_dependency(err, status=status.HTTP_424_FAILED_DEPENDENCY):
        return response.Response(err, status=status)

    @staticmethod
    def internal_server_error(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR):
        return response.Response(err, status=status)

