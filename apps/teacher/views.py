from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from apps.management.models import Semester, Lesson, LessonMaterial
from apps.teacher.serializers import SemesterListSerializer, LessonMaterialSerializer, \
    LessonSerializer
from apps.user.permissions import IsTeacher


class SemesterListAPIView(ListAPIView):
    queryset = Semester.objects.all()
    serializer_class = SemesterListSerializer
    permission_classes = (IsTeacher,)

    def get_queryset(self):
        return self.queryset.filter(teacher=self.request.user)


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsTeacher,)
    filterset_fields = ("semester", "lesson_type")
    search_fields = ("title",)

    def get_queryset(self):
        return self.queryset.filter(semester__teacher=self.request.user)


class LessonMaterialViewSet(ModelViewSet):
    queryset = LessonMaterial.objects.all()
    serializer_class = LessonMaterialSerializer
    permission_classes = (IsTeacher,)
    filterset_fields = ("lesson", "type")
    search_fields = ("description",)

    def get_queryset(self):
        return self.queryset.filter(lesson__semester__teacher=self.request.user)
