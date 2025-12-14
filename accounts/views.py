from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


# ==============================
# REGISTER (WEB)
# ==============================
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('number')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        address = request.POST.get('address')

        if not username or not password1 or not password2:
            messages.error(request, "Username and password are required!")
        elif password1 != password2:
            messages.error(request, "Passwords do not match!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        elif phone and User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already registered!")
        else:
            User.objects.create_user(
                username=username,
                password=password1,
                phone=phone,
                email=email,
                address=address
            )
            messages.success(request, "Account created successfully!")
            return redirect('accounts:login')

    return render(request, 'register.html')


# ==============================
# LOGIN (WEB)
# ==============================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('shop:shop_home')  # Ensure this URL exists in shop app
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')


# ==============================
# LOGOUT
# ==============================
@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


# ==============================
# STAFF MANAGEMENT (SUPERUSER ONLY)
# ==============================
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)


@superuser_required
@login_required
def staff_list(request):
    staff = User.objects.filter(is_staff=True)
    return render(request, 'staff_list.html', {'staff': staff})


@superuser_required
@login_required
def add_staff(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Username and password are required!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = True
            user.save()
            messages.success(request, f"Staff {username} added successfully.")
            return redirect('accounts:staff_list')

    return render(request, 'add_staff.html')


@superuser_required
@login_required
def remove_staff(request, user_id):
    user = get_object_or_404(User, id=user_id, is_staff=True)
    username = user.username
    user.delete()
    messages.success(request, f"Staff {username} removed successfully.")
    return redirect('accounts:staff_list')


# ==============================
# API VIEWS
# ==============================
class LoginAPI(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)


class RegisterAPI(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        phone = request.data.get("phone")

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username exists"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(username=username, password=password, phone=phone)
        return Response({"message": "Registered successfully"}, status=status.HTTP_201_CREATED)
