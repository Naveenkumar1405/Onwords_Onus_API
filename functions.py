from main import db

def find_client_using_client_id(client_id):
    client_data = db.child("clients").get().val()
    if client_data:
        for sts in client_data:
            for _client_id in client_data[sts]:
                if _client_id == client_id:
                    return client_data[sts][_client_id]
    return None

def find_sts_of_client(client_id):
    client_data = db.child("clients").get().val()
    
    if client_data:
        for sts in client_data:
            for _client_id in client_data[sts]:
                if _client_id == client_id:
                    return sts
    return None

def find_pod_using_uid(uid):
    pods = db.child("pod").get().val()

    for pod_name in pods:
        members_list = pods[pod_name]['members']
        for members_uid in members_list:
            if uid == members_uid:
                return pod_name
    return "Error in finding pod"