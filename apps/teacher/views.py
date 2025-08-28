from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.management.models import Semester, Lesson, LessonMaterial, Group, SemesterSubject
from apps.teacher.serializers import LessonMaterialSerializer, \
    LessonSerializer, GroupSerializer, SemesterSerializer, SemesterSubjectSerializer, UserMiniSerializer
from apps.user.models import User
from apps.user.permissions import IsTeacher


class GroupViewSet(ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = (IsTeacher,)

    def get_queryset(self):
        teacher = self.request.user
        group_ids = (
            Semester.objects
            .filter(semestersubject__teacher=teacher)
            .values_list('group_id', flat=True)
            .distinct()
        )
        return Group.objects.filter(id__in=group_ids).order_by('id')

    @action(detail=True, methods=["get"])
    def students(self, request, pk=None):
        group = self.get_object()
        queryset = User.objects.filter(studentgroup__group=group)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserMiniSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserMiniSerializer(queryset, many=True)
        return Response(serializer.data)


class SemesterViewSet(ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = (IsTeacher,)
    filterset_fields = ("order", "group", "academic_year", "is_finished",)

    def get_queryset(self):
        user = self.request.user

        return (
            self.queryset
            .filter(semestersubject__teacher=user)
            .distinct()
        )


class SemesterSubjectViewSet(ModelViewSet):
    queryset = SemesterSubject.objects.all()
    serializer_class = SemesterSubjectSerializer
    permission_classes = (IsTeacher,)
    filterset_fields = ("semester", "subject", "teacher",)

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(teacher=user)


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsTeacher,)
    filterset_fields = ("semester_subject", "lesson_type")
    search_fields = ("title",)

    def get_queryset(self):
        return self.queryset.filter(semester__teacher=self.request.user)


class LessonMaterialViewSet(ModelViewSet):
    queryset = LessonMaterial.objects.all()
    serializer_class = LessonMaterialSerializer
    permission_classes = (IsTeacher,)
    filterset_fields = ("lesson", "type")
    search_fields = ("description",)

    # parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return self.queryset.filter(lesson__semester__teacher=self.request.user).order_by('id')
