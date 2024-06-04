from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *

urlpatterns = [
    #----------------Parent------------------#
    path('parent-create/', ParentOnboardingUserSignupView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    #----------------Child------------------#
    path('child/create/', ChildCreateView.as_view(), name='child-create'),
    path('child/<int:child_id>/', ChildDetailView.as_view(), name='child-detail'),

    #-----------------Blogs---------------------#
    path('blog/categories/', BlogCategoryListView.as_view(), name='blog-category-list'),
    path('blogs/', BlogListView.as_view(), name='blog-list'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/create', BlogView.as_view(), name='blog-create'),


    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
