from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        account = self.model(
            email=self.normalize_email(email),
            profile_id = kwargs.get('user')
        )
        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)
        account.is_admin = True
        account.save()
        return account


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=70, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'app'

    @classmethod
    def create_userprofile(cls, **kwargs):
        try:
            user = Profile.objects.create(username=kwargs.get('username'))

            user_profile = Account.objects.create_user(
                kwargs.get('email'),
                password=kwargs.get(password),
                user=user
            )

        return user_profile
        except IntegrityError:
            return None

    @classmethod
    def create_orgprofile(cls, **kwargs):
        pass


class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=70, blank=True)
    last_name = models.CharField(max_length=70, blank=True)
    is_admin = models.BooleanField(default=False)
    profile_id = models.ForeignKey(Profile)
    objects = AccountManager()
    USERNAME_FIELD = 'email'

    class Meta:
        app_label = 'app'


    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name
