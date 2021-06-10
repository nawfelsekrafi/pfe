from datetime import date
import datetime
import pyrebase
import firebase_admin
from firebase_admin import credentials, db
import json

# time
today = date.today()
m = str(today.strftime("%m"))
d = str(today.strftime("%d"))
y = str(20) + str(today.strftime("%y"))
w = today.isocalendar()[1]
date = d + " " + m + " " + y
day_name = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
today = day_name[day]


def get_today():
    return today


# config
config = {
    "apiKey": "AIzaSyBMDDOwcndSDbAzRlqYMZ4w0GWCJ_kLVHU",
    "authDomain": "backend-347db.firebaseapp.com",
    "databaseURL": "https://backend-347db-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "backend-347db",
    "storageBucket": "backend-347db.appspot.com",
    "messagingSenderId": "278802640563",
    "appId": "1:278802640563:web:5143a4bc0ef6997c9a8ac6"
}
# initialize
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


def get_students_data():
    # Connection with firebase
    cred = credentials.Certificate('./ServiceAccountKey.json')
    default_app = firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://backend-347db-default-rtdb.europe-west1.firebasedatabase.app/'
    })

    ref = db.reference("/")

    # post students info
    with open("students.json", "r") as f:
        file_contents = json.load(f)
    ref.set(file_contents)
    ref = db.reference("/")

    organ_name = "Intellect"
    # get students info
    students = []
    q = ref.order_by_child("age").get()
    for key, value in q.items():
        # test on organization
        for j in value["organization"]:
            if j["name"].lower() == organ_name.lower():
                for i in value["weeks_of_study"]:
                    if str(i["year"]) == y and str(i["n"]) == str(w):  # and i["week"] ==
                        for k in i["days"]:
                            if today == k["n"]:
                                students.append(value)
    return students


def download_students_avatars(students):
    for s in students:
        print(s["name"])
        img_title = str(s["phone_number"]) + ".jpg"
        # download Student pics
        path_on_cloud = "images/" + img_title
        storage.child(path_on_cloud).download("./images/students_avatars/" + img_title)


def download_organization_logo(organ_name):
    organ_logo_name = organ_name.lower() + ".jpg"
    path_on_cloud = "logos/" + organ_logo_name
    storage.child(path_on_cloud).download("./images/organ_logo/" + organ_logo_name)
