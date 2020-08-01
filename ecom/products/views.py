from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from products.models import Product
from django.contrib.auth import authenticate, login, get_user_model
from . forms import ContactForm, LoginForm, RegisterForm
from .import views
# Create your views here.

def home(request):
    return render(request, 'products/home.html')

def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
    return render(request, 'products/contact.html', context={'form': form})

def login_page(request):
    form = LoginForm(request.POST or None)
    print("User")
    print(request.user.is_authenticated)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        #print(request.user.is_authenticated)
        if user is not None:
            #print(request.user.is_authenticated)
            login(request, user)
            return redirect ("/")
        else:
            print("Error")
    return render(request, 'product/login.html', context={'form': form})

User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create_user(username,email, password)
        print(new_user)
    return render(request, 'product/register.html', context={'form': form}) 

class ProductFeaturedListView(ListView):
    #queryset = Product.objects.all()
    template_name = 'products/list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()

class ProductFeaturedDetailView(DetailView):
    #queryset = Product.objects.all()
    template_name = 'products/detail.html'
  
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'products/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context

class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context

    # def get_object(self, *args, **kwargs): 
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     instance = Product.objects.get_by_id(pk)
    #     if instance is None:
    #         raise Http404("Product")
    #     return instance



