from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    EMPLOYEE = 'employee'
    MANAGER = 'manager'
    ROLE_CHOICES = (
        (EMPLOYEE, 'employee'),
        (MANAGER, 'manager'),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    date_hired = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    shift_time = models.CharField(max_length=220, blank=True, null=True)
    image = models.ImageField(
        upload_to='user_images', blank=True, null=True)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.role = self.role.lower()
        if self.status:
            self.status = self.status.lower()
        if self.shift_time:
            self.shift_time = self.shift_time.lower()
        super(User, self).save(*args, **kwargs)


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    manager = models.ForeignKey(
        Manager, on_delete=models.CASCADE, related_name='manager_employee', null=True, blank=True)

    def __str__(self):
        return self.user.email
