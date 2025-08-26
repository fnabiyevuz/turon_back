from rest_framework import serializers

from apps.management.models import Semester, Group, Lesson, LessonMaterial, Direction


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ('id', 'name', 'code', 'department', 'type')


class GroupSerializer(serializers.ModelSerializer):
    direction = DirectionSerializer()

    class Meta:
        model = Group
        fields = ('id', 'name', 'direction', 'type', 'course')


class SemesterSerializer(serializers.ModelSerializer):
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
