from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.management.models import StudentGroup, Semester
from apps.teacher.serializers import SemesterSerializer
from apps.user.permissions import IsStudent


# Create your views here.
class SemesterAPIView(APIView):
    permission_classes = (IsStudent,)

    def get(self, request, *args, **kwargs):
        student = request.user

        groups = StudentGroup.objects.filter(student=student).values_list("group_id", flat=True)

        semesters = Semester.objects.filter(group_id__in=groups)



        return Response(SemesterSerializer(semesters, many=True).data, status=status.HTTP_200_OK)
