from flask import Flask, render_template,request
from ops import MovieCollector

mc = MovieCollector()
mc.update_by_csv()

app=Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/movie")
def movie():
    
    return render_template("movie.html")
    
@app.route("/boxoffice")
def boxoffice():
    key=request.args.get("key")
    if key=="ssafy_seoul1":
         json2=mc.send_json()
    else:
        json2="Wrong Approach"
    return render_template("boxoffice.html",json=json2)
    

### if token==ssafy,then


if __name__=="__main__":
    
    # mc.make_csv_files()
    # mc.gathering_info(2019,1,13)
    pass