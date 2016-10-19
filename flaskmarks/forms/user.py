from .base import Form
from .base import strip_filter

from wtforms import StringField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import validators


class UserRegisterForm(Form):
    username = StringField('Username',
                         [validators.Length(min=4, max=32)],
                         filters=[strip_filter])
    email = StringField('Email',
                      [validators.Length(min=4, max=320),
                       validators.Email(message='Not a valid email address')],
                      filters=[strip_filter])
    password = PasswordField('Password',
                             [validators.Length(min=6, max=64),
                              validators.EqualTo('confirm',
                                                 message='Passwords must\
                                                          match')],
                             filters=[strip_filter])
    confirm = PasswordField('Confirm Password',
                            filters=[strip_filter])


class UserProfileForm(UserRegisterForm):
    password = PasswordField('Password',
                             [validators.Optional(),
                              validators.Length(min=6, max=64),
                              validators.EqualTo('confirm',
                                                 message='Passwords must\
                                                          match')],
                             filters=[strip_filter])
    per_page = SelectField('Items per page',
                           coerce=int,
                           choices=[(n, n) for n in range(10, 21)])
    suggestion = SelectField('Show suggestions',
                             coerce=int,
                             choices=[(n, n) for n in range(5)])
    recently = SelectField('Recently added',
                           coerce=int,
                           choices=[(n, n) for n in range(5)])
    sort_type = SelectField('Sort type',
                            coerce=str,
                            choices=[('clicks', 'Clicks'),
                                     ('dateasc', 'Date asc'),
                                     ('datedesc', 'Date desc')])
