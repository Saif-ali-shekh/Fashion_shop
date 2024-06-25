from django.urls import path
from .views import *
from .drf_apis import *


urlpatterns = [
    path('' , DashboardView.as_view(), name='dashboard'),
    path('signup/' , SignUpView.as_view(), name='signup'),
    path('login/' , LoginView.as_view(), name='login'),
    path('user/<str:identifier>/', UserDetailView.as_view(), name='user-detail'),
    
    ################rest_framework########
    path('api/login/', UserLoginView.as_view(), name='login'),
    path('api/signup/', UserSignupView.as_view(), name='signup'),
    path('api/userlist/', UserListView.as_view(), name='userlist'),
    path('api/useradd/', UserAddView.as_view(), name='useradd'),
    path('api/add-design/', AddDesignView.as_view(), name='add_design'),
    path('api/designs-with-images/', DesignsWithImagesView.as_view(), name='designs-with-images'),
]
