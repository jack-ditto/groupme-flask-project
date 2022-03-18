import requests
from pathlib import Path
from parsing_functions import *
import os
import datetime
import json
API_BASE_URL = "https://api.groupme.com/v3"


def getMyId(access_token):

    endpoint = "/users/me"
    params = {"token": access_token}
    req = requests.get(API_BASE_URL + endpoint, params=params)

    if req.status_code != 200:
        return

    return req.json()["response"]["id"]


def initMe(access_token):

    curr_user_id = getMyId(access_token)
    Path("./data/" + curr_user_id).mkdir(parents=True, exist_ok=True)


def getAllGroups(access_token):

    # Request pages of groups
    def getGroup(page=1):
        endpoint = "/groups"
        params = {
            "page": page,
            "token": access_token,
            "omit": "memberships"
        }
        return requests.get(API_BASE_URL + endpoint, params=params)

    i = 2
    resp = getGroup()
    groups_info = []
    while (resp) and (resp.status_code == 200) and (resp.json()["response"]):

        for g in resp.json()["response"]:
            group = {}
            group["name"] = g["name"]
            group["id"] = g["id"]
            groups_info.append(group)
        i += 1
        resp = getGroup(page=i)

    return groups_info


def groupIdIsValid(group_id, access_token):
    endpoint = "/groups/" + group_id
    params = {
        "token": access_token
    }

    resp = requests.get(API_BASE_URL + endpoint, params=params)

    if resp.status_code == 200:
        return True

    return False


def getAllMessages(group_id, access_token):

    def getPage(max_limit=100, before_id=None):
        endpoint = "/groups/" + group_id + "/messages"
        params = {
            "before_id": before_id,
            "limit": max_limit,
            "token": access_token
        }
        return requests.get(API_BASE_URL + endpoint, params=params)

    all_messages_info = []
    resp = getPage()

    while (resp) and (resp.status_code == 200) and (resp.json()["response"]):

        for m in resp.json()["response"]["messages"]:
            msg = {}
            msg["text"] = m["text"]
            msg["created_at"] = m["created_at"]
            msg["msg_id"] = m["id"]
            msg["sender_id"] = m["user_id"]
            msg["sender_name"] = m["name"]
            msg["liked_by"] = m["favorited_by"]
            oldest_id = m["id"]
            all_messages_info.append(msg)

        resp = getPage(before_id=oldest_id)

    return all_messages_info


def getMessagesLastUpdated(my_id, group_id):
    path = "./data/" + my_id + "/" + group_id + ".json"

    try:
        time_mod = os.stat(path).st_mtime
        time_mod_dt = datetime.datetime.fromtimestamp(time_mod)

        return datetime.datetime.today() - time_mod_dt

    except Exception as e:

        if(e == FileNotFoundError):
            return None


def loadAllMessagesData(my_id, group_id, access_token, reload_messages=False):

    path = "./data/" + my_id + "/" + group_id + ".json"
    if (reload_messages == True) or (getMessagesLastUpdated(my_id, group_id) == None):
        # Load messages from API and store in file
        messages = getAllMessages(group_id, access_token)
        with open(path, "w+") as f:
            json.dump(messages, f)

        return messages
    else:
        # Load messages from file and return
        with open(path, "r") as f:
            messages = json.load(f)
        return messages


def getGroupInfo(group_id, access_token):

    endpoint = API_BASE_URL + "/groups/" + str(group_id)
    params = {
        "id": group_id,
        "token": access_token
    }
    res = requests.get(endpoint, params).json()

    num_members = len(res["response"]["members"])
    created_on = res["response"]["created_at"]
    created_on = datetime.datetime.utcfromtimestamp(
        created_on).strftime("%B %d, %Y")

    members_info = {}
    for m in res["response"]["members"]:

        members_info[m["user_id"]] = {
            "nickname": m["nickname"]
        }

    return {
        "num_members": num_members,
        "created_on": created_on,
        "members_info": members_info
    }
