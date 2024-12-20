from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from useractivities import dboperations as me

# Temporary in-memory user storage (for demonstration purposes)
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate inputs
        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return render(request, 'login.html')

        # Fetch the user from the database
        user = me.get_user_by_email(email)  # Define this function in `dboperations`
        if user and check_password(password, user['password']):
            # Login success
            userdata = {
                'name': user['username'],
                'dob': user['dob'],
                'department': user['department'],
                'cgpa': user['cgpa'],
                'gender': user['gender'],
                'registerno':user['registerno'],
            }
            return render(request, 'dashboard.html', {'userdata': userdata})

        # If no matching user is found or password is incorrect
        messages.error(request, 'The username and/or password you specified are not correct.')
        return render(request, 'login.html')

    return render(request, 'login.html')
def register_view(request):
    if request.method == 'POST':
        # User data manually provided (you can replace these with dynamic data from form)
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        cgpa = request.POST.get('cgpa')
        department = request.POST.get('department')
        registerno=request.POST.get('rollno')
        # Validate inputs
        if not username or not password or not email:
            messages.error(request, 'Username, password, and email are required')
            return render(request, 'register.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return render(request, 'register.html')

        existing_users = me.get_all_users()  # Get all users
        if any(user['email'] == email for user in existing_users):
            messages.error(request, 'Email already registered')
            return render(request, 'register.html') 

        # Hash the password before storing it (use Django's make_password if needed)
        hashed_password = make_password(password)

        # Prepare user data
        user_data = {
            'username': username,
            'password': hashed_password,
            'email': email,
            'dob': dob,
            'gender': gender,
            'cgpa': cgpa,
            'department': department,
            'registerno':registerno

        }

        # Insert user data into the database using your insertdata function
        me.insertdata(user_data)

        # Redirect to login page after successful registration
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')  # Make sure you have the correct name for your login view

    return render(request, 'register.html')

def forget_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')

        # Validate inputs
        if not email or not password or not confirm_password:
            messages.error(request, 'All fields are required.')
            return render(request, 'forgetpage.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'forgetpage.html')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'forgetpage.html')

        # Check if email exists in the database
        user = me.get_user_by_email(email)  # Function to fetch user by email
        if not user:
            messages.error(request, 'No account found with this email.')
            return render(request, 'forgetpage.html')

        # Update the password in MongoDB
        hashed_password = make_password(password)
        try:
            me.update_user_password(email, hashed_password)  # Update password in database
            messages.success(request, 'Password updated successfully. Please log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'Failed to update password. Please try again later.')
            print(f"Error updating password: {e}")
            return render(request, 'forgetpage.html')

    return render(request, 'forgetpage.html')