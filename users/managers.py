from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, login, password, **extra_fields):
        if not login:
            raise ValueError("not_login")
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, login, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("is_staff")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("is_superuser")

        return self.create_user(login, password, **extra_fields)
