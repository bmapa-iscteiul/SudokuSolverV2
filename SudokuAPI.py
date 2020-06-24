import requests

def generateSudoku():
    r = requests.get("https://sugoku.herokuapp.com/board?difficulty=hard")
    json_object = r.json()
    print(json_object['board'])
    return json_object['board']