import pyrebase

firebaseConfig={"apiKey": "AIzaSyBSaNWZH_N9fb-1ExTxET4bqfGGEmbjjhw",
  "authDomain": "work-sample-test.firebaseapp.com",
  "databaseURL": "https://work-sample-test-default-rtdb.firebaseio.com",
  "projectId": "work-sample-test",
  "storageBucket": "work-sample-test.appspot.com",
  "messagingSenderId": "776126785760",
  "appId": "1:776126785760:web:59d986efc982eb7e1c0885",
  "measurementId": "G-Q5SNEE822W"}

firebase=pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
fname = db.child('Forms').child().get()
#data = {
 #           'field_type': fname.child().val()[0]
  #      }
    
#print(fname.val())
#print(data)
data = []
for key in fname.val():
  data.append(key[0:])
  print(data)


