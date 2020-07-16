from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import PitchForm,CommentForm,Update_Profile
from ..models import User,Pitch,Comment,PhotoProfile
from flask_login import login_required,current_user
from .. import db,photos
import markdown2

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    pitch = Pitch()
    title = 'Home - 60"pitch'

    return render_template('index.html',pitch = pitch, title = title)

@main.route('/pitches', methods = ["GET","POST"])
@login_required
def pitches():
    '''
    Function to display pitches page
    '''
    all_pitches = Pitch.query.all()

    return render_template('pitches.html',all=all_pitches)

@main.route('/interview')
def interview():
    comment = Comment.query.all()
    interview = Pitch.query.filter_by(category='Interview').all()
    return render_template('interview.html',interview=interview, comment=comment)

@main.route('/promotion')
def promotion():
    comment = Comment.query.all()
    promotion = Pitch.query.filter_by(category = 'Promotion').all()
    return render_template('promotion.html',promotion=promotion,comment=comment)

@main.route('/product')
def product():
    comment = Comment.query.all()
    product = Pitch.query.filter_by(category = 'Product').all()
    return render_template('product.html',product=product,comment=comment)

@main.route('/pickup')
def pickup():
    comments = Comment.query.all()
    pickup = Pitch.query.filter_by(category = 'Pick_Up lines').all()
    return render_template('pickup.html', pickup=pickup,comments=comments)

@main.route('/software')
def software():
    comments = Comment.query.all()
    software = Pitch.query.filter_by(category = 'Software').all()
    return render_template('software.html', software=software,comments=comments)

@main.route('/agriculture')
def agri():
    comments = Comment.query.all()
    agri = Pitch.query.filter_by(category = 'Agriculture').all()
    return render_template('agri.html',agri=agri,comments=comments)

@main.route('/business')
def business():
    comments = Comment.query.all()
    business = Pitch.query.filter_by(category = 'Business').all()
    return render_template('business.html',business=business,comments=comments)    

@main.route('/pitch/<int:pitch_id>',methods = ['GET','POST'])
@login_required
def pitch(pitch_id):
    '''
    View pitch page function that returns the movie details page and its data
    '''
    pitch = Pitch.query.filter_by(id = pitch_id)
    comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    comment_form = CommentForm()
    user = current_user.username
    if comment_form.validate_on_submit():
        comment = comment_form.comment.data
        new_comment = Comment(comment=comment,pitch_id=pitch_id,user_id=current_user.id)
        new_comment.save_comment()
        return redirect(url_for('.pitch',pitch_id = pitch_id))

    return render_template('pitch.html',pitch = pitch,comments = comments,comment_form = comment_form,user=user,pitch_id=pitch_id)

@main.route('/pitch/new/', methods = ['GET','POST'])
@login_required
def new_pitch():
    form = PitchForm()
    title = "new pitch"
    if form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        details = form.details.data
        new_pitch = Pitch(title=title,details=details,category=category)
        new_pitch.save_pitch()
        return redirect(url_for('main.pitches'))
    return render_template('new_pitch.html',title = title, pitch_form=form)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)
    return render_template("Profile/profile.html", user = user)

@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def update_profile(name):
    user = User.query.filter_by(username = name).first()
    if user is None:
        abort(404)
    form = Update_Profile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile',uname=user.username))

    return render_template('Profile/update.html', form=form)
    
@main.route('/user/<uname>/update_pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
