from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter

from .views import ResourceViewSet, SkillViewSet, ResourceAvailabilityViewSet

router = routers.DefaultRouter()
router.register("resources", ResourceViewSet)
router.register("skills", SkillViewSet)

resource_avl_router = NestedDefaultRouter(
    router,
    "resources",
    lookup="resource",
)

resource_avl_router.register("availability", ResourceAvailabilityViewSet, basename='resource_availability')

router_urls = router.urls + resource_avl_router.urls

urlpatterns = router_urls
