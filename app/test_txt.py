import save_data_txt

dict1 = {"one": 1, "two": 2}
dict2 = {"three": 3,  "four": 4, "five": 5}
new_save_data_txt = save_data_txt.data()
new_save_data_txt.write(dict1)
new_save_data_txt.write(dict2)
