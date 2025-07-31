from rest_framework import routers

from .views import ManagerViewSet

router = routers.DefaultRouter()
router.register("managers", ManagerViewSet)

urlpatterns = router.urls
