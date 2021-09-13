from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email не может быть пустым')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create(email, password, **extra_fields)


class User(AbstractBaseUser):

    GENDER = (
        ('male', 'Мужчина'),
        ('female', 'Женщина')
    )

    email = models.EmailField(error_messages={'unique': 'A user with that username already exists.'}, unique=True)
    username = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, choices=GENDER, default='male')
    avatar = models.ImageField(upload_to='users/avatar', blank=True)
    birthday = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=20, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def create_activation_code(self):
        code = get_random_string(10)
        self.activation_code = code
        self.save()

    def send_activation_email(self):
        message = f'''
        Благодарим Вас за регистрацию на нашем сайте.
        Ваш код активации: {self.activation_code}
        '''
        send_mail('Активация аккаунта',
                  message,
                  'test@gmail.com',
                  [self.email],
                  )
