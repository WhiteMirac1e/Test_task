from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Note
from .serializers import NoteSerializer, NoteSerializerAll


class NoteApiView(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    # Метод для вывода всех заметок
    def list(self, request):
        notes = self.queryset.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    # Метод для вывода конкретной заметки
    def retrieve(self, request, pk=None):
        # Пробуем получить заметку по указанному id(pk)
        try:
            note = self.get_object()
        # Вызываем исключение если данный id не существует
        except Exception as e:
            return Response({"error": "Не удалось найти объект"}, status=404)

        serializer = NoteSerializerAll(note)
        return Response(serializer.data)


class NotesViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    # Добавление метода POST
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        # Проверка валидности сериализатора
        if serializer.is_valid():
            serializer.save()
            return Response({'id': serializer.instance.id}, status=201)
        else:
            return Response(serializer.errors, status=400)

    # Добавление метода PUT
    def update(self, request, pk=None):
        # Пробуем обновить заметку по указанному id(pk)
        try:
            note = self.get_object()
        # Вызываем исключение если данный id не существует
        except Exception as e:
            return Response({"error": "Не удалось найти объект"}, status=404)

        serializer = NoteSerializer(note, data=request.data, partial=True)
        # Проверка валидности сериализатора
        if serializer.is_valid():
            serializer.save()
            return Response({})
        else:
            return Response(serializer.errors, status=400)

    # Добавление метода DELETE
    def delete(self, request, item_id):
        # Используем функцию для получения объекта, если объект не найден, то выводим исключение
        note = get_object_or_404(Note, id=item_id)
        note.delete()
        return Response({}, status=204)
