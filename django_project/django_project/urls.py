from django.urls import include, path

urlpatterns = [
    path('', include('blog.urls')),
    path('captcha/', include('captcha.urls')),
]
