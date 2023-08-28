import time,functions,models
import uvicorn as uvicorn
from fastapi import FastAPI, HTTPException
import pyrebase

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
    return {"Hello": "THIS IS ONUS API"}

@app.post("/create_staff")
def create_staff(staff: models.Staff_model):
    email = staff.email
    password = staff.password
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
    status = functions.find_sts_of_client(client_id)
    if status is None:
        return f"Client {client_id} not found."

    db.child("clients").child(status).child(client_id).child("notes").push(data)
    return f"Notes added successfully..!"

@app.post("/status_change/{client_id}")
def change_sts_of_client(client_id: str, status_model: models.ChangeStatusModel):
    old_sts = functions.find_sts_of_client(client_id)
    if old_sts == status_model.status:
        raise HTTPException(status_code=400, detail=f"Client is already in {status_model.status}. No changes have been made!")
    else:
        client_data = functions.find_client_using_client_id(client_id)
        if client_data:
            db.child("clients").child(status_model.status).child(client_id).set(client_data)
            
            db.child("clients").child(old_sts).child(client_id).remove()
            
            data = {
                "pr_uid": status_model.pr_uid,
                "status": status_model.status
            }
            db.child("clients").child(status_model.status).child(client_id).child("status").update(data)
           
            client_new_data = db.child("clients").child(status_model.status).child(client_id).get().val()
            
            return client_new_data
        else:
            raise HTTPException(status_code=404, detail=f"Client with id {client_id} not found")

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
def get_schedules_data(uid: str):
    schedule_datas = db.child("schedule").get().val()
    user_pod = functions.find_pod_using_uid(uid)
    schedules = []

    for schedule_type, schedules_data in schedule_datas.items():
        for schedule_id, schedule in schedules_data.items():
            pod = schedule['pod_id']
            if pod == user_pod:
                schedule['schedule_id'] = schedule_id
                schedules.append(schedule)

    return schedules

@app.delete("/delete_schedule/{schedule_id}")
def delete_schedule(schedule_id: str):
    schedule_datas = db.child("schedule").get().val()
    for schedule_type, schedules in schedule_datas.items():
        if schedule_id in schedules:
            schedules.pop(schedule_id)
            db.child("schedule").child(schedule_type).set(schedules)
            return {"message": "Schedule deleted successfully"}
    raise HTTPException(status_code=404, detail="Schedule not found")

@app.put("/mark_schedule_done/{schedule_id}")
def mark_schedule_done(schedule_id: str):
    schedule_datas = db.child("schedule").get().val()
    for schedule_type, schedules in schedule_datas.items():
        if schedule_id in schedules:
            schedules[schedule_id]["status"] = "Done"
            db.child("schedule").child(schedule_type).set(schedules)
            return {"message": "Schedule marked as done"}
    raise HTTPException(status_code=404, detail="Schedule not found")

@app.get("/client/{number}")
def Client_Profile_with_Number(number: str):
    try:
        client_data = db.child("clients").child(number).get().val()
        return client_data
    except:
        return f"{number}'s data not found!"

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
    
@app.post("/save_uploaded_clients/")
def save_uploaded_clients(uploaded_clients: list[models.UploadedClient]):
    try:
        ref = db.reference("uploaded_clients")
        for client in uploaded_clients:
            client_data = {
                "ad_name": client.ad_name,
                "platform": client.platform,
                "full_name": client.full_name,
                "phone_number": client.phone_number,
                "email": client.email,
                "city": client.city
            }
            ref.push().set(client_data)
        return {"message": "Data successfully saved"}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.1.18", port=8155, reload=True)