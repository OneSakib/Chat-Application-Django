from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('user/<username>/', views.user_detail, name='user_detail'),
    path('follow/', views.follow, name='follow'),
    path('chat/', views.chat, name='chat'),
    path('login/', views.UserLoginForm.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', views.UserProfile.as_view(), name='profile'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
