import time
import uvicorn as uvicorn
from fastapi import FastAPI, HTTPException
import pyrebase
import functions
import models
from firebase_admin import db
app = FastAPI()
config = {
    "apiKey": "AIzaSyBb1Age-jnJPIQJDnGFEtbAUPfJm7GdBiI",
    "authDomain": "onwords-master-db.firebaseapp.com",
    "databaseURL": "https://onwords-master-db-default-rtdb.firebaseio.com",
    "projectId": "onwords-master-db",
    "storageBucket": "onwords-master-db.appspot.com",
    "messagingSenderId": "956596402862",
    "appId": "1:956596402862:web:8355b18cb727e935588b3f"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()


@app.get("/")
def read_root():
    return {"Hello": "This is onus api"}


@app.post("/create_staff")
def create_staff(staff: models.Staff_model):
    # if len(staff.phone) != 10:
    #     return "invalid ph no"

    email = staff.email
    password = staff.password
    # create a new user
    try:
        user = auth.create_user_with_email_and_password(email, password)
        uid = user['localId']

        data = {
            'name': staff.name,
            'phone': staff.phone,
            'email': staff.email,
            'department': staff.department,
            'dob': staff.dob,
            'blood_group': staff.blood_group,
            'profile_pic_url': staff.profile_pic_url,
            'address': staff.address,
            'family': staff.family.dict(),
            'designation': staff.designation,
            'emp_id': staff.emp_id,
            'bank_data': staff.bank_data.dict(),
            'mode_of_transport': staff.mode_of_transport,
            'laptop': staff.laptop,
            'government_id': staff.government_id.dict(),
            'role': staff.role

        }

        db.child("staff").child(uid).set(data)
        return "Created Staff Successfully...!"
    except Exception as e:
        return e

    # return uid


@app.post("/staff/login")
def get_staff_uid(login: models.Login_model):
    email = login.email
    password = login.password
    try:
        login_data = auth.sign_in_with_email_and_password(email, password)
        uid = login_data['localId']
        return uid
    except Exception as e:
        return e


@app.get('/client/state')
def client_states():
    client_state = db.child("clients").get().val()
    statelist = []
    for state in client_state:
        statelist.append(state)
    return statelist


@app.post('/client/getstate/{state}/{pod}')
def client_states_post(state: str, pod: str):
    new_client_data = db.child("clients").child(state).get().val()
    new_client_list = []
    for client in new_client_data:
        client_pod = new_client_data[client]['pod_id']
        if client_pod == pod:
            new_client_list.append(new_client_data[client])

    return new_client_list


@app.get('/pod/names')
def get_pod_names():
    pods = db.child('pod').get().val()
    pod_name_list = []
    for pod in pods:
        pod_name_list.append(pod)

    return pod_name_list


# @app.post("/cust/data")
# def get_staff_data_with_uid(uid: models.Uid_model):
#     staff_data = db.child("staff").child(uid.uid).get().val()
#     pod_id=staff_data["pod_id"]
#     try:
#         clientnumber=[]
#         clientstate=[]
#         clients=db.child("clients").get().val()
#         for state in clients:
#             for number in clients[state]:
#                 if clients[state][number]["pod_id"] == pod_id:
#                     clientnumber.append(clients[state][number])
#                     clientstate.append(state)
#         return clientnumber,clientstate
#     except Exception as e:
#         return e

@app.post("/staff/tagged_client/new")
def get_tagged_client(uid: models.Uid_model):
    client_data = db.child("clients").child("new").get().val()
    new_client_data = []
    for client in client_data:
        new_client_data.append(client_data[client])
    return new_client_data


@app.post("/pod/create")
def create_pod(pod: models.Pod):
    data = {
        "name": pod.name,
        "members": pod.members
    }
    db.child("pod").child(pod.name).set(data)
    return f"Created {pod.name} pod!"


@app.post("/staff/data")
def get_staff_data_with_uid(uid: models.Uid_model):
    staff_data = db.child("staff").child(uid.uid).get().val()
    return staff_data


@app.get("/staff/alldata/")
def get_staff_alldata():
    staff_data = db.child("staff").get().val()
    staffnamelist = []
    staffuidlist = []
    for staffuid in staff_data:
        if staff_data[staffuid]["role"] == "PR":
            staffnamelist.append(staff_data[staffuid]["name"])
            staffuidlist.append(staffuid)
    return staffnamelist, staffuidlist


@app.get("/staff/data/all")
def get_all_staf_data():
    staff_data = db.child("staff").get().val()
    return staff_data


@app.get("/staff/pod/{uid}")
def get_staffs_pod_with_uid(uid: str):
    pods = db.child("pod").get().val()
    for pod in pods:
        members = pods[pod]['members']
        for member in members:
            if member == uid:
                return pod

    return "Not found!"



@app.get("/client/pod/{pod_name}")
def get_client_tagged_with_pod_name(pod_name: str):
    new_client_data = db.child("clients").child("new").get().val()
    new_client_list = []
    for client in new_client_data:
        client_pod = new_client_data[client]['pod_id']
        if client_pod == pod_name:
            new_client_list.append(new_client_data[client])

    return new_client_list


@app.get("/staff/data/name")
def get_all_staf_data():
    staff_name = []
    staff_data = db.child("staff").get().val()
    for staff in staff_data:
        staff_name.append(staff_data[staff]['name'])
    return staff_name


@app.get("/all_numbers")
def get_all_numbers_in_database():
    client_data = db.child('clients').get().val()
    client_number_list = []

    for sates in client_data:
        for client_numbers in client_data[sates]:
            client_number_list.append(client_numbers)

    return client_number_list


@app.post("/create_client")
def create_client1(client: models.Client_model):
    data = {
        'name': client.name,
        'phone': client.phone,
        'address': client.address.dict(),
        'rating': client.rating,
        'pod_id': client.pod_id,
        'enquiry': client.enquiry.dict(),

    }
    db.child('clients').child("new").child(client.phone).set(data)
    return "Created client successfully...!"


@app.get("/client/{client_id}")
def client_data(client_id: str):
    return functions.find_client_using_client_id(client_id)


@app.post("/client/{client_id}/add_notes")
def add_notes_to_client(client_id: str, notes: models.Client_notes_model):
    data = {
        "pr_user_id": notes.pr_user_id,
        "timestamp": time.time(),
        "notes": notes.notes
    }
    db.child("clients").child(functions.find_sts_of_client(client_id)).child(client_id).child("notes").push(data)
    return f"Notes added successfully..!"


@app.post("/client/{client_id}/sts/{sts}")
def change_sts_of_client(client_id: str, sts: str, sts_model: models.Change_sts_model):
    old_sts = functions.find_sts_of_client(client_id)
    if old_sts == sts:
        return f"client is already in {sts}. No changes have been made!"
    else:
        db.child("clients").child(sts).child(client_id).set(functions.find_client_using_client_id(client_id))
        time.sleep(1)
        db.child("clients").child(old_sts).child(client_id).remove()
        data = {
            "pr_uid": sts_model.pr_uid,
            "state": sts_model.state,
            "reason": sts_model.reason,
            "time": time.time()
        }
        db.child("clients").child(sts).child(client_id).child("status").push(data)
        client_new_data = db.child("clients").child(sts).child(client_id).get().val()
        return client_new_data

@app.post("/client/{client_id}/create_schedule")
def Create_client_schedule(client_id: str, schedule_model: models.Schedule_model):
    data = {
        "type": schedule_model.type,
        "pod_id": schedule_model.pod_id,

        "date_and_time": schedule_model.date_and_time,
        "schedule_created_timestamp": time.time()

    }
    db.child("clients").child(functions.find_sts_of_client(client_id)).child(client_id).child("schedule").push(data)
    data2 = {
        "type": schedule_model.type,
        "pod_id": schedule_model.pod_id,
        "pr_user_id":schedule_model.pr_user_id,

        "date_and_time": schedule_model.date_and_time,
        "schedule_created_timestamp": time.time(),
        "client_id": client_id

    }
    db.child("schedule").child(schedule_model.type).push(data2)

@app.get("/schedule/{uid}")
def Get_staffs_schedule_taged_to_therir_pod_using_uid(uid:str):
    schedule_datas = db.child("schedule").get().val()
    user_pod = functions.find_pod_using_uid(uid)
    schedules = []
    for schedule_type in schedule_datas:
        type = schedule_datas[schedule_type]
        for schedule in type:
            pod = type[schedule]['pod_id']
            if pod == user_pod:
                schedules.append(type[schedule])
    return schedules

@app.get("/client/{number}")
def Client_Profile_with_Number(number: str):
    try:
        client_data = db.child("clients").child(number).get().val()
        return client_data
    except:
        return f"{number}'s data not found!"

# TODO Schedule clients
@app.post("/client/{client_id}/payments")
def Create_client_schedule(client_id: str, payment: models.Payment_model):
    data = {
        "payment_id": payment.payment_id,
        "payment_time": payment.payment_time,
        "amount": payment.amount,
        "paid_for": payment.paid_for,
        "pending_payment": payment.pending_payment,
        "uid": payment.uid
    }
    db.child("clients").child(functions.find_sts_of_client(client_id)).child(client_id).child("payments").child(
        payment.payment_id).set(data)



@app.post("/save_data/")
async def save_data(data: models.AdData):
    try:
        phone_id = data.phone_number  # Use phone number as the ID
        db.child("ads").child(phone_id).set(data.dict())
        return {"status": "Data saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.1.116", port=8000, reload=True)