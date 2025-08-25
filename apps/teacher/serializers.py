from rest_framework import serializers

from apps.management.models import Semester, Group, Lesson, LessonMaterial


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class SemesterListSerializer(serializers.ModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = Semester
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonMaterial
        fields = "__all__"
