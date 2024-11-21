Создание rest Сервера на DRF
Для запуска сервера на определенном порту необходимо дать команду, где 5577 - номер порта

python manage.py runserver 5577

1. Установим Django и Django REST Framework:
   
pip install django djangorestframework
  
2. Создадим новый проект Django:
   
django-admin startproject notesRest
   
3. Перейдем в созданный каталог
   
cd notesRest

4. Создадим приложение
   
python manage.py startapp api

5. Добавим приложение и REST Framework в файл settings.py
    
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'rest_framework',
]

6. Откроем файл api/models.py и создадим модель Note:
    
from django.db import models


class Note(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    note = models.CharField(max_length=120)
    description = models.TextField(max_length=1024)

    def __str__(self):
        return self.note
7. Проведем миграции
   
python manage.py makemigrations
python manage.py migrate

8. Создадим сериализатор, который будет испольоваться для преобразования данных в формат JSON
   Создадим файл api/serializers.py и добавим следующий код:
   
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
        
9. Создадим представления 
Откроем файл api/views.py и добавим следующие представления:

from .models import Note
from .serializers import NoteSerializer, NoteSerializerAll


class NoteApiView(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
10. Настроим url маршруты с помощь router
Откроем файл notesRest/url.py и добавим следующие маршруты:

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api import views

# С помощью router мы можем задать один маршрут для всех методов
router = routers.DefaultRouter()
router.register(r'notes', views.NoteApiView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(router.urls)),
]
11. Добавим методы GET, POST, DELETE, PUT

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
