from django.test import TestCase
from django.contrib.auth.models import User
from users.models import UsersMessage, UsersChat


class TestProfileModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username="test1", id=1)
        user1.set_password('test')
        user2 = User.objects.create(username="test2", id=2)
        user2.set_password('test')
        user1.profile.friends.add(user2)
        user2.profile.friends.add(user1)

    def test_description_max_length(self):
        user1 = User.objects.get(id=1)
        max_length = user1.profile._meta.get_field('description').max_length
        self.assertEqual(max_length, 100)

    def test_str(self):
        user1 = User.objects.get(id=1)
        expected_str = f'{user1.username} Profile'
        self.assertEqual(str(user1.profile), expected_str)

    def test_default_image(self):
        user1 = User.objects.get(id=1)
        self.assertEqual(user1.profile.image, 'default.png')

    def test_default_background(self):
        user1 = User.objects.get(id=1)
        self.assertEqual(user1.profile.background, 'default_background.jpg')


class TestUsersMessageModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username="test1", id=1)
        user1.set_password('test')
        user2 = User.objects.create(username="test2", id=2)
        user2.set_password('test')
        user1.profile.friends.add(user2)
        user2.profile.friends.add(user1)
        chat = UsersChat.objects.create(id="1")
        chat.users.add(user1, user2)
        message = UsersMessage.objects.create(id="123", chat=chat,
                                              content="test message",
                                              author=user1
                                              )

    def test_content_max_length(self):
        message = UsersMessage.objects.get(id="123")
        max_length = message._meta.get_field('content').max_length
        self.assertEqual(max_length, 200)
