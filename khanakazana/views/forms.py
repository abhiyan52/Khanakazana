'''
 Name: forms.py
 Description: WTF form classes for rendering forms and validation
 author: abhiyan timilsina              '''


from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, IntegerField, TextAreaField, HiddenField, SelectField, DateTimeField
from wtforms.validators import Required, Email, EqualTo, NumberRange, Regexp, Length


class Users(Form):
    name = StringField('Enter your Name', validators=[Required()])
    username = StringField('Enter user name', validators=[Required()])
    password = PasswordField('Enter a password', validators=[Required(), EqualTo('confirm')])
    confirm = PasswordField('Repeat Password')
    email = StringField('Enter your email', validators=[Required(), Email()])
    contact = StringField('Enter your contact number')
    address = TextAreaField('Enter your complete address(optional)', validators=[Length(max=100)])
    submit = SubmitField('Submit Form')


class Restaurants(Form):
    name = StringField('Enter restaurant Name', validators=[Required()])
    contact = IntegerField('Enter restaurant contact number')
    res_type = StringField('Enter restaurant type')
    minimum_order = IntegerField('Enter minimim order', validators=[Required()])
    opening_time = StringField('Enter in HH:MM:SS', validators=[Required()])
    closing_time = StringField('Enter in HH:MM:SS', validators=[Required()])
    submit = SubmitField('Submit Form')


class Items(Form):
    name = StringField('Enter Item Name', validators=[Required()])
    description = TextAreaField('Enter the description', validators=[Required(), Length(min=1, message='The length must be 30 characters')])
    price = IntegerField('Enter the Price', validators=[Required()])
    category = StringField('Enter the category of item', validators=[Required()])
    submit = SubmitField('Add Items')


class BookRestaurant(Form):
    name = StringField(label='Enter the visitor\'s name', validators=[Required()])
    number = SelectField(label='Choose Number of Persons', default=0, choices=[(1, 'One Member'),(2, 'Two Members'), (3, 'Three Members'), (4, 'Four Members')])
    date = DateTimeField(label='Enter date and time of your visit')
    submit = SubmitField('Book Now')

    
