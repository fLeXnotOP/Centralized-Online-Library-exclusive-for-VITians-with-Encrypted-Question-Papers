from email.message import EmailMessage
import readline
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from pauth import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_str 
from django.template.loader import render_to_string
from . tokens import generate_token
from base64 import urlsafe_b64decode, urlsafe_b64encode #Used in def activate try block first line
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required #used to ensure that coe is the only one able to login 
from authentication.functions import handle_uploaded_file 
from authentication.forms import StudentForm 

# Create your views here.
def index(request):
    return render(request, "authentication\index.html")

def home(request):#Made By ANSH MEHTA(21BCY10113)
    return render(request, "authentication\home.html")

#####################################################################################################################

def signup(request):#Made By ANSH MEHTA(21BCY10113)

    if request.method == 'POST':
        #username = request.POST.get('username')
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        #fname = request.POST['fname']
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if User.objects.filter(username=username):#Made By ANSH MEHTA(21BCY10113)
            messages.error(request, "Username aldready exist! Please try again with some other username")
            return redirect('signup')

        # if not username.isalnum(): #Made By ANSH MEHTA(21BCY10113)
        #     messages.error(request, "Username must be alphanumeric") 
        #     return redirect('signup')

        if User.objects.filter(email=email): #Made By ANSH MEHTA(21BCY10113)
            messages.error(request, "email aldready registered!")
            return redirect('signup')

        if len(username)>14: #Made By ANSH MEHTA(21BCY10113)
            messages.error(request, "Username must be under 14 charecters")

        if len(username)<3: #Made By ANSH MEHTA(21BCY10113)
            messages.error(request, "Username too short must be atleast greater than 2 letters")

        if len(pass1)<2 or len(pass1)>14: #Made By ANSH MEHTA(21BCY10113)
            messages.error(request, "Username must be greater than 8 & lesser than 14 charecters")        

        if pass1 != pass2: #Made By ANSH MEHTA(21BCY10113)
            messages.error(request, "Passwords Did not Match")
            return redirect('signup')

        def is_academic(email):
        # Check if the email address belongs to a known academic domain
            academic_domains = ['vitbhopal.ac.in']
            for domain in academic_domains:
                if domain in email:
                    return True
            return False

        # Example usage
        if is_academic(email):
           myuser = User.objects.create_user(username, email, pass1)
           myuser.first_name = fname
           myuser.last_name = lname
           myuser.is_active = False       
           myuser.save()
           messages.success(request,'Your account has been successful created. Please Login to Continue')


           #Welcome Email

        #    subject = "welcome to Login system made by Ansh Mehta (21BCY10113)" #This subject will be displayed to the user
        #    message = "hello "+ myuser.first_name + "!!\n"  + "Your Username is:- "+ myuser.username + " Kindly Click on the link to activate your account \n \n Thank you for visiting our website ~Ansh mehta (21BCY10113)" #This content will be displayed to the user
        #    from_email = settings.EMAIL_HOST_USER
        #    to_list = [myuser.email]
        #    send_mail(subject, message, from_email, to_list, fail_silently=True)

           #Email Address confirmation Email

           current_site = get_current_site(request)
           email_subject = "confirm your email @ansh login system"
           message2 = render_to_string('email_verification.html',{
               'name': myuser.first_name,
               'Username': myuser.username,
               'domain': current_site.domain,
               'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
               'token' : generate_token.make_token(myuser)
           })
           email= EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
           )
           email.fail_silently = True
           email.send()
           
           return redirect('signin')

        else:
            messages.error(request, "Try Again using VIT Bhopal Mail id ~Ansh Mehta 21BCY10113")
            return redirect('signup') #Used to redirect to another webpage after signup
    
    return render(request, "authentication/signup.html")

#####################################################################################################################
def signin(request): #Made By ANSH MEHTA(21BCY10113)
    if request.method == 'POST':
        username = request.POST['username'] 
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request, "authentication\index.html", {'fname': fname})
        else:
            messages.error(request, "Incorrect Username or Password")
            return redirect('index')

    return render(request, "authentication/signin.html")
#####################################################################################################################

def signout(request): #Made By ANSH MEHTA(21BCY10113)
    logout(request)
    messages.success(request, "Logged Out Sucessfully ! ~Ansh Mehta 21BCY10113")
    return redirect(index)
#####################################################################################################################

def activate(request, uidb64, token): #Made By ANSH MEHTA(21BCY10113)
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'activation_failed.html')

#####################################################################################################################

def upload(request): #Made By ANSH MEHTA(21BCY10113)
    if request.user.username != 'coe':
        return redirect('unauthorized')
    return render(request, "authentication/upload.html")

def unauthorized(request): #Made By ANSH MEHTA(21BCY10113)
    return render(request, 'authentication/unauthorized.html')

def uploadfile(request):  
    if request.method == 'POST':  
        student = StudentForm(request.POST, request.FILES)  
        if student.is_valid():  
            handle_uploaded_file(request.FILES['file'])  
            model_instance = student.save(commit=False)
            model_instance.save()
            return HttpResponse("File uploaded successfuly")  
    else:  
        student = StudentForm()  
        return render(request,"upload.html",{'form':student})