from django.shortcuts import render,redirect
from django.contrib import messages
from .models import push
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import jwt
import time
from django.conf import settings

# Create your views here.
import pandas as pd
from .models import push
def store_post(request):
    df_json1 = request.session.get('df2',None)
    if df_json1:
        df1  = pd.read_json(df_json1)
        if(df1.empty):
            messages.error(request,"No available Records to Push")
            return render(request,"scrape/home.html")
        records = []
        users_obj = User.objects.using('default').get(id = request.user.id)
    #to postgre
        for _,rows in df1.iterrows():
            records.append(push(
             user_id = users_obj.id,
             title = rows['Title'],
             Likes = rows['Likes'],
             views = rows['Views'],
             comments = rows['CommentsCount'],
             subs = rows['Subs'],
            
            ))
        
            
        
    # bulk_create is better performance
        try:
           push.objects.bulk_create(records)
           messages.success(request,"Successfully Pushed!")
           return render(request,"scrape/success.html")
       
        except Exception as e:
            messages.error(request,f"failed to push! reason - {e} ")
            return render(request,"scrape/success.html")
    else:
        messages.success(request,"no records to push !")
        return render(request,"scrape/success.html")



def generateJWD_TOKEN(user):
    payload = {
        "user":{
            "username":str(user.id),
            "email":f"{user.username}@example.com",
            "first_name":"Guest",
            "last_name":"User",
            
        },
        "resources":[
            {"type":"dashboard","id":"0ff0e534-c5c0-4efd-a460-7a84d4bb292c"}#add dashboard_id
        ],
        "roles":["Gamma"],
        "exp":int(time.time())+600,
    }   
    token = jwt.encode(payload,"3TN0vTxT7sgtnZkK3uxuYo7Qv3Vw6abxMLa0o1ft7geOfQURDNL-uJgdP0qLI24XFRQblpEt7Dc8CsLDC2qUcQ",algorithm="HS256")
    decoded = jwt.decode(token, options={"verify_signature": False})
    print("DEBUG - JWT payload:", decoded)
    return token
def dashboard_embedd(request):
    
    token = generateJWD_TOKEN(request.user)
    return render(request,"scrape/dashboards.html",{"token":token})




