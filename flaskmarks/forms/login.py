from .base import Form
from .base import strip_filter

from wtforms import StringField
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import validators


class LoginForm(Form):
    username = StringField('Username or Email',
                         [validators.Length(min=4, max=255)],
                         filters=[strip_filter])
    password = PasswordField('Password',
                             [validators.Length(min=1, max=255)],
                             filters=[strip_filter])
    remember_me = BooleanField('Remember me', default=False)
