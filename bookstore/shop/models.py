from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password="", **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password="", **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_validator = RegexValidator(regex=r'^\+\d{11}$', message=_("Введите корректный номер"))
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=12, unique=True, null=True, validators=[phone_validator], verbose_name=_("Номер телефона"))
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, default="")
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Publisher(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'


class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    count_pages = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class BooksGenre(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Книга-Жанр'
        verbose_name_plural = 'Книги-Жанры'


class Order(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Заказ от {self.date} - {'Оплачен' if self.is_paid else 'Не оплачен'}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
