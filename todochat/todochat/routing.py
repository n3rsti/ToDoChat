from channels.auth import AuthMiddlewareStack
from channels.security.websocket import OriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
from todochat.settings import config


application = ProtocolTypeRouter({

    "websocket": OriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        ),
        config["ALLOWED_HOSTS"],
    ),
})