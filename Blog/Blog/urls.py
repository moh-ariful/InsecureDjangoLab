from django.conf import settings
from posting.views import index, UpdatePost, DeletePost, SearchPosting
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from posting import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('detail/<int:pk>', views.DetailPosting.as_view(), name='detail'),
    path('detail/<str:pk>/', views.DetailPosting.as_view(), name='detail'),    # Rentan SQLI
    # Add post
    path('add/', views.AddPost.as_view(), name='add'),
    path('<int:pk>/update', UpdatePost.as_view(), name='update'),
    path('detail/<int:pk>/delete', DeletePost.as_view(), name='delete'),
    path('search/', SearchPosting.as_view(), name='search'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
