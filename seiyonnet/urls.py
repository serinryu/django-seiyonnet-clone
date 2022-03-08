from django.contrib import admin
from django.urls import path, include
from board import views
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home, name='home'),

    path('search/', views.search, name='search'),
    path('profile/<int:user_id>', views.profile, name='profile'),

    path('anony/', views.anony, name='anony'),
    path('anony_postcreate/', views.anonypostcreate, name='anonypostcreate'),
    path('anony_detail/<int:post_id>', views.anonydetail, name='anonydetail'),
    path('anony_detail/<int:post_id>/edit', views.anonydetail_edit, name='anonydetail_edit'),
    path('anony_detail/<int:post_id>/delete', views.anonydetail_delete, name='anonydetail_delete'),
    path('new_comment/<int:post_id>', views.newcomment, name='newcomment'),
    path('new_comment/<int:post_id>/delete/<int:comment_id>', views.comment_delete, name='comment_delete'),

    path('free/', views.free, name='free'),
    path('free_postcreate/', views.freepostcreate, name='freepostcreate'),
    path('free_detail/<int:post_id>', views.freedetail, name='freedetail'),
    path('free_detail/<int:post_id>/edit', views.freedetail_edit, name='freedetail_edit'),
    path('free_detail/<int:post_id>/delete', views.freedetail_delete, name='freedetail_delete'),
    path('new_freecomment/<int:post_id>', views.newfreecomment, name='newfreecomment'),
    path('new_freecomment/<int:post_id>/delete/<int:comment_id>', views.freecomment_delete, name='freecomment_delete'),

    path('login/', accounts_views.login, name='login'),    
    path('logout/', accounts_views.logout, name='logout'),
    path('signup/', accounts_views.signup, name='signup'),

    #path('accounts/', include('allauth.urls')),

]