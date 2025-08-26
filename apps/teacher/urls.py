from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.teacher.views import LessonViewSet, LessonMaterialViewSet,  SemesterViewSet, GroupViewSet

router = DefaultRouter()
router.register(r'semester', SemesterViewSet, basename='semester')
router.register(r'group', GroupViewSet, basename='group')
router.register(r'lesson', LessonViewSet, basename='lesson')
router.register(r'lesson-materials', LessonMaterialViewSet, basename='lesson-material')

urlpatterns = [
    # path('group/', GroupAPIView.as_view(), name='group-list'),
    path('', include(router.urls)),
]
