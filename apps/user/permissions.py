from rest_framework.permissions import BasePermission

from .models import RoleType


class IsStudent(BasePermission):
    """
    Allows access only to users with the Student role.
    """

    def has_permission(self, request, view):
        return (
                request.user
                and request.user.is_authenticated
                and request.user.role == RoleType.STUDENT
        )


class IsTeacher(BasePermission):
    """
    Allows access only to users with the Teacher role.
    """

    def has_permission(self, request, view):
        return (
                request.user
                and request.user.is_authenticated
                and request.user.role == RoleType.TEACHER
        )
