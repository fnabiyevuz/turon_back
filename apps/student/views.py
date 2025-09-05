from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.management.models import StudentGroup, Semester, SemesterSubject, Lesson, LessonMaterial
from apps.teacher.serializers import SemesterSerializer, SemesterSubjectSerializer, LessonSerializer, \
    LessonMaterialSerializer
from apps.user.permissions import IsStudent


class SemesterAPIView(APIView):
    permission_classes = (IsStudent,)

    def get(self, request, *args, **kwargs):
        student = request.user

        groups = StudentGroup.objects.filter(student=student).values_list("group_id", flat=True)

        semesters = Semester.objects.filter(group_id__in=groups)

        return Response(SemesterSerializer(semesters, many=True).data, status=status.HTTP_200_OK)


class SemesterSubjectListAPIView(ListAPIView):
    queryset = SemesterSubject.objects.all()
    serializer_class = SemesterSubjectSerializer
    filterset_fields = ("semester",)
    permission_classes = (IsStudent,)

    def get_queryset(self):
        user = self.request.user

        student_groups = StudentGroup.objects.filter(student=user).values_list("group_id", flat=True)

        return SemesterSubject.objects.filter(
            semester__group_id__in=student_groups,
        ).select_related("semester", "subject", "teacher")


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filterset_fields = ("semester_subject",)
    permission_classes = (IsStudent,)

    def get_queryset(self):
        user = self.request.user

        student_groups = StudentGroup.objects.filter(student=user).values_list("group_id", flat=True)

        return Lesson.objects.filter(
            semester_subject__semester__group_id__in=student_groups,
        )


class LessonMaterialListAPIView(ListAPIView):
    queryset = LessonMaterial.objects.all()
    serializer_class = LessonMaterialSerializer
    filterset_fields = ("lesson",)
    permission_classes = (IsStudent,)

    def get_queryset(self):
        user = self.request.user

        student_groups = StudentGroup.objects.filter(student=user).values_list("group_id", flat=True)

        return LessonMaterial.objects.filter(
            lesson__semester_subject__semester__group_id__in=student_groups,
        )
