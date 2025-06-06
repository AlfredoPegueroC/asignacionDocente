from myapp.models import APILog
import logging

class APILogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.excluded_paths = ['/api/login', '/api/logout']

    def __call__(self, request):
        response = self.get_response(request)

        try:
            if (
                request.path.startswith("/api/") and
                request.method in ['POST', 'PUT', 'PATCH', 'DELETE'] and
                request.path not in self.excluded_paths
            ):
                user = getattr(request, 'user', None)
                username = 'Anónimo'

                if user and user.is_authenticated:
                    username = user.username
                else:
                    user = None  # Guardamos None si no está autenticado

                print(f"[LOG] {request.method} → {request.path} | Usuario: {username}")

                APILog.objects.create(
                    user=user,
                    method=request.method,
                    path=request.path,
                    status_code=response.status_code,
                    message=f"{request.method} to {request.path} por {username}"
                )

        except Exception as e:
            logging.getLogger(__name__).error(f"[Middleware Error] {e}")

        return response
