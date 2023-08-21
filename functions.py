from main import db


def find_client_using_client_id(client_id):
    client_data = db.child("clients").get().val()  # .child("new").child(client_id)

    for sts in client_data:
        for _client_id in client_data[sts]:
            if _client_id == client_id:
                return client_data[sts][client_id]

    return False


def find_sts_of_client(client_id):
    client_data = db.child("clients").get().val()  # .child("new").child(client_id)

    for sts in client_data:
        for _client_id in client_data[sts]:
            if _client_id == client_id:
                return sts
    return f"Client id <{client_id}> is not found!"


def find_pod_using_uid(uid):
    pods = db.child("pod").get().val()

    for pod_name in pods:
        members_list = pods[pod_name]['members']
        for members_uid in members_list:
            if uid == members_uid:
                return pod_name
    return "Error in finding pod"