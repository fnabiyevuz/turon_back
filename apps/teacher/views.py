from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.management.models import Semester, Lesson, LessonMaterial, Group
from apps.teacher.serializers import LessonMaterialSerializer, \
    LessonSerializer, GroupSerializer, SemesterSerializer
from apps.user.permissions import IsTeacher


class GroupViewSet(ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = (IsTeacher,)

    def get_queryset(self):
        teacher = self.request.user
        group_ids = (
            Semester.objects.filter(teacher=teacher)
            .values_list('group_id', flat=True)
            .distinct()
        )
        return Group.objects.filter(id__in=group_ids).order_by('id')

    @action(detail=True, methods=["get"])
    def students(self, request, pk=None):
        group = self.get_object()
        queryset = (
            group.studentgroup_set
            .select_related("student")
            .values("student__uuid", "student__first_name", "student__last_name")
        )

        # Pagination qo‘llash
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(page)

        return Response(queryset)


class SemesterViewSet(ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = (IsTeacher,)
    filterset_fields = ("semester", "group", "subject", "teacher", "academic_year")

    # search_fields = ("title",)

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
