from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import Length,Email,EqualTo,DataRequired
from simpledu.models import db,User
from wtforms import ValidationError
from wtforms import TextAreaField,IntegerField
from simpledu.models import Course
from wtforms.validators import URL,NumberRange


class RegisterForm(FlaskForm):
    username=StringField('username',validators=[DataRequired(),Length(3,24)])
    email=StringField('email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired(),Length(6,24)])
    repeat_password=PasswordField('repeat_password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('submit')
    def create_user(self):
        user=User()
        user.username=self.username.data
        user.email=self.email.data
        user.password=self.password.data
        db.session.add(user)
        db.session.commit()
        return user
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username is existed')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email is existed')




class LoginForm(FlaskForm):
    email=StringField('email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired(),Length(6,24)])
    remember_me=BooleanField('remember_me')
    submit=SubmitField('submit')
    def validate_email(self,field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('email is existed')

    def validate_password(self,field):
        user=User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('password is wrong')



class CourseForm(FlaskForm):
    name=StringField('course name',validators=[DataRequired(),Length(5,32)])
    description=TextAreaField('course description',validators=[DataRequired(),Length(20,256)])
    image_url=StringField('headline picture',validators=[DataRequired(),URL()])
    author_id=IntegerField('author ID',validators=[DataRequired(),NumberRange(min=1,message='illeagel use id')])
    submit=SubmitField('submit')
    def validate_author_id(self,field):
        if not User.query.get(self.author_id.data):
            raise ValidationError('use is not existed')

    def create_course(self):
        course=Course()
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self,course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course




























