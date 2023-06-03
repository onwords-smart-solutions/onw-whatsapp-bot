import json

from fastapi import FastAPI, Request, Header
from fastapi.templating import Jinja2Templates
import requests, keys, pyrebase
from twilio.rest import Client

app = FastAPI()
templates = Jinja2Templates(directory="templates")

account_sid = keys.account_sid
auth_token = keys.auth_token
client = Client(account_sid, auth_token)

databse = pyrebase.initialize_app(keys.config)
db = databse.database()
# db = firebase.database()


def whatsapp(reply, _from="whatsapp:+18144812393"):
    global from_
    message = client.messages.create(
        body=reply,
        to=from_,
        from_=_from
    )


url = "http://117.247.181.113:8000/"


def device(room, sts):
    device_data = requests.get(url).json()
    for ids in device_data:
        if room == ids['Room'].lower():
            _url = url + str(ids['id']) + "/"
            if sts == "on":
                requests.put(_url, json={"Device_Status": True})
            elif sts == "off":
                requests.put(_url, json={"Device_Status": False})
        # else:
        #     print(f'{room} is not equal to {ids["Room"]}')


def queryContains(a):
    global body
    for x in a:
        if x in body:
            # print(f'{x} is in {body}')
            return True
    return False


def checkOfficeServerStatus():
    try:
        _temp = requests.get("http://office.onwordsapi.com/sts/",timeout=3)
        return True
    except:
        return False


@app.get("/")
async def home(request: Request):
    base_url = "https://api.twilio.com/2010-04-01/Accounts/"
    messages_url = f"{base_url}{account_sid}/Messages.json"
    response = requests.get(messages_url, auth=(account_sid, auth_token))
    if response.status_code == 200:
        messages = response.json()["messages"]
        return templates.TemplateResponse("messages.html", {"request": request, "messages": messages})
    else:
        return {"error": response.text}


global body, from_

# def storeInDb():
#     db.child("+919095640275").push({"name": "Nikhil"})

def reply(body, _from):
    # print("inside the reply function >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    try:
        userData = db.child(_from).get().val()
        # print(userData)
        if userData == None:

            user = False
        elif userData['name'] == False:
            whatsapp('May I rembember your name as {}\nreply with "yes" to save your name\n"no" to reenter'.format(body.capitalize()))
            db.child(_from).update({'name': body,'pending':'yes or no'})
        elif userData['pending'] =='yes or no':
            if body == "yes":
                whatsapp('saving your name as {}'.format(userData['name'].capitalize()))
                db.child(_from).update({'name': userData['name'],'pending':'none'})
                # if userData['firstAskedQuestion']

            elif body == "no":
                whatsapp('ok, Please enter your name again')
                db.child(_from).update({'name': False})
            else:
                whatsapp('Please reply with yes or no')
        else:
            user  =True
    except Exception as e:
       print('errprr is ', e)
       whatsapp('Can\'t handle the current laod. surver is too busy.\nError code is 12')
    # print(user)


    if user:
        name = userData['name'].capitalize()
        print(name)
    else:
        whatsapp('Hey,\nBefore answering that may I know what shall I call you?\nEnter your name:')
        db.child(_from).update({'name': False,'firstAskedQuestion':body})
        # print("returning")
        return


    if queryContains(['off', 'turn', 'on']):
        if queryContains(['light', 'tubelight', 'lights']):
            if queryContains(['room', 'garage']):
                if queryContains(['admin', 'green', 'garage']):
                    if queryContains(['admin']):
                        if queryContains(['on']):
                            device('admin room', 'on')
                            whatsapp(f'turrnig on admin room lights and query = {body}')
                        elif queryContains(['off']):
                            device('admin room', 'off')

                            whatsapp('turning off admin room light')
                        else:
                            whatsapp('sorry, i don\'t know what to do in admin room')

                    elif queryContains(['green']):
                        if queryContains(['on']):
                            device('green room', 'on')
                            whatsapp('turrnig on green room lights')
                        elif queryContains(['off']):
                            device('green room', 'off')
                            whatsapp('turning off green room light')
                        else:
                            whatsapp('sorry, i don\'t know what to do in green room')

                    elif queryContains(['garage']):
                        if queryContains(['on']):
                            device('garage', 'on')
                            whatsapp('turrnig on garage lights')
                        elif queryContains(['off']):
                            device('garage', 'off')
                            whatsapp('turning off garage light')
                        else:
                            whatsapp('sorry, i don\'t know what to do in garage')
        else:
            a = requests.post("http://onwordsapi.com/", json={"command": body, "name": name, "gender": "str"}).json()
            whatsapp(a["reply"])
            # whatsapp('sorry, I don't recognise device')


    else:
        if "datatolinksmarthome" in body:
            try:
                json_object = json.loads(body)

                uid= json_object['datatolinksmarthome']
                whatsapp(uid)
            except ValueError:
                whatsapp("error code 12, please report the bug to my admin")

        else:

            if checkOfficeServerStatus():
                a = requests.post("http://office.onwordsapi.com/whatsapp",
                                  json={"command": body, "name": name, "gender": "str","from":"whatsapp"}).json()
                whatsapp(a["reply"])
            else:
                a = requests.post("http://onyx.onwordsapi.com/",
                                  json={"command": body, "name": name, "gender": "str"}).json()
                whatsapp(a["reply"])


@app.post("/webhook")
async def webhook(request: Request):
    # Handle the webhook request
    data = await request.form()
    message_body = data.get("Body")
    message_from = data.get("From")
    global body, from_
    body = message_body.lower()
    from_ = message_from.lower()
    # message_sid = request.form.get("MessageSid")
    # message_body = request.form.get("Body")
    reply(message_body.lower(), message_from)


@app.post("/webhook2")
async def webhook2(request: Request):
    # Handle the webhook request
    data = await request.form()
    message_body = data.get("Body")
    message_from = data.get("From")
    global body, from_
    body = message_body.lower()
    from_ = message_from.lower()
    # message_sid = request.form.get("MessageSid")
    # message_body = request.form.get("Body")
    #reply(message_body.lower(), message_from)
    if message_body == "hoi":
        whatsapp("Hai Welcome to Twilio API", "whatsapp:+917708630275")
    else:
        whatsapp("message from", "whatsapp:+917708630275")