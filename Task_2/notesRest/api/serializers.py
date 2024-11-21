from rest_framework import serializers
from .models import Note


# Создание сериализатора для вывода подробной информации о заметке
class NoteSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("id", "note", 'description')


# Создание сериализатора для вывода краткой информации о всех заметках
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("id", "note")
