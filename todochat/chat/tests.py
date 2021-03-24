from channels.testing import ChannelsLiveServerTestCase
from django.test import TestCase
from selenium import webdriver
from .models import ChannelMessage
from app.models import Server, Channel
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.auth.models import User
from unittest import skip


@skip("Not working with Travis CI yet")
class ChatTests(ChannelsLiveServerTestCase):
    serve_static = True  # emulate StaticLiveServerTestCase

    def setUp(self):
        user1 = User.objects.create(username="test1", id=1)
        user1.set_password('test')
        user2 = User.objects.create(username="test2", id=2)
        user2.set_password('test')
        user1.profile.friends.add(user2)
        user2.profile.friends.add(user1)
        user1.save()
        user2.save()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            # NOTE: Requires "chromedriver" binary to be installed in $PATH
            clsOptions = webdriver.ChromeOptions()
            clsOptions.add_argument("--no-sandbox")
            clsOptions.add_argument("--disable-setuid-sandbox")
            clsOptions.add_argument("--disable-dev-shm-using")
            clsOptions.add_argument("--disable-extensions")
            clsOptions.add_argument("--disable-gpu")
            cls.driver = webdriver.Chrome(ChromeDriverManager().install())
        except:
            super().tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_when_chat_message_posted_then_seen_by_everyone_in_same_room(self):
        try:
            self._enter_chat_room('test2', 1)

            self._open_new_window()
            self._enter_chat_room('test1', 2)

            self._switch_to_window(0)
            self._post_message('hello')
            WebDriverWait(self.driver, 2).until(lambda _:
                                                'hello' in self._chat_log_value,
                                                'Message was not received by window 1 from window 1')
            self._switch_to_window(1)
            WebDriverWait(self.driver, 2).until(lambda _:
                                                'hello' in self._chat_log_value,
                                                'Message was not received by window 2 from window 1')
        finally:
            self._close_all_new_windows()

    def test_when_chat_message_posted_then_not_seen_by_anyone_in_different_room(self):
        try:
            self._enter_chat_room('test2', 1)

            self._open_new_window()
            self._enter_chat_room('test1', 2)
            self._switch_to_window(0)
            self._post_message('hello')
            WebDriverWait(self.driver, 2).until(lambda _:
                                                'hello' in self._chat_log_value,
                                                'Message was not received by window 1 from window 1')

            self._switch_to_window(1)
            self._post_message('world')
            WebDriverWait(self.driver, 2).until(lambda _:
                                                'world' in self._chat_log_value,
                                                'Message was not received by window 2 from window 2')
            self.assertTrue('hello' not in self._chat_log_value,
                            'Message was improperly received by window 2 from window 1')
        finally:
            self._close_all_new_windows()

    # === Utility ===

    def _enter_chat_room(self, room_name, index):
        self.driver.get(self.live_server_url + "/login")
        username_box = self.driver.find_element_by_css_selector("#id_username")
        password_box = self.driver.find_element_by_css_selector("#id_password")
        username_box.send_keys(f'test{index}')
        password_box.send_keys('test')
        password_box.submit()
        self.driver.get(self.live_server_url + f'/profile/{room_name}/chat/')
        """ ActionChains(self.driver).send_keys(room_name + '\n').perform()
        ActionChains(self.driver).send_keys('test').perform() """
        WebDriverWait(self.driver, 2).until(lambda _:
                                            room_name in self.driver.current_url)

    def _open_new_window(self):
        self.driver.execute_script('window.open("about:blank", "_blank");')
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def _close_all_new_windows(self):
        while len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.execute_script('window.close();')
        if len(self.driver.window_handles) == 1:
            self.driver.switch_to.window(self.driver.window_handles[0])

    def _switch_to_window(self, window_index):
        self.driver.switch_to.window(self.driver.window_handles[window_index])

    def _post_message(self, message):
        ActionChains(self.driver).send_keys(message + '\n').perform()

    @property
    def _chat_log_value(self):
        return self.driver.find_element_by_css_selector('.chat-log__li:nth-last-child(1)').get_attribute('innerText')


class ChannelModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username="test1", id=1)
        user2 = User.objects.create(username="test2", id=2)
        server = Server.objects.create(name="test_name", id=123, owner=user1)
        server.users.add(user2)
        channel = Channel.objects.create(server=server, name="test_channel", pk=2)
        message = ChannelMessage.objects.create(id="123", channel=channel, content="test message", author=user1)
        message2 = ChannelMessage.objects.create(id="1234", channel=channel, content="test message2", author=user2)

    def test_content_max_length(self):
        message = ChannelMessage.objects.get(pk="123")
        max_length = message._meta.get_field('content').max_length
        self.assertEqual(max_length, 200)
