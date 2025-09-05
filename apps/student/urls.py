from django.urls import path

from apps.student.views import SemesterAPIView, SemesterSubjectListAPIView, LessonListAPIView, LessonMaterialListAPIView

urlpatterns = [
    path('semesters/', SemesterAPIView.as_view()),
    path('subjects/', SemesterSubjectListAPIView.as_view()),
    path('lessons/', LessonListAPIView.as_view()),
    path('lessons/', LessonListAPIView.as_view()),
    path('lesson-materials/', LessonMaterialListAPIView.as_view()),
]
