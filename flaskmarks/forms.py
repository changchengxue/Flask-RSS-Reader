from flask_wtf import Form

from wtforms import StringField
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import validators
from wtforms import HiddenField


def strip_filter(x):
    if x:
        return x.strip()
    else:
        return


pmm = 'Passwords must match'


class LoginForm(Form):
    username = StringField('Username or Email',
                         [validators.Length(min=4, max=255)],
                         filters=[strip_filter])
    password = PasswordField('Password',
                             [validators.Length(min=1, max=255)],
                             filters=[strip_filter])
    remember_me = BooleanField('Remember me', default=False)


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
                                                 message=pmm)],
                             filters=[strip_filter])
    confirm = PasswordField('Confirm Password',
                            filters=[strip_filter])


class UserProfileForm(UserRegisterForm):
    password = PasswordField('Password',
                             [validators.Optional(),
                              validators.Length(min=6, max=64),
                              validators.EqualTo('confirm',
                                                 message=pmm)],
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


class MarkForm(Form):
    referrer = HiddenField([validators.URL(require_tld=False)])
    title = StringField('Title',
                      [validators.Length(min=0, max=255)],
                      filters=[strip_filter])
    url = StringField('URL',
                    [validators.Length(min=4, max=512),
                     validators.URL(require_tld=False,
                                    message='Not a valid URL')],
                    filters=[strip_filter])
    type = StringField('Type',
                      coerce=str,
                      choices=[('bookmark', 'Bookmark'), ('feed', 'Feed')],
                      default='bookmark')
    tags = StringField('Tags',
                     [validators.Length(min=0, max=255)],
                     filters=[strip_filter])
