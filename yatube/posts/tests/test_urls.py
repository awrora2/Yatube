from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='the_group',
        )
        cls.post = Post.objects.create(
            author=User.objects.create_user(username='test_name'),
            text='Тестовый пост',
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='name')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.user_second = self.post.author
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(self.user_second)

    def test_pages_urls_for_guest_users(self):
        """Тест доступности страниц guest пользователям"""
        urls = [
            reverse('posts:profile', kwargs={'username': self.user.username}),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:index'),
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}),
        ]
        for address in urls:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_urls_for_auth_users(self):
        """Тест доступности страниц auth пользователям"""
        urls = [
            reverse('posts:profile', kwargs={'username': self.user.username}),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:index'),
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}),
        ]
        for address in urls:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_for_auth_users(self):
        """Тест доступности /create/ auth пользователям"""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unexisting_page_for_auth_users(self):
        """Тест доступности unexisting auth пользователям"""
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_unexisting_page_for_guest_users(self):
        """Тест доступности unexisting guest пользователям"""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_edit(self):
        """Тест доступности редактирования Автору поста"""
        response = self.authorized_client_author.get(
            reverse('posts:post_edit', kwargs={
                'post_id': self.post.id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_redirect_anonymous_on_auth_login(self):
        """Страница по адресу /create/ перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(response, ('/auth/login/?next=/create/'))

    def test_edit_url_redirect_anonymous_on_posts_login(self):
        """Страница по адресу /post_id/edit/ перенаправит анонимного
        пользователя на страницу поста.
        """
        response = self.guest_client.get(
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post.id}), follow=True)
        self.assertRedirects(response, (
            f'/auth/login/?next=/posts/{self.post.id}/edit/'))

    def test_edit_url_redirect_auth_not_author_on_post_detail(self):
        """Страница по адресу /post_id/edit/ перенаправит
        неавтора поста на свою страницу.
        """
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={
                'post_id': self.post.id}), follow=True)
        self.assertRedirects(response,
                             (f'/profile/{self.user.username}/'))

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={
                'slug': self.group.slug}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={
                'username': self.user}): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={
                'post_id': self.post.id}): 'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}):
            'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(template=template):
                response = self.authorized_client_author.get(address)
                self.assertTemplateUsed(response, template)
