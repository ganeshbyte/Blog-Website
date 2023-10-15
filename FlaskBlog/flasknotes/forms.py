from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flasknotes.models import User



class NoteForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired(), Length(min=2)])
    
    date_note =DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    
    content = StringField('Description', validators=[DataRequired()])
    
    submit = SubmitField('Add')
    
    

