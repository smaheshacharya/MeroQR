from django.urls import path
from users.views import SendPasswordResetView, UserChangePasswordView, UserPasswordResetView, UserProfileView,UserLoginView,UpdateUserView,signupVerify,signup
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('register/', UserRegistrationView.as_view(), name='register'),
    path('register_verify/<int:otp>/', signupVerify,name = "signup_verify"),
    path('register/', signup,name = "signup"),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-otp/', SendPasswordResetView.as_view(), name='change-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('user-update/<int:pk>/', UpdateUserView.as_view(), name='user-update'),


    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
