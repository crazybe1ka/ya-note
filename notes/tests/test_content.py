from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestListPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.another_author = User.objects.create(username='Другой автор')
        cls.note = Note.objects.create(
            title='Тестовая заметка',
            text='Просто текст.',
            author=cls.author
        )
        cls.list_url = reverse('notes:list')

    def test_pages_contains_form(self):
        """Проверяет, что на страницы создания
        и редактирования заметки передаются формы.
        """
        self.client.force_login(self.author)
        urls = (
            ('notes:edit', [self.note.slug]),
            ('notes:add', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

    def test_notes_list_for_different_users(self):
        """Проверяет список заметок
        для пользователя-автора и другого пользователя.
        """
        users = (
            (self.author, True),
            (self.another_author, False),
        )
        for user, status in users:
            self.client.force_login(user)
            with self.subTest(user=user):
                response = self.client.get(self.list_url)
                object_list = response.context['object_list']
                if status:
                    self.assertIn(self.note, object_list)
                else:
                    self.assertNotIn(self.note, object_list)
