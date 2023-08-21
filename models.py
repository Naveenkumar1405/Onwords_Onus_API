from pydantic import BaseModel


class Family_data(BaseModel):
    father_name: str
    mother_name: str
    spouse_name: str
    sibling_name: str
    child_name: str


class Bank_data(BaseModel):
    acc_no: str
    acc_holder_name: str
    branch: str
    ifsc_code: str
    acc_type: str


class Gov_id(BaseModel):
    aadhar_no: str
    pan_no: str


class Adress_Model(BaseModel):
    door_no: str
    street: str
    city: str
    state: str
    pincode: str
    landmark: str


class Staff_model(BaseModel):
    name: str
    phone: str
    email: str
    department: str
    # pod_id: str
    dob: str
    blood_group: str
    profile_pic_url: str
    address: str
    family: Family_data
    designation: str
    emp_id: str
    bank_data: Bank_data
    mode_of_transport: str
    laptop: str
    government_id: Gov_id
    role: str
    password: str


class Enquiry_model(BaseModel):
    lead_source: str
    created_by: str
    enquired_for: str


class Client_model(BaseModel):
    name: str
    phone: str
    address: Adress_Model
    rating: str
    pod_id: str
    enquiry: Enquiry_model



class Change_sts_model(BaseModel):
    pr_uid: str
    state: str
    reason: str


class Client_notes_model(BaseModel):
    pr_user_id: str
    notes: str


class Schedule_model(BaseModel):
    pr_user_id:str
    type: str
    pod_id: str

    date_and_time: str


class Login_model(BaseModel):
    email: str
    password: str


class Uid_model(BaseModel):
    uid: str


class Payment_model(BaseModel):
    payment_id: str
    payment_time: str
    amount: str
    paid_for: str
    pending_payment: str
    uid: str


class Pod(BaseModel):
    name: str
    members: list

class AdData(BaseModel):
    ad_name: str
    platform: str
    full_name: str
    phone_number: str
    email: str
    city: str