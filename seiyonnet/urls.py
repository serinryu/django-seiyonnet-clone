from django.contrib import admin
from django.urls import path, include
from board import views
from accounts import views as accounts_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home, name='home'),

    path('search/', views.search, name='search'),
    path('profile/<str:user_username>', views.profile, name='profile'),
    path('profile/<str:user_username>/edit', views.profileedit, name='profileedit'),

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

    path('anony_like/<int:post_id>', views.anony_like, name='anony_like'),
    path('free_like/<int:post_id>', views.free_like, name='free_like'),

    path('accounts/login/', accounts_views.login, name='login'),    
    path('accounts/logout/', accounts_views.logout, name='logout'),
    path('accounts/signup/', accounts_views.signup, name='signup'),

    path('accounts/', include('allauth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)