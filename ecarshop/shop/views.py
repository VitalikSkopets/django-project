from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.shortcuts import render, redirect, get_list_or_404
from django.core.mail import BadHeaderError, EmailMultiAlternatives, send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import DetailView, ListView, FormView, CreateView

from ecarshop.settings import EMAIL_ADMIN
from .models import *
from .forms import *
from .utils import *


class Index(DataMixin, ListView):
    model = Vehicle
    context_object_name = 'vehicles'
    template_name = 'shop/index.html'

    def get_queryset(self):
        return Vehicle.objects.filter(available=True).order_by('-time_update')[:6]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Shop e-car')
        return dict(list(context.items()) + list(c_def.items()))


# def index(request):
#     vehicles = Vehicle.objects.filter(available=True).order_by('-time_update')[:6]
#     cart_vehicle_form = CartAddVehicleForm()
#     context = {
#         'title': 'Shop e-car',
#         'menu': menu,
#         'vehicles': vehicles,
#         'cart_vehicle_form': cart_vehicle_form,
#     }
#     return render(request=request, template_name='shop/index.html', context=context)


class Gallery(DataMixin, ListView):
    model = Vehicle
    template_name = 'shop/gallery.html'
    paginate_by = 3

    def get_queryset(self):
        return get_list_or_404(Vehicle, available=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Gallery')
        return dict(list(context.items()) + list(c_def.items()))


# def gallery(request):
#     all_vehicle_list = get_list_or_404(Vehicle, available=True)  # Vehicle.objects.filter(available=True)
#     paginator = Paginator(all_vehicle_list, 3)  # Show 3 vehicles per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     cart_vehicle_form = CartAddVehicleForm()
#     context = {
#         'title': 'Gallery',
#         'menu': menu,
#         'page_obj': page_obj,
#         'cart_vehicle_form': cart_vehicle_form,
#     }
#     return render(request=request, template_name='shop/gallery.html', context=context)


class TypeDetail(DataMixin, ListView):
    model = Vehicle
    slug_url_kwarg = 'type_slug'
    template_name = 'shop/type_detail.html'
    paginate_by = 3

    def get_queryset(self):
        return get_list_or_404(Vehicle, type__slug=self.kwargs['type_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Type-{self.kwargs['type_slug'].upper()} vehicles"
        context['menu'] = menu
        context['cart_vehicle_form'] = CartAddVehicleForm
        return context


# def type_detail(request, type_slug):
#     type_detail_list = get_list_or_404(Vehicle, type__slug=type_slug)
#     paginator = Paginator(type_detail_list, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     cart_vehicle_form = CartAddVehicleForm()
#     context = {
#         'title': f'Type-{type_slug.upper()} vehicles',
#         'menu': menu,
#         'page_obj': page_obj,
#         'cart_vehicle_form': cart_vehicle_form,
#     }
#     return render(request=request, template_name='shop/type_detail.html', context=context)


class VehicleDetail(DataMixin, DetailView):
    model = Vehicle
    slug_url_kwarg = 'vehicle_slug'
    context_object_name = 'vehicle'
    form_class = CartAddVehicleForm
    template_name = 'shop/vehicle_detail.html'
    allow_empty = False

    def get_queryset(self):
        return Vehicle.objects.filter(slug=self.kwargs['vehicle_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Specification')
        return dict(list(context.items()) + list(c_def.items()))


# def vehicle_detail(request, vehicle_slug):
#     vehicle_details = get_object_or_404(Vehicle, slug=vehicle_slug)
#     cart_vehicle_form = CartAddVehicleForm()
#     context = {
#         'title': 'Specification',
#         'menu': menu,
#         'vehicle': vehicle_details,
#         'cart_vehicle_form': cart_vehicle_form,
#     }
#     return render(request=request, template_name='shop/vehicle_detail.html', context=context)


class Manufacturers(DataMixin, ListView):
    model = Vehicle
    slug_url_kwarg = 'type_slug'
    template_name = 'shop/type_detail.html'
    paginate_by = 3

    def get_queryset(self):
        return Vehicle.objects.filter(slug__startswith=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f"Manufacturer’s vehicles - {self.kwargs['slug'].upper()}")
        return dict(list(context.items()) + list(c_def.items()))


# def manufacturers(request, slug):
#     manufacturer = Vehicle.objects.filter(slug__startswith=slug)
#     cart_vehicle_form = CartAddVehicleForm()
#     context = {
#         'title': f'Manufacturer’s vehicles - {manufacturer[0].make}',
#         'menu': menu,
#         'manufacturers': manufacturer,
#         'cart_vehicle_form': cart_vehicle_form,
#     }
#     return render(request=request, template_name='shop/manufacturers.html', context=context)


class Contact(DataMixin, FormView):
    template_name = 'shop/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('shop:feedback')

    def form_valid(self, form):
        body = {
            'first_name': form.cleaned_data['first_name'],
            'last_name': form.cleaned_data['last_name'],
            'email': form.cleaned_data['email'],
            'message': form.cleaned_data['message'],
        }
        html_body = render_to_string('shop/email.html', body)
        message = EmailMultiAlternatives(subject="Shop E-car Website Inquiry", to=[EMAIL_ADMIN, ])
        message.attach_alternative(html_body, "text/html")
        try:
            message.send(fail_silently=True)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Contact')
        return dict(list(context.items()) + list(c_def.items()))


# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             body = {
#                 'first_name': form.cleaned_data['first_name'],
#                 'last_name': form.cleaned_data['last_name'],
#                 'email': form.cleaned_data['email'],
#                 'message': form.cleaned_data['message'],
#             }
#             html_body = render_to_string('shop/email.html', body)
#             message = EmailMultiAlternatives(subject="Shop E-car Website Inquiry", to=[EMAIL_ADMIN, ])
#             message.attach_alternative(html_body, "text/html")
#             try:
#                 message.send(fail_silently=True)
#             except BadHeaderError:
#                 return HttpResponse('Invalid header found.')
#             return redirect(to='shop:feedback')
#     else:
#         form = ContactForm()
#     context = {
#         'title': 'Contact',
#         'menu': menu,
#         'form': form,
#     }
#     return render(request=request, template_name='shop/contact.html', context=context)


def feedback(request):
    context = {
        'title': 'Thanks!',
        'menu': menu,
    }
    return render(request=request, template_name='shop/feedback.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = NewUserForm
    template_name = 'shop/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Registration successful. New account created: {username}")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(to="shop:home")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information. Account creation failed")
            return render(request=request, template_name=self.template_name, context={'form': form})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Sign Up')
        return dict(list(context.items()) + list(c_def.items()))


# def register_request(request):
#     if request.method == "POST":
#         form = NewUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f"Registration successful. New account created: {username}")
#             login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             return redirect(to="shop:home")
#         else:
#             messages.error(request, "Unsuccessful registration. Invalid information. Account creation failed")
#             return render(request=request, template_name='shop/register.html', context={'title': 'Sign Up',
#                                                                                         'menu': menu,
#                                                                                         'form': form,
#                                                                                         }
#                           )
#     form = NewUserForm()
#     context = {
#         'title': 'Sign Up',
#         'menu': menu,
#         'form': form,
#     }
#     return render(request=request, template_name='shop/register.html', context=context)


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect(to="shop:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
            return render(request=request, template_name='shop/login.html', context={'title': 'Login',
                                                                                     'menu': menu,
                                                                                     'login_form': form,
                                                                                     }
                          )
    form = AuthenticationForm()
    context = {
        'title': 'Login',
        'menu': menu,
        'login_form': form
    }
    return render(request=request, template_name='shop/login.html', context=context)


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect(to="shop:login")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "shop/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'e-carshop',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, EMAIL_ADMIN, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect(to="shop:home")
                    # return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    context = {"password_reset_form": password_reset_form}
    return render(request=request, template_name="shop/password/password_reset.html", context=context)


def search(request):
    query = request.GET.get('query')
    results = []
    if request.GET.get('query'):
        results = Vehicle.objects.annotate(search=SearchVector('make', 'model', 'type__title'),).filter(search=query)
    cart_vehicle_form = CartAddVehicleForm()
    context = {
            'title': 'Search',
            'menu': menu,
            'query': query,
            'results': results,
            'cart_vehicle_form': cart_vehicle_form,
        }
    return render(request=request, template_name='shop/search.html', context=context)


def weather(request):
    city = request.GET.get('city')
    if request.GET.get('city'):
        url = f"https://wttr.in/{city}"
        return redirect(to=url)
    return redirect(to='shop:home')
