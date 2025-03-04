from channels.middleware import BaseMiddleware
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Acceder al header "Authorization"
        token = None
        headers = dict(scope["headers"])

        # La cabecera Authorization suele ser de la forma "Bearer <token>"
        authorization = headers.get(b'authorization', None)
        if authorization:
            # Eliminar "Bearer " del valor del header
            token = authorization.decode().split(' ')[1]

        scope["user"] = AnonymousUser()
        if token:
            try:
                # Verifica el token y asigna el usuario
                access_token = AccessToken(token)
                scope["user"] = await sync_to_async(get_user_model().objects.get)(id=access_token["user_id"])
            except Exception:
                pass

        return await super().__call__(scope, receive, send)
