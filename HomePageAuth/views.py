from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, get_backends
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from .forms import SignupForm, LoginForm, CustomPasswordResetForm, ProfileUpdateForm
from .models import Profile
import os

User = get_user_model()

#  Home View (Shows home if logged in, else redirects to login)


def home(request):
    return render(request, "HomePageAuth/home.html")

#  Signup View with Email Verification


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if not email.endswith("@ddu.ac.in"):
                messages.error(request, "Please use university mail id!")
                return render(request, "HomePageAuth/signup.html", {"form": form})
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            role = form.cleaned_data["role"]

            if not role:
                messages.error(request, "Invalid role selected.")
                return render(request, "HomePageAuth/signup.html", {"form": form})

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return render(request, "HomePageAuth/signup.html", {"form": form})

            verification_code = get_random_string(
                length=6, allowed_chars="1234567890")

            request.session["signup_data"] = {
                "email": email,
                "username": username,
                "password": password,
                "role": role,
                "verification_code": verification_code,
                "expires_at": str(now().timestamp() + 300),  # 5-minute expiry
            }
            request.session.set_expiry(300)

            send_mail(
                "Verify Your Email - CodeSphere",
                f"Your verification code is {verification_code}. It is valid for 5 minutes.",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(
                request, "A verification code has been sent to your email.")
            return redirect(reverse("HomePageAuth:verify_email"))

    else:
        form = SignupForm()

    return render(request, "HomePageAuth/signup.html", {"form": form})

#  Email Verification View


def verify_email(request):
    signup_data = request.session.get("signup_data")

    if not signup_data:
        messages.error(request, "Session expired. Please sign up again.")
        return redirect(reverse("HomePageAuth:signup"))

    if request.method == "POST":
        entered_code = request.POST.get("verification_code")

        if now().timestamp() > float(signup_data.get("expires_at", 0)):
            messages.error(
                request, "Verification code expired. Please sign up again.")
            request.session.pop("signup_data", None)
            return redirect(reverse("HomePageAuth:signup"))

        if entered_code != signup_data["verification_code"]:
            messages.error(
                request, "Invalid verification code. Please try again.")
            return render(request, "HomePageAuth/verify_email.html")

        role = signup_data["role"]

        user = User.objects.create_user(
            username=signup_data["username"],
            email=signup_data["email"],
            password=signup_data["password"],
            role=role,
        )
        user.is_active = True
        user.save()

        #  Automatically Create Profile After Verification
        Profile.objects.create(user=user, full_name=user.username)

        backend = get_backends()[0]
        user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
        login(request, user, backend=user.backend)

        request.session.pop("signup_data", None)

        messages.success(
            request, "Your email has been verified. You are now logged in.")

        return redirect("HomePageAuth:home")

    return render(request, "HomePageAuth/verify_email.html")

#  Profile Update View


def update_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        old_image = profile.image  # Store the old image before updating

        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_image = form.cleaned_data.get("image")

            #  Check if a new image is uploaded and different from the old one
            if new_image and old_image and old_image.name != new_image.name:
                old_image_path = os.path.join(
                    settings.MEDIA_ROOT, str(old_image))

                #  Delete old image only if it exists in the file system
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            if "image" not in request.FILES:  # Keep old image if no new image is uploaded
                form.cleaned_data["image"] = profile.image

            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("HomePageAuth:home")

    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, "HomePageAuth/update_profile.html", {"form": form, "profile": profile})
#  Login View


def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        storage = messages.get_messages(request)
        storage.used = True

        if form.is_valid():
            email = form.cleaned_data["email"]
            # if not email.endswith("@ddu.ac.in"):
            #     messages.error(request, "Please use university mail id!")
            #     return render(request, "HomePageAuth/signup.html", {"form": form})
            password = form.cleaned_data["password"]
            remember_me = form.cleaned_data.get("remember_me")

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                request.session["user_email"] = user.email

                if remember_me:
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)

                messages.success(request, "Login successful!")
                return redirect("HomePageAuth:home")
            else:
                messages.error(request, "Invalid email or password.")

    return render(request, "HomePageAuth/login.html", {"form": form})

#  Logout View


def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect("HomePageAuth:login")

#  Password Reset Request View


def password_reset_request(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if not User.objects.filter(email=email).exists():
                messages.error(request, "No account found with this email.")
                return render(request, "registration/password_reset_form.html", {"form": form})

            form.save(
                request=request,
                use_https=True,
                email_template_name="registration/password_reset_email.html",
                subject_template_name="registration/password_reset_subject.txt",
            )

            messages.success(
                request, "If an account exists with this email, a password reset link has been sent.")
            return redirect("password_reset_done")

    else:
        form = CustomPasswordResetForm()

    return render(request, "registration/password_reset_form.html", {"form": form})
