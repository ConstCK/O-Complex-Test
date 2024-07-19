import datetime

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from accounts.forms import LoginForm, SignUpForm
from .forms import ForecastOrderForm
from accounts.views import sign_up, log_out, log_in
from .models import ForecastOrder


class ForecastTest(TestCase):
    def setUp(self):
        # Выполнение перед всеми тестами
        self.user_form_data_1 = {'username': 'Ivanov', 'password': 'user1234'}
        self.user_form_data_2 = {'username': 'Ivanov', 'password': 'user'}
        self.user_form_data_3 = {'username': 'Petrov',
                                 'password1': 'user9876',
                                 'password2': 'user9876'}
        self.user_form_data_4 = {'username': 'Petrov',
                                 'password1': 'user9876',
                                 'password2': 'user9870'}
        self.user_form_data_5 = {'username': 'Petrov',
                                 'password1': '123',
                                 'password2': '123'}
        self.forecast_form_data_1 = {'city': 'Moscow'}
        self.forecast_form_data_2 = {'city': 'M'}
        self.user = User.objects.create_user(username='Ivanov', password='user1234')
        self.model_data_1 = ForecastOrder.objects.create(user=self.user,
                                                         city='London',
                                                         city_lat=51.5085,
                                                         city_lon=-0.1257,
                                                         created_at=datetime.datetime.now())

    def tearDown(self):
        pass

    def test_model_creation(self):
        # Тест получения ранее созданной модели
        forecast_order = ForecastOrder.objects.get(id=1)
        self.assertEqual(str(forecast_order), 'London для Ivanov')

    def test_forecast_form_validation_successful(self):
        # Проверка валидации формы запроса прогноза погоды
        form = ForecastOrderForm(data=self.forecast_form_data_1)
        self.assertTrue(form.is_valid())

    def test_forecast_form_validation_failed(self):
        # Проверка валидации формы запроса прогноза погоды
        form = ForecastOrderForm(data=self.forecast_form_data_2)
        self.assertFalse(form.is_valid())

    def test_login_form_validation_successful(self):
        # Проверка валидации формы авторизации
        form = LoginForm(data=self.user_form_data_1)
        self.assertTrue(form.is_valid())

    def test_login_form_validation_failed(self):
        # Проверка валидации формы авторизации
        form = LoginForm(data=self.user_form_data_2)
        self.assertFalse(form.is_valid())

    def test_main_page_status(self):
        # Проверка статуса ответа для определенного url
        url = reverse('main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_main_page_template(self):
        # Проверка использования шаблона для определенного url
        url = reverse('main')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'main.html')

    def test_main_statistic_status(self):
        # Проверка использования шаблона для определенного url
        response = self.client.get('/main-statistic/')
        self.assertEqual(response.status_code, 200)

    def test_signup_successful(self):
        # Проверка функции регистрации при правильном вводе данных
        response = self.client.post('/accounts/signup/', self.user_form_data_3)
        self.assertTemplateUsed(response, 'registration/successful_registration.html')

    def test_signup_failed_1(self):
        # Проверка функции регистрации при неправильном вводе данных
        response = self.client.post('/accounts/signup/', self.user_form_data_4)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_failed_2(self):
        # Проверка функции регистрации при неправильном вводе данных 1
        response = self.client.post('/accounts/signup/', self.user_form_data_4)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_login_successful(self):
        # Проверка login функции при правильном вводе данных
        response = self.client.post('/accounts/login/', self.user_form_data_1)
        self.assertEqual(response.status_code, 302)

    def test_login_failed(self):
        # Проверка login функции при неправильном вводе данных
        response = self.client.post('/accounts/login/', self.user_form_data_2)
        self.assertTemplateUsed(response, 'registration/failed_login.html')


    def test_forecast_successful(self):
        # Проверка получения данных
        current_hour = datetime.datetime.now().hour + 1
        self.client.login(username='Ivanov', password='user1234')
        response = self.client.post('', self.forecast_form_data_1)

        self.assertEqual(response.context['hour'], current_hour)
        self.assertEqual(response.status_code, 200)

