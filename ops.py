from utils import get_boxoffice_10weeks, get_movie_info, get_naver_info
from utils import movie_csv,naver_movie_csv, thumb_img, csv_files_templates
from utils import get_csv_boxoffice, get_csv_img
import json

class MovieCollector:
    def __init__(self):
        self.movie_info = None
        self.mv_cd = None
        self.imgs = None
        self.no_imgs = None

    def gathering_info(self,year,month,day):
        D = get_boxoffice_10weeks(year,month,day)
        Mv_Cd_Nm = movie_csv(D)
        img_list = naver_movie_csv(Mv_Cd_Nm)
        no_image = thumb_img(img_list)

        self.movie_info = D
        self.mv_cd = Mv_Cd_Nm
        self.imgs = img_list
        self.no_imgs = no_image
        
    def get_movie_info(self):
        return self.movie_info

    def get_code_name(self):
        return self.mv_cd

    def get_img_urls(self):
        return self.imgs

    def get_no_imgs(self):
        return self.no_imgs

    def make_csv_files(self):
        csv_files_templates()

    def update_by_csv(self):
        D = get_csv_boxoffice()
        self.movie_info = D
        self.imgs = get_csv_img()

        if D != {}:
            L=[]
            for key,values in D.items():
                L.append([key,values[0]])
            self.mv_cd=L

    def send_json(self):
        return json.dumps(self.movie_info,ensure_ascii = False)








