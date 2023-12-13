from django.urls import path, include
from .views import CustomAuthToken, UserSignupViewSet, custom_logout
from rest_framework.routers import DefaultRouter
from .views import (RequestDemoViewSet, ContactUsViewSet, HelpandSupportViewSet,
                    UserProfileDetailView, ForgotPasswordView)


router = DefaultRouter()
router.register(r'request-demo', RequestDemoViewSet)
router.register(r'contact-us', ContactUsViewSet)
router.register(r'helpandsupport', HelpandSupportViewSet)

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='user-login'),
    path('logout/', custom_logout, name='custom-logout'),
    path('signup/', UserSignupViewSet.as_view(), name='signup'),
    # path('signup-request/', SignupRequestsCreateView.as_view(), name='create-user-profile'),
    # path('user-profile/<int:pk>/', UserProfileDetailView.as_view(), name='user-profile-detail'),
    path('user-profile/<int:pk>/photo/', UserProfileDetailView.as_view(), name='user-profile-photo'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('', include(router.urls))
]
