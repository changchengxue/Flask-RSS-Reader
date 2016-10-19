from .base import Form
from .base import strip_filter

from wtforms import StringField
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import RadioField
from wtforms import validators
from wtforms import HiddenField


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
    type = RadioField('Type',
                      coerce=str,
                      choices=[('bookmark', 'Bookmark'), ('feed', 'Feed')],
                      default='bookmark')
    tags = StringField('Tags',
                     [validators.Length(min=0, max=255)],
                     filters=[strip_filter])
