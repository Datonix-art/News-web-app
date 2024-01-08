from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, abort
from flask_admin import AdminIndexView

class AdminModelView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.role == 'admin':
            return True
        else:
            abort(404)

class UserAdminModelView(ModelView):
    column_list = ('id', 'username', 'birthDate', 'signUpDate', 'image', 'role')
    column_searchable_list = ('username',)
    column_filters = ('birthDate', 'signUpDate', 'role')
    can_export = True
       
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('logIn'))  

class InformationAdminModelView(ModelView):
    column_list = ('id', 'image', 'title', 'description', 'date', 'user')
    column_searchable_list = ('title', 'user.username')
    column_filters = ('title', 'user.username', 'date')
    # some configurations
    can_delete = True
    can_edit = True
    can_create = True
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('logIn'))

class PostInfoComments(ModelView):
    column_list = ('id', 'comment', 'date', 'post', 'user')
    column_searchable_list = ('user.username', )
    column_filters = ('user', 'user.username', 'date')
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('logIn'))