from django.test import TestCase
from .models import Server, Channel
from django.contrib.auth.models import User

# Create your tests here.
class ServerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username="test1", id=1)
        user1.set_password('test')
        user1.save()
        server = Server.objects.create(name="test_name", id=123, owner=user1)
        server.save()

    def test_name_length(self):
        server = Server.objects.get(id=123)
        max_length = server._meta.get_field('name').max_length
        self.assertEqual(max_length, 20)

    def test_id_length(self):
        server = Server.objects.get(id=123)
        max_length = server._meta.get_field('id').max_length
        self.assertEqual(max_length, 18)

    def test_get_absolute_url(self):
        server = Server.objects.get(id=123)
        self.assertEqual(server.get_absolute_url(), '/server/123/')

    def test_owner_in_users(self):
        server = Server.objects.get(id=123)
        self.assertTrue(server.owner in server.users.all())

    def test_str(self):
        server = Server.objects.get(id=123)
        expected_str = f'{server.name} server'
        self.assertEqual(str(server), expected_str)
    
    def test_default_img(self):
        server = Server.objects.get(id=123)
        self.assertEqual(server.image, 'default.png')


class ChannelModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username="test1", id=1)
        user1.set_password('test')
        user1.save()
        server = Server.objects.create(name="test_name", id=123, owner=user1)
        server.save()
        channel = Channel.objects.create(server=server, name="test_channel", pk=1234)

    def test_name_length(self):
        channel = Channel.objects.get(pk=1234)
        max_length = channel._meta.get_field('name').max_length
        self.assertEqual(max_length, 20)

    def get_absolute_url(self):
        channel = Channel.objects.get(pk=1234)
        self.assertEqual(channel.get_absolute_url(), '/server/123/test_channel')

    def test_str(self):
        channel = Channel.objects.get(pk=1234)
        expected_str = f'Server: {channel.server.name}, Channel: {channel.name}'
        self.assertEqual(str(channel), expected_str)