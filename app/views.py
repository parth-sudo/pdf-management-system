from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserForm, PDFForm, SharePDFForm, CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from .models import PDF, Comment
from django.contrib.auth.models import User
from .templatetags import extras
from .extra_functions import random_string_generator

@login_required(login_url = 'login')
def home(request):
    if request.method == 'POST':
        form = PDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.author = request.user
            pdf.guest_code = random_string_generator()
            pdf.save()
            messages.success(request, "PDF Added Successfully!")
            return redirect('home')
    else:
        form = PDFForm()
    
    user_pdfs = PDF.objects.filter(author=request.user).order_by('-timestamp')
    shared_pdfs = PDF.objects.filter(users_shared_with=request.user).order_by('-timestamp')
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

def discuss(request, pk, code):
    pdf_instance = get_object_or_404(PDF, pk=pk)
    comments = Comment.objects.filter(pdf = pdf_instance, parent=None).exclude(author__username='guest').order_by('-timestamp')
    replies = Comment.objects.filter(pdf=pdf_instance).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.id not in replyDict.keys():
            replyDict[reply.parent.id] = [reply]
        else:
            replyDict[reply.parent.id].append(reply)
    
    guest_instance = User.objects.get(username='guest')
    guest_comments = Comment.objects.filter(author = guest_instance, pdf = pdf_instance)
    context = {'pdf': pdf_instance, 'comments' : comments, 
               'user' : request.user, 'users' : User.objects.exclude(username='guest'),
               'replyDict' : replyDict, 'guest_comments' : guest_comments}
    
    if request.method == 'POST':
        share_form = SharePDFForm(request.POST)
        if share_form.is_valid():
            if pk != pdf_instance.pk or code != pdf_instance.guest_code:
                return HttpResponse("Path not found") 
            users_shared_with = share_form.cleaned_data['users_shared_with']
            pdf_instance.users_shared_with.set(users_shared_with)
            messages.success(request, f"File Shared successfully! Copy URL: http://127.0.0.1:8000/discuss/{pdf_instance.pk}/{pdf_instance.guest_code}/")
    else:
        if pk != pdf_instance.pk or code != pdf_instance.guest_code:
            return HttpResponse("Path not found") 
        share_form = SharePDFForm()

    context['share_form'] = share_form
    return render(request, 'app/discuss.html', context)

def post_comment(request):
    context = {}
    if request.method == 'POST':
        user = request.user
        pdfId = request.POST.get('pdfId')
        parent_id = request.POST.get('parentSno')
        comment_description = request.POST.get('comment_description')
        pdf_instance = get_object_or_404(PDF, pk=pdfId)

        if parent_id == "":
            new_comment = Comment(description=comment_description, author=user, pdf=pdf_instance)
            messages.success(request, 'Comment posted successfully!')
            new_comment.save()
        else:
            parent = Comment.objects.get(pk=parent_id)  
            new_comment = Comment(description=comment_description, author=user, pdf=pdf_instance, parent=parent)
            messages.success(request, 'Reply posted successfully!')
            new_comment.save()

    return redirect(f'/discuss/{pdfId}/{pdf_instance.guest_code}')


def guest_comment(request):

    if request.method == 'POST':
        pdfId = request.POST.get('pdfId')
        pdf_instance = get_object_or_404(PDF, pk=pdfId)
        # guest_code = request.POST.get('guest_code')
        guest_comment = request.POST.get('guest_comment')
        guest_instance = User.objects.get(username='guest')

        new_comment = Comment(description=guest_comment, author=guest_instance, pdf=pdf_instance)
        new_comment.save()

        # if str(guest_code) == str(pdf_instance.guest_code):
        #     if request.user.is_authenticated == True:
        #         messages.error(request, "You are already logged in, you cannot be a guest.")
        #         return redirect(f'/discuss/{pdfId}')
        #     new_comment = Comment(description=guest_comment, author=guest_instance, pdf=pdf_instance)
        #     new_comment.save()
        #     return redirect(f'/discuss/{pdfId}')
        # elif str(guest_code) != str(pdf_instance.guest_code):
        #     return HttpResponse("Incorrect guest_code entered")
        
    return redirect(f'/discuss/{pdfId}/{pdf_instance.guest_code}/')

def about(request):
    return render(request, 'app/about.html')