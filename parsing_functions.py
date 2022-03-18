
def getOccurrencesOfWords(messages_list, words_list):

    words_dict = {}
    for w in words_list:
        words_dict[w.lower()] = 0

    for msg in messages_list:

        if not msg["text"]:
            continue

        for word in msg["text"].split():

            word = word.lower()
            if word in words_dict.keys():
                words_dict[word] += 1

    return words_dict


def getMessagesPerPerson(messages, group_info, top_limit=7):

    members_info = group_info["members_info"]

    for mem in members_info:
        members_info[mem]["count"] = 0

    for m in messages:

        if m["sender_id"] in members_info.keys():
            members_info[m["sender_id"]]["count"] += 1

        else:
            members_info[m["sender_id"]] = {
                "nickname": m["sender_name"],
                "count": 1
            }

    sorted_ids = sorted(members_info.keys(),
                        key=lambda x: members_info[x]["count"])[-top_limit:]

    return {
        "labels": [members_info[l]["nickname"] for l in sorted_ids],
        "data": [members_info[c]["count"] for c in sorted_ids],
    }


def getLikesPerMessageRatio(messages, group_info, top_limit=7, threshold_messages=0):

    members_info = group_info["members_info"]

    for mem in members_info:
        members_info[mem]["count"] = 0
        members_info[mem]["total_likes"] = 0
        members_info[mem]["likes_to_msg_ratio"] = 0

    for m in messages:

        if m["sender_id"] in members_info.keys():
            members_info[m["sender_id"]]["count"] += 1
            members_info[m["sender_id"]]["total_likes"] += len(m["liked_by"])

        else:
            members_info[m["sender_id"]] = {
                "nickname": m["sender_name"],
                "count": 1,
                "total_likes": len(m["liked_by"])
            }

    for mem in list(members_info):
        if members_info[mem]["count"] <= threshold_messages:
            del members_info[mem]

    for mem in members_info:

        if members_info[mem]["count"] != 0:
            members_info[mem]["likes_to_msg_ratio"] = members_info[mem]["total_likes"] / \
                members_info[mem]["count"]

    sorted_ids = sorted(members_info.keys(),
                        key=lambda x: members_info[x]["likes_to_msg_ratio"])[-top_limit:]

    return {
        "labels": [members_info[l]["nickname"] for l in sorted_ids],
        "data": [members_info[m]["likes_to_msg_ratio"] for m in sorted_ids],
    }
