from django.shortcuts import render,HttpResponse,redirect
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tqdm import tqdm
import os
import time
from googleapiclient.discovery import build
import psycopg2
from django.contrib import messages
from .models import store
from .forms import storeroom
import json
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
#2nd Set your driver
c_op = Options()
c_op.add_argument("--headless") #without chrome
c_op.add_argument("--disable-gpu") # no acceleration
c_op.add_argument("--window-size=1920,1080") # set window size
c_op.add_argument("--disable-blink-features=AutomationControlled") # bypass robotdetection
chrome_service = Service(r"C:\Users\lipun\OneDrive\Documents\chromedriver-win64\chromedriver-win64\chromedriver.exe") #path
driver = webdriver.Chrome(service=chrome_service,options=c_op)
  

   
#CONNECT TO DB
# def connectdb(request):
#    return psycopg2.connect(**DB) # **it will unpack dict to individual components!! dont directly use DB
# def display_links(request):
#     if request.method == 'POST' and 'hist' in request.POST:
#         l = store.objects.filter(user=request.user)
#         context = {
#             'l2':l,
#             'show':True
#         }
#         return render(request,"scrape/home.html",context)
#     return render(request,"scrape/home.html")
@login_required
def statistics(request):
    lst = []
    if(request.method=='POST'):
        f = store.objects.filter(user=request.user).order_by("-Time").first()
        if f:
              
          strfile = f.links
          link_id = strfile.split("=")[-1]
          yts = build("youtube","v3",developerKey="AIzaSyA6IX_Rvr2CQjNiDJ4aAuEmER6Z0PkDSN4") 
          res = yts.videos().list(
              part = "snippet,statistics",
              id = link_id
          )
          resp = res.execute()
          try:
               Likes = int(resp['items'][0]['statistics']['likeCount'])
               Views = int(resp["items"][0]['statistics']['viewCount'])
               CommentsCount = int(resp['items'][0]['statistics']['commentCount'])
               channel_id = resp['items'][0]['snippet']['channelId']
               Title = resp['items'][0]['snippet']['title']
               #about is imp later on!!
          except:
              LIKES = None
              Views = None
              CommentsCount=None
          res1 = yts.channels().list(
               part = 'snippet,statistics',
               id = channel_id 
              )
          resp1 = res1.execute()
          try:
              subs = int(resp1['items'][0]['statistics']['subscriberCount'])
          except:
              subs = None
          #created = timezone.now()
          lst.append([Title,Likes,Views,CommentsCount,subs])
          df1 =  pd.DataFrame(lst,columns=['Title','Likes','Views','CommentsCount','Subs'])

          df_json = df1.to_json(orient="records")
          request.session['df2'] = df_json
          return redirect("DB:post")
        else:
            messages.error(request," No links Found! ")
            return redirect("scrape:data")             
    return render(request,"scrape/home.html")        
          
          
                    


          

# def dash(request):
#     return render(request,'scrape/dashboards.html')  
    
def data(request):
    return render(request,"scrape/data.html")

