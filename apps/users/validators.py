from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class BaseValidator:
    """
    Base class for all validators
    """

    def __init__(self, attrs: dict):
        self.errors = {}
        self.attrs = attrs

    def add_error(self, name, value):
        self.errors[name] = value

    def validate(self):
        raise NotImplementedError

    def is_valid(self):
        if self.errors:
            raise ValidationError(self.errors)
        return self.attrs


class RegisterValidator(BaseValidator):
    def validate_username(self):
        if User.objects.filter(username=self.attrs.get("username")).exists():
            self.add_error("username", "This username already exists")

    def validate_email(self):
        if User.objects.filter(email=self.attrs.get("email")).exists():
            self.add_error("email", "This email already exists")

    def validate(self):
        self.validate_username()
        self.validate_email()
        return self.is_valid()


class LoginValidator(BaseValidator):
    def validate_username(self):
        user = User.objects.filter(username=self.attrs.get("username"))
        if not user.exists():
            self.add_error("username", "Username doesn't exists")

    def validate_auth(self):
        username = self.attrs.get("username")
        password = self.attrs.get("password")
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                self.add_error("password", "Wrong password, try again")
        except User.DoesNotExist:
            self.add_error("username", "Username doesn't exists")

    def validate(self):
        self.validate_username()
        self.validate_auth()
        return self.is_valid()
