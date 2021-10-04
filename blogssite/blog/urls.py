from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name="home"),
    path('search/', views.search, name="search"),
    path('contact-me/', views.contactMe, name="contact-me"),

    path('login/', views.login_view, name="login"),
    path('register/', views.register, name="register"),
    path('activate/<uidb64>/<token>',views.verificationEmail,name="activate"),
    path('logout/', views.logout_view, name="logout"),
    path('post/<slug>', views.view_post, name="view_post"),
    path('like/<slug>',views.like,name="like"),

    path('all_categories/', views.all_categorise, name="all_categories"),
    path('category_post/<slug>', views.categoryPost, name="categoryPost"),

    path('all_posts/', views.all_posts, name="all_posts"),
    path('post/comment/', views.commentOnPost, name="comment"),
    path('replay/', views.replay, name="replay"),

    path('user_panal/', views.user_panal, name="user_panal"),
    path('posts/', views.posts, name="posts"),
    path('create_post/', views.create_posts, name="create_post"),
    path('edit_post/<str:pk>', views.edit_post, name="edit_post"),
    path('delete_post/<str:pk>', views.delete_post, name="delete_post"),

    path('comments/', views.comments, name="comments"),
    path('get_comments/<int:pk>', views.get_comments, name="comments"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('image-update', views.image_update, name="image_update"),

    path('feedback/', views.feedback, name="feedback"),

]
