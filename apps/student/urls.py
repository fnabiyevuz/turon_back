from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.teacher.views import LessonViewSet, LessonMaterialViewSet,  SemesterViewSet, GroupViewSet

router = DefaultRouter()
router.register(r'semester', SemesterViewSet, basename='semester')

urlpatterns = [
    # path('group/', GroupAPIView.as_view(), name='group-list'),
    path('', include(router.urls)),
]
