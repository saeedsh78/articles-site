from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import FieldsMixin, FormValidMixin, AuthorAccessMixin, SuperUserAccessMixin, SuperUserandAuthorAccessMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from blog.models import Article, Category
from .forms import ProfileForm, SignupForm, ArticleForm


class ArticleList(SuperUserandAuthorAccessMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(SuperUserandAuthorAccessMixin, FormValidMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'registration/article-create-update.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        user_info = User.objects.get(pk=self.request.user.pk)
        obj.user_info = user_info
        return obj

    def get_form_kwargs(self):
        kwargs = super(ArticleCreate, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class ArticleUpdate(AuthorAccessMixin, FormValidMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'registration/article-create-update.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        user_info = User.objects.get(pk=self.request.user.pk)
        obj.user_info = user_info
        return obj

    def get_form_kwargs(self):
        kwargs = super(ArticleUpdate, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class ArticleDelete(SuperUserAccessMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('account:home')
    template_name = 'registration/article_confirm_delete.html'


class CategoryCreate(CreateView):
    model = Category
    template_name = 'registration/category-create.html'
    fields = '__all__'


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('account:profile')

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Login(LoginView):

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')


class Register(CreateView):
    form_class = SignupForm
    template_name = "registration/register.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی اکانت'
        message = render_to_string('registration/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse("لینک فعالسازی به ایمیل شما ارسال شد.<a href='/login'>ورود</a>")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return HttpResponse("اکانت شما با موفقیت فعال شد برای ورود <a href='/login'>کلیک</a> کنید.")
    else:
        return HttpResponse("لینک فعالسازی منقضی شده است. <a href='/register'>دوباره امتحان کنید.</a>")