@login_required
def home(request):
    if(request.method=='POST'):
      links = request.POST.get('links')
      form = storeroom(request.POST)
      if form.is_valid():
          scraped_link = form.save(commit=False)
          scraped_link.user = request.user
          scraped_link.save()
      
 
    
      if 'watch?v' in links:

         driver.get(str(links))
         video = driver.find_element(By.TAG_NAME,'video')
         driver.execute_script("document.querySelector('video').pause();") #pausing !

         for i in tqdm(range(0,5000,100)):
            driver.execute_script(f"window.scrollTo(0,{str(i)})")
            time.sleep(.1)
         soup = BeautifulSoup(driver.page_source,"html.parser")
         vid_id = links.split("=")[-1] 
         yt = build('youtube','v3',developerKey="AIzaSyA6IX_Rvr2CQjNiDJ4aAuEmER6Z0PkDSN4")
         #api request to get videos details
         r = yt.videos().list(
            part = "statistics,snippet",
            id = vid_id
         )
         response = r.execute()
         try:
            likes = int(response["items"][0]['statistics']['likeCount'])
            views = int(response["items"][0]['statistics']['viewCount'])
            Published_at =response['items'][0]['snippet']['publishedAt']
            Description = response['items'][0]['snippet']['description']
            AudioLang = response['items'][0]['snippet']['defaultAudioLanguage']
            video_thumbnail = response['items'][0]['snippet']['thumbnails']['standard']['url']
            channel_id = response['items'][0]['snippet']['channelId']

         except:
            print("invalid id")
         al_lst = []
         al_st = []
        #  #channel INFO
        #  request_channel = yt.channels().list(
        #     part = 'snippet,statistics',
        #     id = channel_id
        #  )
        #  response_channel = request_channel.execute()
        #  try:
        #     channel_Published_at = response_channel['items'][0]['snippet']['publishedAt']
        #     Description_channel = response_channel['items'][0]['snippet']['description']
        #     Channel_Name = response_channel['items'][0]['snippet']['title']
        #     Thumbnail = response_channel['items'][0]['snippet']['thumbnails']['medium']['url']
        #     Country = response_channel['items'][0]['snippet']['country']
            


        #  except:
        #     print("invalid channel id")



         title, channel_name, home_channel_link = None,None,None
         #Analysis On Scraping data (its increases time But worth it for Practicing!)
         for div in soup.find_all("ytd-watch-flexy"):
                 title = div.find_all("yt-formatted-string",class_="style-scope ytd-watch-metadata")[0].text
                 channel_name = div.find("a",class_="yt-simple-endpoint style-scope yt-formatted-string").text
                 home_channel_link = "https://www.youtube.com"+div.find("a",class_="yt-simple-endpoint style-scope yt-formatted-string").get("href")
                 subscribers = div.find("yt-formatted-string",class_="style-scope ytd-video-owner-renderer").text
                 s = subscribers.split(" ")[0]
                 if(s[-1]=='M'):
                     subscribers = s.replace("M","")
                     subscribers = int(float(subscribers)*1000000)
                 elif(s[-1]=='B'):
                     subscribers = s.replace("B","")
                     subscribers = int(float(subscribers)*1000000000)
                 elif(s[-1]=='K'):
                     subscribers = s.replace("K","")
                     subscribers = int(float(subscribers)*1000)
                 about = div.find_all("span",class_="yt-core-attributed-string--link-inherit-color")[0].text
                 for i in soup.find_all("span",class_="style-scope yt-formatted-string"):
                     try:
                         if type(int(i.text.replace(",","")))==int:
                              comments = i.text
                              break
                     except:
                            pass
                 comments = comments.replace(",","")
                 comments = int(comments)
                 ls = []
                 ig = []
                 twi = []
                 face = []
                 for i in div.find_all("a"):
                        ls.append(i.get("href"))
                 for i in ls:
                     try:
                        if "instagram.com" in str(i):
                           ig.append(i)
                           break
                        
                     except:
                           ig.append(np.nan)
                 for i in ls:
                     try:
                        if "twitter.com" in str(i):
                            twi.append(i)
                            break
                        
                     except:
                            twi.append(np.nan)

                 for i in ls:
                     try:
                        if "facebook.com" in str(i):
                            face.append(i)
                            break
                          
                     except:
                            face.append(np.nan)
                 ig = "".join(ig)
                 twi = "".join(twi)
                 face = "".join(face)
                 lll = []
                 About = []
                 alternative_link = []
                 for spans in div.find_all('yt-attributed-string',class_ = "style-scope ytd-text-inline-expander"):
                     for i in spans.find_all("span"):
                        lll.append(i.text)
                     abt = " ".join(lll).split(" ")
                 for i in abt:
                     if "https" in i:
                        alternative_link.append(i)
                     if "http" in i:
                        alternative_link.append(i)
                     if "https" and "http" not in i:
                        About.append(i)
                 # alternative_link="".join(alternative_link)
                 About = " ".join(About)
         
         al_st.append([title,likes,views,comments,subscribers,vid_id])
        #  YVdfst = pd.DataFrame(al_st,columns=["Title",'Likes','Views','Comments','Subscribers',"video_id"])
         
         request.session['MediaLinks'] = [channel_name,ig,twi,face,alternative_link]
        #  tohtml = YVdfst.to_html(classes="table table-striped",index=False)
         messages.success(request,f"successfully Scraped! for video {links}! ")

         
         return render(request,'scrape/data.html',{"tohtml":al_st})     
      else:
         
          messages.error(request," invalid link! ")
          return redirect('scrape:home')   
    

    else:
        form = storeroom()

    return render(request,"scrape/home.html")             
def MoreInfomation(request):
    #using API
    if(request.method == 'POST'):
        lst = []
        USER = store.objects.filter(user=request.user).first()
        link = USER.links
        vid_id = link.split("=")[-1]
        channel_id = ""
        Yt   = build("youtube","v3",developerKey="AIzaSyA6IX_Rvr2CQjNiDJ4aAuEmER6Z0PkDSN4")

        # Video INFO
        request_link = Yt.videos().list(
            part = "statistics,snippet",
            id = vid_id

        )
        response = request_link.execute()
        try:
            if(response):
                Published_at =response['items'][0]['snippet']['publishedAt']
                Description = response['items'][0]['snippet']['description']
                AudioLang = response['items'][0]['snippet']['defaultAudioLanguage']
                video_thumbnail = response['items'][0]['snippet']['thumbnails']['standard']['url']
                channel_id = response['items'][0]['snippet']['channelId']
            else:
                print("request cancelled!")
        except:
            print("invalid id")

        #channel INFO
        request_channel = Yt.channels().list(
            part = 'snippet,statistics',
            id = channel_id
        )
        response_channel = request_channel.execute()
        try:
            channel_Published_at = response_channel['items'][0]['snippet']['publishedAt']
            Description_channel = response_channel['items'][0]['snippet']['description']
            channel_name = response_channel['items'][0]['snippet']['title']
            Thumbnail = response_channel['items'][0]['snippet']['thumbnails']['medium']['url']
            Country = response_channel['items'][0]['snippet']['country']
            


        except:
            print("invalid channel id")

        #LINKS WILL BE ADDED BELOW
        medialinks = request.session.get("MediaLinks",None)
        try:
            if(medialinks[1]==None or medialinks[1]==""):
                medialinks[1] = "Not Provided"
            if(medialinks[2]==None or medialinks[2]==""):
                medialinks[2] = "Not Provided"
            if(medialinks[3]==None or medialinks[3]==""):
                medialinks[3] = "Not Provided"
            if(medialinks[4]==None or medialinks[4]==""):
                medialinks[4] = "Not Provided"
        except:
            print("No MediaLinks Found!")



        context = {
            "published_at":Published_at,
            "description":Description,
            "audiolang":AudioLang,
            "channelpublishedate":channel_Published_at,
            "descriptionchannel":Description_channel,
            "channelname":channel_name,
            "thumbnail":Thumbnail,
            "country":Country,
            "instagram":medialinks[1],
            "twitter":medialinks[2],
            "facebook":medialinks[3],
            "otherlinks":medialinks[4],
            "videothumbnail":video_thumbnail
        }
        return render(request,"scrape/Moreinformation.html",context)
    messages.error(request,"No Request Was made For More Information")
    return render(request,"scrape/home.html")



        


        








    
    







             
         
             

   
    
       

    
    
        
    

    






