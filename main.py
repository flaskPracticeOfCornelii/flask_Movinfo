from ops import MovieCollector

mc = MovieCollector()
mc.make_csv_files()
mc.gathering_info(2019,1,13)

# mc.update_by_csv()

print(mc.get_code_name())
