from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Follow, Group, Post, User


class PostsViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Test-name')

        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug-text',
        )
        cls.posts = [
            Post(
                author=cls.user,
                text='Тестовый пост {i}',
                group=cls.group)
            for i in range(13)
        ]
        cls.group_new = Group.objects.create(
            title='Тестовая группа1',
            slug='slug-text1',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}): 'posts/group_list.html',
            reverse('posts:profile',
                    kwargs={'username': self.user.username}):
            'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.id}):
            'posts/post_detail.html',
            reverse('posts:post_create'):
            'posts/create_post.html',
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post.id}):
            'posts/create_post.html',
            '/unexisting_page/': 'core/404.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object.text, 'Тестовый пост')

    def test_group_list_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
        )
        first_object = response.context['group']
        group_title = first_object.title
        group_slug = first_object.slug
        self.assertEqual(group_title, self.group.title)
        self.assertEqual(group_slug, self.group.slug)

    def test_post_detail_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={
                'post_id': self.post.id}),
        )
        first_object = response.context['post']
        posts = first_object.text
        self.assertEqual(posts, 'Тестовый пост')
        self.assertEqual(response.context['author'].username,
                         self.user.username)

    def test_post_create_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_edit_context(self):
        """Шаблон edit_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
        )
        form_fields = {
            'text': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_first_page(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_group_list_first_page(self):
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
        )
        self.assertEqual(len(response.context['page_obj']), 0)

    def test_profile_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username}),
        )
        first_object = response.context['page_obj'][0]
        posts = first_object.text
        self.assertEqual(posts, self.post.text)
        self.assertEqual(response.context['author'].username,
                         self.user.username)

    def test_profile_first_page(self):
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username}),
        )
        self.assertEqual(len(response.context['page_obj']), 1)


class FollowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Test_user')
        cls.author = User.objects.create_user(username='Test_author')
        cls.group = Group.objects.create(
            title='TestGroup',
            slug='offtopic',
        )
        cls.post = Post.objects.create(
            text='Test_text',
            author=cls.author,
            group=cls.group,
        )

    def setUp(self):
        self.guest = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(FollowTests.user)

    def test_follow_users_for_authorized_client(self):
        follow_counter = Follow.objects.count()
        self.assertRedirects(
            self.guest.get(reverse(
                'posts:profile_follow',
                kwargs={'username': self.author.username}),
            ),
            f'/auth/login/?next=/profile/{self.author.username}/follow/',
        )
        self.authorized_client.get(reverse(
            'posts:profile_follow',
            kwargs={'username': self.author.username}),
        )
        self.assertTrue(
            Follow.objects.filter(
                user=self.user,
                author=self.author,
            ).exists(),
        )
        self.authorized_client.get(reverse(
            'posts:profile_unfollow',
            kwargs={'username': self.author.username}),
        )
        self.assertEqual(Follow.objects.count(), follow_counter)

    def test_user_follow_posts_exist_at_desire_location(self):
        self.authorized_client.get(reverse(
            'posts:profile_follow',
            kwargs={'username': self.author.username}),
        )
        Post.objects.create(
            text='text',
            author=self.author,
        )
        response = self.authorized_client.get(reverse('posts:follow_index'))
        content = response.context['page_obj'][0]
        self.assertEqual(content.text, 'text')
