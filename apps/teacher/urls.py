from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.teacher.views import SemesterListAPIView, LessonViewSet, LessonMaterialViewSet

router = DefaultRouter()
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'lesson-materials', LessonMaterialViewSet, basename='lesson-material')

urlpatterns = [
    path('semesters/', SemesterListAPIView.as_view(), name='semester-list'),
    path('', include(router.urls)),
]
