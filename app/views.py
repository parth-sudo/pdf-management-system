from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserForm, PDFForm, SharePDFForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from .models import PDF, Comment
from django.contrib.auth.models import User

@login_required(login_url = 'login')
def home(request):
    if request.method == 'POST':
        form = PDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.author = request.user
            pdf.save()
            messages.success(request, "PDF Added Successfully!")
            return redirect('home')
    else:
        form = PDFForm()
    
    user_pdfs = PDF.objects.filter(author=request.user).order_by('title')
    shared_pdfs = PDF.objects.filter(users_shared_with=request.user).order_by('title')
    context = {'form': form, 'user_pdfs': user_pdfs, 'shared_pdfs':shared_pdfs}
    return render(request, 'app/home.html', context)

@unauthenticated_user
def register(request):
    context = {}
    form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context['form'] = form
    return render(request, 'app/register.html', context)

@unauthenticated_user
def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'app/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth_logout(request)
    return redirect('login')

# @login_required(login_url = 'login')
#TODO one more permission.
def discuss(request, pk):
    pdf_instance = get_object_or_404(PDF, pk=pk)
    comments = Comment.objects.filter(pdf = pdf_instance).order_by('-timestamp')
    context = {'pdf': pdf_instance, 'comments' : comments, 
               'user' : request.user, 'users' : User.objects.all()}
    return render(request, 'app/discuss.html', context)

def post_comment(request):
    if request.method == 'POST':
        comment_description = request.POST.get('comment_description')
        user = request.user
        pdfId = request.POST.get('pdfId')
        pdf_instance = get_object_or_404(PDF, pk=pdfId)

        new_comment = Comment(description=comment_description, author=user, pdf=pdf_instance)
        new_comment.save()
        messages.success(request, 'Comment posted successfully!')

    return redirect(f'/discuss/{pdfId}')


def share_pdf(request, pdf_id):
    pdf = PDF.objects.get(id=pdf_id)

    if request.method == 'POST':
        form = SharePDFForm(request.POST)
        if form.is_valid():
            users_shared_with = form.cleaned_data['users_shared_with']
            pdf.users_shared_with.set(users_shared_with)
            messages.success(request, "File Shared successfully!")
    else:
        form = SharePDFForm()

    context = {'pdf': pdf, 'form': form}
    return render(request, 'app/discuss.html', context)