from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required,Email
from ..models import Users

class PitchForm(FlaskForm):
    title = StringField('Pitch title',validators=[Required()])
    category = SelectField('Title', validators=[Required()],
                                    choices=[('Business','Business'),
                                            ('Software','Software'),
                                            ('Pick_Up lines','Pick_Up lines'),
                                            ('Agriculture','Agriculture'),
                                            ('Interview','Interview'),
                                            ('Product','Product'),
                                            ('Promotion','Promotion')])
    details = TextAreaField('Here goes your pitch',validators = [Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = StringField('Comment on the pitch')
    submit = SubmitField('comment')

class Update_Profile(FlaskForm):
    bio = TextAreaField('Say something about yourself...', validators = [Required()])
    submit = SubmitField('Submit')
