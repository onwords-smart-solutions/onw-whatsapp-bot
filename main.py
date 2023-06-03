from fastapi import FastAPI, Request
import requests, keys, pyrebase, uvicorn
from twilio.rest import Client

app = FastAPI()

account_sid = keys.account_sid
auth_token = keys.auth_token
client = Client(account_sid, auth_token)

databse = pyrebase.initialize_app(keys.config)
db = databse.database()


def whatsapp(reply, _from="whatsapp:+18144812393"):
    global from_
    message = client.messages.create(
        body=reply,
        to=from_,
        from_=_from
    )    


global body, from_


def reply(body, _from):
    try:
        userData = db.child(_from).get().val()
        if userData == None:

            user = False
        elif userData['name'] == False:
            whatsapp('May I rembember your name as {}\nreply with "yes" to save your name\n"no" to reenter'.format(body.capitalize()))
            db.child(_from).update({'name': body,'pending':'yes or no'})
        elif userData['pending'] =='yes or no':
            if body == "yes":
                whatsapp('saving your name as {}'.format(userData['name'].capitalize()))
                db.child(_from).update({'name': userData['name'],'pending':'none'})

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


    if user:
        name = userData['name'].capitalize()
        print(name)
    else:
        whatsapp('Hey,\nBefore answering that may I know what shall I call you?\nEnter your name:')
        db.child(_from).update({'name': False,'firstAskedQuestion':body})
        return


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
    if body == "hoi":
        whatsapp("Hoi Welcome to Twilio API", "whatsapp:+917708630275 webhook1")
    elif message_body == "hello":
        whatsapp("Hello Welcome to onwords webhook1")
    elif message_body == "hell":
        whatsapp("Hell this is onwords webhook1")
    else:
        whatsapp("None of the aboveee webhook1")
    # reply(message_body.lower(), message_from)


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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8182, reload=True)