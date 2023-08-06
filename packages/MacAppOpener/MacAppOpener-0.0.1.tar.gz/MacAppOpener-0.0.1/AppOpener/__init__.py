import os
from difflib import SequenceMatcher



def open(app):
    item_list = []
    for item in os.listdir("/Applications/"):
        item_path = os.path.join("/Applications/", item)
        item_list.append(item_path)

    highest_similarity = 0.0
    most_similar_string = None

    for string in item_list:
        similarity_ratio = SequenceMatcher(None, app, string).ratio()
        if similarity_ratio > highest_similarity:
            highest_similarity = similarity_ratio
            most_similar_string = string
    print(most_similar_string)
    # os.system("open " + most_similar_string)
    # if ' ' in most_similar_string:
    #     most_similar_string = os.path.join(".", most_similar_string)
    #     os.system("open" + most_similar_string)
    # else:
    formatted_file_path = f'"{most_similar_string}"'
    command = f'open {formatted_file_path}'
    os.system(command)

open("SF")