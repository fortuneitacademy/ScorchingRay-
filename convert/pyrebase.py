import pyrebase
import urllib

config = {
  "apiKey": "AIzaSyAGz0NylOh-nKxBstZSN9wjHtql331Uxas",
  "authDomain": "stlconverter-1f730.firebaseapp.com",
  "projectId": "stlconverter-1f730",
  "databaseURL": "https://stlconverter-1f730-default-rtdb.firebaseio.com",
  "storageBucket": "stlconverter-1f730.appspot.com",
  "messagingSenderId": "214485460624",
  "appId": "1:214485460624:web:32025468feb52158321a15",
  "measurementId": "G-QCZ2DSH4EG"
}
print(dir(pyrebase))
ayth_storage = pyrebase.initialize_app(config)
db = ayth_storage.database()
st = ayth_storage.storage()
file = 'main.kv'
cludname = 'kivy/main.txt'
st.child(cludname).put(file)
print(st.child(cludname).get_url(None))
print(urllib.request.urlopen(st.child(cludname).get_url(None)).read())