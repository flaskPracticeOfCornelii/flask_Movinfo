import requests as rq
import os
from datetime import datetime, timedelta
import csv
import pandas

KEY=os.getenv("MOVIE_KEY")
CLOVA_ID=os.getenv("NAVER_CLOVA_ID")
CLOVA_SECRET=os.getenv("NAVER_CLOVA_SECRET")

week_base_url="http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json"
movieInfo_base_url="http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json"
naver_movie_base_url="https://openapi.naver.com/v1/search/movie.json?"


header={
    "X-Naver-Client-Id":CLOVA_ID,
    "X-Naver-Client-Secret":CLOVA_SECRET,
}

######################
# Functions for url  #
######################
def boxoffice_url(key,targetDt):
    
    url=week_base_url+"?key={}&targetDt={}&weekGb=0".format(key,targetDt)
    res=rq.get(url)
    return res

def naver_url(query):
    url=naver_movie_base_url+"query={}".format(query)
    res=rq.get(url,headers=header)
    return res

def movie_info_url(key,movieCd):
    url=movieInfo_base_url+"?key={}&movieCd={}".format(key,movieCd)
    res=rq.get(url)
    return res

######################
# Requests by url    #
######################
def get_boxoffice(targetDt):   
    res=boxoffice_url(KEY,targetDt)
    res=res.json()

    D={}
    for idx in range(10):
        movieCd=res["boxOfficeResult"]["weeklyBoxOfficeList"][idx]["movieCd"]
        movieNm=res["boxOfficeResult"]["weeklyBoxOfficeList"][idx]["movieNm"]
        audiAcc=res["boxOfficeResult"]["weeklyBoxOfficeList"][idx]["audiAcc"]

        D[movieCd]=[movieNm,audiAcc,targetDt]

    return D

def get_movie_info(movieCd):   
    res=movie_info_url(KEY,movieCd)
    res=res.json()

    MovieCd=res["movieInfoResult"]["movieInfo"]["movieCd"]
    MovieNm=res["movieInfoResult"]["movieInfo"]["movieNm"]
    MovieNmEn=res["movieInfoResult"]["movieInfo"]["movieNmEn"]
    MovieNmOg=res["movieInfoResult"]["movieInfo"]["movieNmOg"]
    openDt=res["movieInfoResult"]["movieInfo"]["openDt"]
    showTm=res["movieInfoResult"]["movieInfo"]["showTm"]
    try:
        genreNm=res["movieInfoResult"]["movieInfo"]["genres"][0]["genreNm"]
    except:
        genreNm=""
    try:
        directors=res["movieInfoResult"]["movieInfo"]["directors"][0]["peopleNm"]
    except:
        directors=""
    try:
        watchGradeNm=res["movieInfoResult"]["movieInfo"]["audits"][0]["watchGradeNm"]
    except:
        watchGradeNm=""
    try:
        actor1=res["movieInfoResult"]["movieInfo"]["actors"][0]["peopleNm"]
        actor2=res["movieInfoResult"]["movieInfo"]["actors"][1]["peopleNm"]
        actor3=res["movieInfoResult"]["movieInfo"]["actors"][2]["peopleNm"]
    except:
        actor1,actor2,actor3="","",""

    return [MovieCd,MovieNm,MovieNmEn,MovieNmOg,openDt,showTm,genreNm,directors,watchGradeNm,actor1,actor2,actor3]



def get_naver_info(movieCd,movieNm):
    res=naver_url(movieNm)
    res=res.json()
    try:
        img_url=res["items"][0]["image"]
    except:
        img_url=""
    try:
        link=res["items"][0]["link"]
    except:
        link=""
    try:
        userRating=res["items"][0]["userRating"]
    except:
        userRating=""

    return movieCd,img_url,link,userRating

######################
# Data Manipulation  #
######################

def dictionary_merge(D1,D2):
    #D2 -> D1
    for key,values in D1.items():
        if key in D2:
            if D1[key][1]>D2[key][1]:
                    D2[key][1]=D1[key][1]
        else:
            D2[key]=values
    return D2

def get_boxoffice_10weeks(year,month,day):
    now=datetime(year,month,day)
    tdelta=timedelta(days=-7)

    with open("boxoffice.csv","a",encoding="utf-8",newline="") as csvFile:
        csvwriter=csv.writer(csvFile,delimiter=",")
        D=get_boxoffice(now.strftime("%Y%m%d"))

        for idx in range(1,10):
            tmp_targetDt=now+idx*tdelta
            targetDt=tmp_targetDt.strftime("%Y%m%d")

            cD=get_boxoffice(targetDt)
            D=dictionary_merge(cD,D)

        for key,values in D.items():
            csvwriter.writerow([key,values[0],values[1],values[2]])
    
    return D

######################
# CSV Writing        #
######################

def movie_csv(D):
    Mv_Cd_Nm=[]
    with open("movie.csv","a",encoding="utf-8",newline="") as csvFile:
            csvwriter=csv.writer(csvFile,delimiter=",")
            for key in D.keys():
                movie_info_list=get_movie_info(key)
                csvwriter.writerow(movie_info_list)
                Mv_Cd_Nm.append(movie_info_list[:2])
    return Mv_Cd_Nm

def naver_movie_csv(Mv_Cd_Nm):
    img_list=[]
    with open("movie_naver.csv","a",encoding="utf-8",newline="") as csvFile:
            csvwriter=csv.writer(csvFile,delimiter=",")
            for MvCd,MvNm in Mv_Cd_Nm:
                movie_naver_list=get_naver_info(MvCd,MvNm)
                csvwriter.writerow(movie_naver_list)
                img_list.append(movie_naver_list[:2])
    return img_list
                
def thumb_img(img_list):
    no_image=[]
    for name,url in img_list:
        with open("./images/{}.jpg".format(name),"wb") as f:
            try:
                img=rq.get(url)
                f.write(img.content)
            except:
                no_image.append([name,url])
    return no_image


def csv_files_templates():
    if "images" not in os.listdir():
        os.mkdir("images")

    with open("boxoffice.csv",'w',encoding="utf-8",newline="") as f:
        csvwriter=csv.writer(f,delimiter=",")
        csvwriter.writerow(["movie_code","title","audience","recorded_at"])

    with open("movie_naver.csv",'w',encoding="utf-",newline="") as f:
        csvwriter=csv.writer(f,delimiter=",")
        csvwriter.writerow(["movie_code","thumb_url","link_url","user_rating"])
    
    with open("movie.csv",'w',encoding="utf-",newline="") as f:
        csvwriter=csv.writer(f,delimiter=",")
        csvwriter.writerow(["movie_code","movie_name_ko","movie_name_en","movie_name_og","prdt_year,genres","directors","watch_grade_nm","actor1","actor2","actor3"])

######################
# CSV Reading        #
######################

def get_csv_boxoffice():
    D={}
    try:
        with open("./movie.csv","r",encoding="utf-8") as csvFile:
                csvreader=csv.reader(csvFile,delimiter=",")
                next(csvreader)
                for row in csvreader:
                    D[row[0]]=row[1:]
    except:
        print("No movie.csv exists")
    return D

def get_csv_img():
    imgs=[]
    try:
        with open("./movie_naver.csv","r",encoding="utf-8") as csvFile:
                csvreader=csv.reader(csvFile,delimiter=",")
                next(csvreader)
                for row in csvreader:
                    imgs.append([row[0],row[1]])
    except:
        print("No movie_naver.csv exists")
    return imgs

    