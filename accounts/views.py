from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


# Create your views here.
class SignUpView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
