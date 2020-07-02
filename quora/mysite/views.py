from django.shortcuts import render,get_object_or_404,redirect
from .models import Question, Answer, Account
from .forms import AnswerForm, QuestionForm
from django.contrib.auth.models import User
from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateform,EditQuestionForm
from django.contrib.auth import (
            authenticate,
            logout ,
            login
        )
from django.contrib import messages

def home(request):
    context = {}
    context['questions'] = Question.objects.all()
    return render(request, 'mysite/home.html', context)

def question_detail(request, slug):
    context = {}
    query =   Question.objects.filter(slug__iexact=slug)
    answers = Answer.objects.filter(question = query[0].id)
    context['object'] = query[0]
    context['answer_list'] = answers
    # print(context['object'])
    # import random
    # classes = ['warning', 'success','primary', 'danger']
    # o = random.choice(classes)
    # context['o'] = o
    return render(request, "mysite/q_detail.html",context)



def create_answer(request, slug):
    context = {}
    q_obj = get_object_or_404(Question, slug=slug)
    if request.method=='POST':
        form = AnswerForm(request.POST)
        if form.is_valid():

            f = form.save(commit=False)
            f.author = request.user
            f.question = q_obj
            f.save()
            return redirect(q_obj.get_absolute_url())
        else:
            print("Invalid input")
    else:
        form = AnswerForm()
    context['form'] = form
    return render(request, "mysite/answerform.html", context)


def create_question(request):
    context = {}
    if request.method=='POST':
        form = QuestionForm(request.POST)
        if form.is_valid():

            f = form.save(commit=False)
            f.author = request.user
            f.save()
            return redirect("/home/")
        else:
            print("Invalid input")
    else:
        form = QuestionForm()
    context['form'] = form
    return render(request, "mysite/answerform.html", context)



# def profileUpdate(request):
#     context = {}
#     obj = get_object_or_404(User, username__iexact=request.user.username)
#     context['user'] = obj
#     if request.method=='POST':
#         form_u = UserUpdateForm(data=request.POST , instance=request.user)
#         form_p = ProfileUpdateForm(data=request.POST, instance=request.user)
#         if form_p.is_valid() and form_u.is_valid():
#             form_p.save()
#             form_u.save()
#         else:
#             print("Invalid input")
#     else:
#         form_p = ProfileUpdateForm(instance=obj)
#         form_u = UserUpdateForm(instance=obj)
#     context['form_p'] = form_p
#     context['form_u'] = form_u
#     return render(request, "mysite/profileUpdate.html",context)

# def profile(request):
#     context = {}
#     obj = get_object_or_404(User, username__iexact = request.user.username)
#     context['obj'] = obj
#     # obj2 = get_object_or_404(Profile,  = request.user.id)
#     print(obj2.bio)
#     return render(request, "mysite/profile.html", context)

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email    = form.cleaned_data.get('email')
            raw_pass = form.cleaned_data.get('password1')
            account = authenticate(email=email, password = raw_pass)
            login(request, account)
            messages.success(request, "You have been Registered as {}".format(request.user.username))
            return redirect('login')
        else:
            messages.error(request, "Please Correct Below Errors")
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, "registration/registration.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "Logged Out")
    return redirect("login")


def  login_view(request):
    context = {}

    user = request.user

    if user.is_authenticated:
        return redirect("home")
    if request.POST:
        form    = AccountAuthenticationForm(request.POST)
        email   = request.POST.get('email')
        password = request.POST.get('password')
        user =  authenticate(email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged In")
            return redirect("home")
        else:
            messages.error(request, "Please Correct Below Errors")
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form

    return render(request, "registration/login.html", context)


def account_view (request):
    if not request.user.is_authenticated:
        return redirect("login")
    context = {}
    print(request.user.bio)
    if request.method=='POST':
        form = AccountUpdateform(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "profile Updated")
        else:
            messages.error(request, "Please Correct Below Errors")
    else:
        form  = AccountUpdateform(
            instance=request.user
        )
    context['account_form']=form
    # blog_posts = Post.objects.filter(author=request.user)
    # context['blog_posts']=blog_posts
    return render(request, "mysite/profile.html", context)

def users_list(request):
    users = Account.objects.filter(is_active=True)
    print(users[0].bio)
    return render(request, "mysite/user_list.html", {'users':users})


def user_detail(request, username):
    user_obj = get_object_or_404(Account,username=username, is_active=True)
    return render(request,"mysite/user_detail.html",{'user':user_obj})



from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.http import HttpResponseBadRequest
from .models import Contact

def ajax_required(f):
   """
   AJAX request required decorator
   use it in your views:

   @ajax_required
   def my_view(request):
       ....

   """

   def wrap(request, *args, **kwargs):
       if not request.is_ajax():
           return HttpResponseBadRequest()
       return f(request, *args, **kwargs)

   wrap.__doc__=f.__doc__
   wrap.__name__=f.__name__
   return wrap

@ajax_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action  = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id = user_id)
            if action=='follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user)
            else:
                Contact.objects.filter(user_from=request.user,user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})



def delete_question(request, slug):
    obj = Question.objects.get(slug__iexact=slug)
    obj.delete()
    messages.success(request,"{} deleted successfully".format(slug))
    return redirect("home")
def delete_answer(request, slug, author):
    question = Question.objects.get(slug__iexact=slug)
    ans_obj = Answer.objects.get(question=question, author=author)
    ans_obj.delete()
    messages.success(request,"Answer deleted successfully")
    return redirect(question.get_absolute_url())
