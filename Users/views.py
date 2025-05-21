from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required
from scrape.models import store
from DB.models import push
# Create your views here.



def firstpage(request):
    return render(request,'registration/firstpage.html')
def Register(request):
   if request.method == 'POST':
       form = UserCreationForm(request.POST)
       if(form.is_valid()):
           form.save()
           messages.success(request,'Successfully Registered!')
           return redirect('users:login')
   else:
        form = UserCreationForm()
   return render(request,"registration/registration.html",{'form':form})

@login_required
def Sucesslogin(request):
    messages.success(request,"Successfully logged in")
    return redirect("scrape:home")

def Successlogout(request):
    logout(request)
    messages.success(request,"successfully logged out! Log in Again")
    return redirect("users:login")
@login_required
def profile(request):
    if request.method == 'POST':
        users = store.objects.filter(user=request.user)
        context = {
          "details":users,
          "show":True
        }
        return render(request,"registration/profile.html",context)
    return render(request,"scrape/home.html")
@login_required
def scrapeddata(request):
    if(request.method=='POST'):
       if(request.POST.get('id')):
           data_id = request.POST.get('id')
           delete = push.objects.filter(user_id=request.user.id,id=data_id).delete()
       data = push.objects.filter(user_id=request.user.id)
       context ={
           'data':data
        }
       return render(request,'registration/ScrapedHistory.html',context)
    return render(request,'scrape/home.html')
# def DeleteScrapedData(request):
#     if()