# MovieCollector




## Attributes
|Attributes|Description|
|---|--|
|movie_info|**Dictionary** containing information about first 10 list among ones gathered for 10 weeks|
|mv_cd|**List** containing the sublist paired up with movie's code and its name|
|imgs|**List** containing the sublist paired up with movie's code and its ThumbNail img_url if it exists|
|no_imgs|**List** containing the sublist paired up with movie's code and its ThumbNail img_url that could not be found |


## Methods
|Methods|Description|
|---|---|
|MovieCellector()|Construct MovieCollector Object|
|make_csv_files()|Construct MovieCollector Object|
|gathering_info(year,month,day)|it gathered and save information in the object generated|
|update_by_csv()|If csv files(movie.csv, movie_naver.csv,boxoffice.csv) exists it get the data from these csv files|
|get_movie_info()|get an attribute of movie_info |
|get_code_name()|get an attribute of mv_cd |
|get_img_urls()|get an attribute of imgs |
|get_no_imgs()|get an attribute of no_imgs |



## Generated files
### 1. boxoffice.csv
movie_code,title,audience,recorded_at

### 2. movie_naver.csv
movie_code,thumb_url,link_url,user_rating

### 3. movie.csv
movie_code,movie_name_ko,movie_name_en,movie_name_og,"prdt_year,genres",directors,watch_grade_nm,actor1,actor2,actor3

## Examples
### python
```python
from ops import MovieCollector

mc = MovieCollector()  # generate object
mc.make_csv_files()    # making csv file 
mc.gathering_info(2019,1,13) # gathering information and it automatically fill in the three csv files

```

```python
from ops import MovieCollector
mc = MovieCollector()
mc.update_by_csv()

```