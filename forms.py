from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class ItemForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[NumberRange(min=1,message="Enter integer"),DataRequired()])
    description = StringField('description', validators=[DataRequired()])

