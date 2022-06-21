from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path('', views.index, name = 'index'),
    path('nav', views.nav, name = 'nav'),
    # Authentication
    path('login', views.login_user, name = 'login'),
    path('register', views.register_user, name = 'register'),
    path('logout', views.logout_user, name = 'logout'),
    # Blog Methods
    path('list', views.list_blog, name = 'list'),
    path('view/<int:blog_id>', views.view_blog, name = 'view'),
    path('create', views.create_blog, name = 'create'),
    path('edit/<int:blog_id>', views.edit_blog, name = 'edit'),
    path('delete/<int:blog_id>', views.delete_blog, name = 'delete'),
]