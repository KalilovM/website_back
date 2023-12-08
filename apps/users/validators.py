from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class BaseValidator:
    """
    Base class for all validators
    """

    def __init__(self, attrs: dict):
        self.attrs = attrs
        self.errors = {key: [] for key in attrs.keys()}
        self.model: User | None = None

    def add_error(self, name, value):
        self.errors[name].append(value)

    def validate(self):
        raise NotImplementedError

    def is_valid(self):
        for k, v in self.errors.items():
            if len(v) != 0:
                raise ValidationError(self.errors)
        return self.attrs


class RegisterValidator(BaseValidator):
    def validate_username(self):
        if User.objects.filter(username=self.attrs.get("username")).exists():
            self.add_error("username", "This username is already taken.")

    def validate_email(self):
        if User.objects.filter(email=self.attrs.get("email")).exists():
            self.add_error("email", "This email already exists")

    def validate(self):
        self.validate_username()
        self.validate_email()
        return self.is_valid()


class LoginValidator(BaseValidator):

    def validate_username(self):
        try:
            user = User.objects.get()
            self.model = user
        except User.DoesNotExist:
            self.add_error("username", "Username doesn't exists")

    def validate_auth(self):
        password = self.attrs.get("password")
        try:
            if not self.model.check_password(password):
                self.add_error("password", "Wrong password, try again")
        except User.DoesNotExist:
            self.add_error("username", "Username doesn't exists")

    def consolidate_data(self):
        self.attrs["email"] = self.model.email
        self.attrs["username"] = self.model.username
        self.attrs["avatar"] = self.model.avatar.url

    def validate(self):
        self.validate_username()
        self.validate_auth()
        self.consolidate_data()
        return self.is_valid()
