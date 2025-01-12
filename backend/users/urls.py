from django.urls import path

from .views import ServiceHealthView, UserViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter(trailing_slash=False)
router.register('users', UserViewSet)

urlpatterns = [
    path("health", ServiceHealthView.as_view())
]
urlpatterns += router.urls