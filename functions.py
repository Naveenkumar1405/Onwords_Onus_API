from main import db
from fastapi import HTTPException

def find_client_using_client_id(client_id):
    try:
        client_data = db.child("clients").get().val()
        if client_data:
            for sts in client_data:
                for _client_id in client_data[sts]:
                    if _client_id == client_id:
                        return client_data[sts][_client_id]
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding client: {str(e)}")

def find_sts_of_client(client_id):
    try:
        client_data = db.child("clients").get().val()
        if client_data:
            for sts in client_data:
                for _client_id in client_data[sts]:
                    if _client_id == client_id:
                        return sts
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding client status: {str(e)}")

def find_pod_using_uid(uid):
    try:
        pods = db.child("pod").get().val()
        for pod_name in pods:
            members_list = pods[pod_name]['members']
            for members_uid in members_list:
                if uid == members_uid:
                    return pod_name
        return "Error in finding pod"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding pod: {str(e)}")
