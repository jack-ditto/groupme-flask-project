from flask import Flask, session, request, render_template, redirect, url_for, jsonify
import request_functions as rf
import parsing_functions as pf
import requests
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
app.secret_key = 'thisisiasecretkeyrighthere!'

API_BASE_URL = 'https://api.groupme.com/v3'
API_ME_URL = API_BASE_URL + '/users/me'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/data')
def data():
    if not session.get('api_token'):
        return redirect(url_for('home'))

    return render_template('data.html')


@app.route('/init', methods=['GET', 'POST'])
def initUser():

    if request.method == 'POST':
        # Check if API token is valid
        api_token = request.form.get('api_token', False)
        params = {'token': api_token}
        res = requests.get(API_ME_URL, params=params)

        if res.status_code == 500:
            return {'response': res.status_code, 'error_msg': 'Something is broken on the server!'}

        if res.status_code != 200:
            # This means the API token is incorrect, so redirect
            return {'response': res.status_code, 'error_msg': 'API token incorrect.'}

        user_id = res.json()['response']['id']

        # Store api token, user id in session
        session['api_token'] = request.form['api_token']
        session['user_id'] = user_id

        return {'response': res.status_code}
    else:
        return 'GET!'


@app.route('/groups')
def getGroups():
    api_token = session['api_token']

    groups = rf.getAllGroups(api_token)

    return jsonify(groups)


@app.route('/countMessages')
def getNumMessages():

    my_id = session['user_id']
    api_token = session['api_token']
    group_id = request.args.get('group_id')

    reload_messages = True if request.args.get(
        'reload_messages') == "true" else False

    messages = rf.loadAllMessagesData(
        my_id, group_id, api_token, reload_messages=reload_messages)
    return jsonify(len(messages))


@app.route('/groupInfo')
def getGroupInfo():

    api_token = session['api_token']
    group_id = request.args.get('group_id')

    group_info = rf.getGroupInfo(group_id, api_token)

    return {
        "num_members": group_info["num_members"],
        "created_on": group_info["created_on"],
    }


@app.route('/messagesPerPerson')
def getMessagesPerPerson():

    api_token = session['api_token']
    my_id = session['user_id']
    group_id = request.args.get('group_id')
    reload_messages = True if request.args.get(
        'reload_messages') == "true" else False

    messages = rf.loadAllMessagesData(
        my_id, group_id, api_token, reload_messages=reload_messages)

    group_info = rf.getGroupInfo(group_id, api_token)

    messages_per_person_data = pf.getMessagesPerPerson(messages, group_info)

    return messages_per_person_data


@app.route('/likesPerMessage')
def getLikesPerMessage():

    api_token = session['api_token']
    my_id = session['user_id']
    group_id = request.args.get('group_id')
    reload_messages = True if request.args.get(
        'reload_messages') == "true" else False

    messages = rf.loadAllMessagesData(
        my_id, group_id, api_token, reload_messages=reload_messages)

    group_info = rf.getGroupInfo(group_id, api_token)

    likes_to_message_ratio_data = pf.getLikesPerMessageRatio(
        messages, group_info)
    print(likes_to_message_ratio_data)
    return likes_to_message_ratio_data

    # @app.route('/testSession')
    # def testSession():
    #     return session['api_token']
