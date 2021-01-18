from django.test import TestCase
from app.models import Server
from .models import Task
from django.contrib.auth.models import User

# Create your tests here.
class TestTaskModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username="test1", id=1)
        user2 = User.objects.create(username="test2", id=2)
        server = Server.objects.create(name="test_name", id=123, owner=user1)
        server.users.add(user2)
        task = Task.objects.create(task_id="123", pk=1, 
            description="this is test description",
            author=user1,
            server=server
        )
        task.assigned_for.add(user2)
    
    def test_task_id_max_length(self):
        task = Task.objects.get(pk=1)
        max_length = task._meta.get_field('task_id').max_length
        self.assertEqual(max_length, 50)
    
    def test_title_max_length(self):
        task = Task.objects.get(pk=1)
        max_length = task._meta.get_field('title').max_length
        self.assertEqual(max_length, 20)
    
    def test_absolute_url(self):
        task = Task.objects.get(pk=1)
        expected_str = f'/server/{task.server.id}/tasks/1/'
        self.assertEqual(task.get_absolute_url(), expected_str)
    
    def test_str(self):
        task = Task.objects.get(pk=1)
        expected_str = f'{task.server.name} #{task.task_id}'
        self.assertEqual(str(task), expected_str)