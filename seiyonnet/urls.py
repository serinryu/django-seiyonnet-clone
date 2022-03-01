from django.contrib import admin
from django.urls import path, include
from board import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home, name='home'),

    path('anony/', views.anony, name='anony'),
    path('anony_postcreate/', views.anonypostcreate, name='anonypostcreate'),
    path('anony_detail/<int:post_id>', views.anonydetail, name='anonydetail'),
    path('new_comment/<int:post_id>', views.newcomment, name='newcomment'),

    path('free/', views.free, name='free'),
    path('free_postcreate/', views.freepostcreate, name='freepostcreate'),
    path('free_detail/<int:post_id>', views.freedetail, name='freedetail'),
    path('new_freecomment/<int:post_id>', views.newfreecomment, name='newfreecomment'),


    # path('login/', accounts_views.login, name='login'),    
    # path('logout/', accounts_views.logout, name='logout'),
    # path('signup/', accounts_views.signup, name='signup'),


    # path('accounts/', include('allauth.urls')),

]