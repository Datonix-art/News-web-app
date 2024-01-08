from datetime import datetime
from os import path

from flask import render_template, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import desc

from extensions import app, db, admin
from admin_views import InformationAdminModelView, UserAdminModelView, PostInfoComments
from forms import ChangePostForm, PasswordChangeForm, PostArticleForm, PostCommentForm, SignupForm, LoginForm, UsernameChangeForm
from models import CommentModel, PostModel, UserModel, generate_password_hash

admin.add_view(UserAdminModelView(UserModel, db.session, endpoint='User_panel', category='User')) 
admin.add_view(InformationAdminModelView(PostModel, db.session, endpoint='Post_panel', category='Post'))
admin.add_view(PostInfoComments(CommentModel, db.session, endpoint='Comment_panel', category='Post'))

@app.route('/')
def default_route():
    return redirect('/1')

@app.route('/<int:page_id>') 
def home(page_id):
   all_table_information = PostModel.query.order_by(PostModel.id.desc()).limit(5)
   all_information = PostModel.query.paginate(per_page=5, page=page_id)
   return render_template('base.html', all_table_information = all_table_information, all_information=all_information)

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostArticleForm() 
    if form.validate_on_submit():
      file = form.image.data
      filename = file.filename
      
      information = PostModel(image=filename, title=form.title.data, description=form.description.data, date=datetime.utcnow(), user_id=current_user.id)
      
      file.save((path.join(app.root_path, 'static/img', filename)))

      information.create()
      return redirect('/1')

    return render_template('post.html', form=form)

@app.route('/contactUs')
def contact_us():
  return render_template('contact_us.html')

@app.route('/SignUp', methods=["GET", "POST"])
def signUp():
   signUp_data = SignupForm()
   if signUp_data.validate_on_submit():
      exisiting_user = UserModel.query.filter(UserModel.username == signUp_data.username.data).first()
      if not exisiting_user:
         user = UserModel(username=signUp_data.username.data, password=signUp_data.password.data, birthDate=signUp_data.birthDate.data, signUpDate=datetime.utcnow())
         user.create()
         return redirect('/1')
   return render_template('SignUp.html', signUp_data=signUp_data)

@app.route('/LogIn', methods=['GET','POST'])
def log_In():
   form = LoginForm()
   if form.validate_on_submit():
      user = UserModel.query.filter(UserModel.username == form.username.data).first()
      if user and user.check_password(form.password.data):
         login_user(user)
         return redirect('/1')
   return render_template('LogIn.html', form=form)

@app.route('/Logout', methods=['GET', 'POST'])
def logout():
   logout_user()
   return redirect('/1')

@app.route('/profile/<int:page_id>', methods=['GET', 'POST'])
@login_required
def profile_information(page_id):
   all_posted_information = PostModel.query.filter_by(user_id=current_user.id).paginate(per_page=5, page=page_id)
   user_information = UserModel.query.all() 
   return render_template('profile.html', all_posted_information=all_posted_information, user_information=user_information)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    news_to_delete = PostModel.query.get_or_404(id)
    news_to_delete.delete()
    return redirect(url_for('profile_information', page_id=1))

@app.route('/edit/<int:information_id>', methods=['GET', 'POST'])
@login_required
def edit_info(information_id):
    information = PostModel.query.get_or_404(information_id)
    form = ChangePostForm(title=information.title,description=information.description)
     
    if form.validate_on_submit():
        information.title = form.title.data
        information.description = form.description.data
        
        if form.image.data:     
          information.image = form.image.data.filename
          file = path.join(app.root_path, 'static/img', form.image.data.filename)
          form.image.data.save(file)
                
        db.save()

        return redirect('/1')
    return render_template('post.html', form=form)

@app.route('/profile_edit/password/', methods=["GET","POST"])
@login_required
def edit_profile_password():
   password_change_form = PasswordChangeForm()
   if password_change_form.validate_on_submit():
      if current_user.check_password(password_change_form.password.data):
         new_password_hash = generate_password_hash(password_change_form.newPassword.data) 
         current_user.password = new_password_hash
         current_user.save()
         return redirect(url_for('profile_information', page_id=1))
      print(password_change_form.errors)
   return render_template('password_change.html', password_change_form=password_change_form)

@app.route('/profile_edit/username/', methods=["GET","POST"])
@login_required
def edit_profile_username():
   username_change_form = UsernameChangeForm(username=current_user.username, password=current_user.password)
   exisiting_user = UserModel.query.filter(UserModel.username == username_change_form.username.data).first()
   if username_change_form.validate_on_submit():
      if not exisiting_user:
         current_user.username = username_change_form.username.data
         current_user.save()
         return redirect(url_for('profile_information', page_id=1))
   return render_template('username_change.html', username_change_form=username_change_form)

@app.route('/post/<int:id>', methods=["GET", "POST"])
def inner_post(id):
   post = PostModel.query.get_or_404(id)
   form = PostCommentForm()
   all_comments = CommentModel.query.filter_by(post_id=post.id).order_by(desc(CommentModel.date)).all()
   if form.validate_on_submit():
      new_comments = CommentModel(comment=form.message.data, post_id=post.id, user_id=current_user.id, date=datetime.utcnow())
      new_comments.create() 
      all_comments = CommentModel.query.filter_by(post_id=post.id).order_by(desc(CommentModel.date)).all() 
   return render_template('inner.html', post=post, form=form, all_comments=all_comments,)

@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    comment = CommentModel.query.get_or_404(comment_id)
    if current_user.is_authenticated and current_user.id == comment.user_id or current_user.role == 'admin' :
        comment.delete()
    return redirect(url_for('inner_post', id=comment.post_id)) 

@app.route('/search/<int:page_id>')
def search(page_id):
    search = request.args.get('search', '')
    Posts = PostModel.query.filter(PostModel.title.ilike(f"%{search}%")).paginate(per_page=6, page=page_id)
    return render_template("search_results.html", Posts=Posts, search=search)

@app.errorhandler(404)
def error_404(error):   
  return render_template('error.html', error = 404), 404

