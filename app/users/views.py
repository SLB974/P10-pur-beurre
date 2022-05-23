
from django.contrib.auth import get_user_model
from django.contrib.auth import login as log_in
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

# from .forms import CustomUserCreationForm, UserForm
from .forms import RegisterForm, UserForm

User = get_user_model()

def account(request):
    """ view to see account details """
    form=UserForm()
    return render(request, "users/account.html", {"form":form})

def signup(request):
    if request.method == "GET":
        form = RegisterForm
        return render(request, 'account/signup.html',{'form':form})
    
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        log_in(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
        return redirect(reverse('index'))
        
    
    username=request.POST['username']
    email=request.POST['email']
    password1=request.POST['password1']
    password2=request.POST['password2']
    context = {"message":"Tous les champs sont obligatoires.", "advice":"Vérifiez votre saisie.", "form":form}

    
    if User.objects.filter(username=username).exists():
        context["message"]="Le nom de l'utilisateur est déjà attribué."
        context["advice"]="Choisissez un autre nom d'utilisateur."
        return render(request, 'account/signup.html', context)
        
    if User.objects.filter(email=email).exists():
        context["message"]="Cet e-mail est déjà attribué à un utilisateur existant."
        context["advice"]="Choisissez une autre adresse e-mail."
        return render(request, 'account/signup.html', context)
        
    if password1 != password2:
        context["message"]="Les mots de passe ne correspondent pas."
    
    return render(request, 'account/signup.html', context)
