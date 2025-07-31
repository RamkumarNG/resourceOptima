from rest_framework import routers

from .views import ProjectViewSet

router = routers.DefaultRouter()
router.register("projects", ProjectViewSet, basename='project')

urlpatterns = router.urls
