from django.test import TestCase
from shop.models import Category, Product
from django.urls import reverse, resolve
from shop.views import product_list, product_detail
from django.contrib.auth.models import User

class UserAuthTests(TestCase):
    def setUp(self):
        self.signup_url = reverse('user_profile:signup')
        self.login_url = reverse('user_profile:login')
        self.profile_url = reverse('user_profile:profile')
        self.logout_url = reverse('user_profile:logout')
        self.user_data = {
            'first_name': '123',
            'last_name': '456',
            'username': 'testuser',
            'password': 'testpassword123%',
            'email': 'test@mail.com'
        }

    def test_signup(self):
        """ Проверяет, что новый пользователь может зарегистрироваться успешно """
        response = self.client.post(self.signup_url, {
            'first_name': self.user_data['first_name'],
            'last_name': self.user_data['last_name'],
            'username': self.user_data['username'],
            'password1': self.user_data['password'],
            'password2': self.user_data['password'],
            'email': self.user_data['email']
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username=self.user_data['username']).exists())

    def test_login(self):
        """ Проверяет, что пользователь может войти в систему после регистрации """
        self.client.post(self.signup_url, {
            'username': self.user_data['username'],
            'password1': self.user_data['password'],
            'password2': self.user_data['password'],
            'email': self.user_data['email']
        })
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        })
        self.assertEqual(response.status_code, 200)

    def test_profile_access(self):
        """ Проверяет, что пользователь может получить доступ к своей странице профиля после входа """
        self.client.post(self.signup_url, {
            'username': self.user_data['username'],
            'password1': self.user_data['password'],
            'password2': self.user_data['password'],
            'email': self.user_data['email']
        })
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)

class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='<PASSWORD>')

    def test_get_profile_view(self):
        """ Проверяет, что вьюха профиля возвращает правильный шаблон и данные пользователя """
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_profile:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile/profile.html')
        self.assertContains(response, self.user.username)

    def test_edit_profile_view(self):
        """ Проверяет, что вьюха редактирования профиля возвращает правильный шаблон и данные пользователя """
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_profile:edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile/edit.html')
        self.assertContains(response, self.user.username)

    def test_edit_profile_form_valid(self):
        """ Проверяет, что форма редактирования профиля работает правильно при допустимых данных """
        self.client.force_login(self.user)
        form_data = {'username': 'new_username', 'email': 'new_email@example.com'}
        response = self.client.post(reverse('user_profile:edit'), form_data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'new_username')
        self.assertEqual(self.user.email, 'new_email@example.com')

    def test_edit_profile_form_invalid(self):
        """ Проверяет, что форма редактирования профиля отображает ошибки при недопустимых данных """
        self.client.force_login(self.user)
        form_data = {}
        response = self.client.post(reverse('user_profile:edit'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile/edit.html')
        self.assertContains(response, 'This field is required.')

class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """ Создает тестовые данные для тестов модели Category """
        Category.objects.create(name='Test Category', slug='test-category')

    def test_category_creation(self):
        """ Проверяет, что категория создается с правильным именем и слагом """
        category = Category.objects.get(id=1)
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.slug, 'test-category')

class TestUrls(TestCase):
    def test_product_list_url_resolves(self):
        """ Проверяет, что URL-адрес для списка продуктов соответствует представлению product_list """
        url = reverse('shop:product_list')
        self.assertEqual(resolve(url).func, product_list)

    def test_product_detail_url_resolves(self):
        """ Проверяет, что URL-адрес продукта соответствует представлению product_detail """
        category = Category.objects.create(name='Test Category', slug='test-category')
        product = Product.objects.create(category=category, name='Test product', slug='test-product', price=10.00)

        url = reverse('shop:product_detail', args=[product.id, product.slug])
        self.assertEqual(resolve(url).func, product_detail)

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """ Создает тестовые данные для тестов модели Product """
        category = Category.objects.create(name='Test Category', slug='test-category')
        Product.objects.create(category=category, name='Test product', slug='test-product', price=10.00)

    def test_name_label(self):
        """ Проверяет, что метка поля 'name' модели Product равна 'Name' """
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Name')

    def test_slug_label(self):
        """ Проверяет, что метка поля 'slug' модели Product равна 'Link' """
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'Link')

    def test_object_name_is_name(self):
        """ Проверяет, что строковое представление объекта Product равно его имени """
        product = Product.objects.get(id=1)
        expected_object_name = product.name
        self.assertEqual(expected_object_name, str(product))

    def test_product_creation(self):
        """ Проверяет, что продукт создается с правильными данными """
        product = Product.objects.get(id=1)
        self.assertEqual(product.name, 'Test product')
        self.assertEqual(product.slug, 'test-product')
        self.assertEqual(product.price, 10.00)
        self.assertEqual(product.category.name, 'Test Category')

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """ Создает тестовые данные для тестов модели User """
        User.objects.create_user(username='testuser', password='testpassword123')

    def test_user_creation(self):
        """ Проверяет, что пользователь создается с правильным именем пользователя """
        user = User.objects.get(id=1)
        self.assertEqual(user.username, 'testuser')

    def test_object_name_is_username(self):
        """ Проверяет, что значение объекта User равно его имени пользователя """
        user = User.objects.get(id=1)
        expected_object_name = user.username
        self.assertEqual(expected_object_name, str(user))

class UserDeletionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """ Создает тестовые данные для теста удаления пользователя """
        cls.user = User.objects.create_user(username='testuser3', email='testuser3@example.com', password='<PASSWORD>')

    def test_user_deletion(self):
        """ Проверяет, что пользователь может быть успешно удален из базы данных """
        self.user.delete()
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)

