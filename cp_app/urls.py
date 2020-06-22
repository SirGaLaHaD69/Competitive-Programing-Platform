from django.urls import path
from cp_app import views

app_name = 'cp_app'

urlpatterns=[
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='user_login'),
    path('discuss/',views.discuss,name='discuss'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('add',views.add_problems,name='add'),
]
