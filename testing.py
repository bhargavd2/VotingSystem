from firebase import Firebase

config = {
    "apiKey": "AIzaSyBL-6E-f1GGYmxqOqJMvI1AekPzIORCr38",
    "authDomain": "voting-7f2da.firebaseapp.com",
    "databaseURL": "https://voting-7f2da-default-rtdb.firebaseio.com",
    "projectId": "voting-7f2da",
    "storageBucket": "voting-7f2da.appspot.com",
    "messagingSenderId": "767619014270",
    "appId": "1:767619014270:web:c137edd767ac4dda98422f"
}
firebase = Firebase(config)

auth = firebase.auth()

db = firebase.database()
'''
user = auth.sign_in_with_email_and_password("a@t.com", "123456")

print(user["localId"])
print(user["email"])'''


c = db.child("candidates").get()
data=[]
for i in c.each():
    a = i.val()
    b = i.key()
    if a == None:
        continue
    a.pop("votes")
    data.append(a)
print(data)
'''
v = db.child("voters").get()
for user in v.each():
    a = user.val()
    b = user.key()
    if a == None:
        continue
    a["status"]=True
    db.child("voters").child(b).update(a)
print("done")
# e = db.child("election").get()
# print(e.val())
# print(e.key())
'''