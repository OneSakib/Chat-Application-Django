from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView
from .models import Profile, Thread, ChatMessage
from .forms import UserUpdateForm, ProfileUpdateForm


# Create your views here.
def index(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'index.html', context)


def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user
    }
    return render(request, 'userdetail.html', context)


def follow(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        user = request.POST.get('user')
        user = User.objects.get(username=user)
        target = request.POST.get('target')
        target = User.objects.get(username=target)
        try:
            if action == 'Follow':
                thread = Thread.objects.create(first_person=user, second_person=target)
                thread.save()
            elif action == 'Unfollow':
                thread = Thread.objects.get(first_person=user, second_person=target)
                thread.delete()
            return JsonResponse({'status': 'ok'})
        except Exception:
            return JsonResponse({'status': 'ko'})

    return JsonResponse({'status': 'ko'})


@login_required(login_url='/')
def chat(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessages_thread')
    context = {
        'Threads': threads,
        'alluser': User
    }
    return render(request, 'chat.html', context)


class UserLoginForm(LoginView):
    template_name = 'login.html'
    success_url = '/'
    login_url = '/'


class SignUp(FormView):
    template_name = 'signup.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super(SignUp, self).form_valid(form)


class UserProfile(FormView):
    template_name = 'profile.html'
    form_class = UserUpdateForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        context['form'] = UserUpdateForm(instance=self.request.user)
        context['profile'] = ProfileUpdateForm(instance=self.request.user.profile)
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            f = UserUpdateForm(request.POST, instance=request.user)
            p = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if f.is_valid():
                if p.is_valid():
                    f.save()
                    p.save()
                    return HttpResponseRedirect('/')
        return super(UserProfile, self).post(request, *args, **kwargs)
