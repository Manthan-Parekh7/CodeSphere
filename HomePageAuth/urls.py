from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm  # ✅ Import the custom form

app_name = "HomePageAuth"  # ✅ Namespace for URL names

urlpatterns = [
    path('', view=home, name="home"),
    path('signup/', signup_view, name="signup"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),

    # ✅ Email Verification URL
    path("verify-email/", verify_email, name="verify_email"),
    path("update-profile/", update_profile_view, name="update_profile"),
    # ✅ Password Reset URLs (Using Django's built-in views but with custom templates)
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html",
        form_class=CustomPasswordResetForm  #
    ), name="password_reset"),

    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"), name="password_reset_done"),

    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),

    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"), name="password_reset_complete"),
]
