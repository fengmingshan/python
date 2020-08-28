from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from flask_wtf import FlaskForm
from flask_uploads import UploadSet


excel_files = set(['xls', 'xlsx', 'csv'])
excels = UploadSet('excels', excel_files)

class UploadForm(FlaskForm):
    excel = FileField(validators=[FileAllowed(excels, u'Only allowed Excel files!'), FileRequired(u'Choose a file!')])
    submit = SubmitField(u'Upload')
