from datetime import datetime, timedelta
from fastapi import BackgroundTasks, FastAPI, Request
import requests, keys, pyrebase, uvicorn, time, json
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from threading import Timer
import asyncio

app = FastAPI()

sessions = {}
authlist = {}
account_sid = keys.account_sid
auth_token = keys.auth_token
client = Client(account_sid, auth_token)


# databse = pyrebase.initialize_app(keys.config)
# db = databse.database()

# async def send_whatsapp_message(to, body, media_url=None):
#     try:
#         upload_task = asyncio.create_task(upload_file(to, media_url))

#         message_task = asyncio.create_task(send_message(to, body))

#         await asyncio.gather(upload_task, message_task)
#     except Exception as e:
#         print("the error is",e)

# async def upload_file(to, media_url, _from="whatsapp:+917708630275"):
#     # Logic to upload the PDF file
#     client.messages.create(
#             body="",
#             media_url=media_url,
#             to=to,
#             from_=_from
#         )

# async def send_message(to, body, _from="whatsapp:+917708630275"):
#     # Logic to send the message
#     client.messages.create(
#             body=body,
#             to=to,
#             from_=_from
#         )


def send_message(reply, to, _from="whatsapp:+917708630275"):
    try:
        client.messages.create(
            body="",
            media_url=reply,
            to=to,
            from_=_from
        )
    except Exception as e:
        client.messages.create(
            body=reply,
            to=to,
            from_=_from
        )


# def reply(body, _from):
#     try:
#         userData = db.child(_from).get().val()
#         if userData == None:
#
#             user = False
#         elif userData['name'] == False:
#             send_message('May I rembember your name as {}\nreply with "yes" to save your name\n"no" to reenter'.format(body.capitalize()))
#             db.child(_from).update({'name': body,'pending':'yes or no'})
#         elif userData['pending'] =='yes or no':
#             if body == "yes":
#                 send_message('saving your name as {}'.format(userData['name'].capitalize()))
#                 db.child(_from).update({'name': userData['name'],'pending':'none'})
#
#             elif body == "no":
#                 send_message('ok, Please enter your name again')
#                 db.child(_from).update({'name': False})
#             else:
#                 send_message('Please reply with yes or no')
#         else:
#             user  =True
#     except:
#        send_message('Can\'t handle the current laod. surver is too busy.\nError code is 12')
#
#
#     if user:
#         name = userData['name'].capitalize()
#     else:
#         send_message('Hey,\nBefore answering that may I know what shall I call you?\nEnter your name:')
#         db.child(_from).update({'name': False,'firstAskedQuestion':body})
#         return

@app.post("/")
async def webhook(request: Request):
    # Handle the webhook request
    data = await request.form()
    message_body = data.get("Body")
    message_from = data.get("From")
    body = message_body.lower()
    from_ = message_from.lower()
    ProfileName = data.get("ProfileName")
    print(body)
    if message_from in sessions:
        timer = sessions[message_from]
        timer.cancel()

    if body == "hi":
        send_message(
           "Hi There! Welcome to ONWORDS. I am Onyx, your virtual assistant to provide information about our products and services. Would you be interested with our Products or Services?",
            from_)


    elif body == "services":
        send_message("Below listed are some of the services that we are currently offering. Please select the service you are interested in.",from_)

    elif body == "Security Systems":
        send_message("will send ss data",from_)

    elif body == "smart home":
        send_message("hear will be the link of smart home videos",from_)
        send_message("this is broucher",from_)
        send_message("Just I have sent you the videos and catalog for smart home.",from_)
        send_message("Please select your option from the below to proceed further.",from_)

    elif body == "swing type" or body == "sliding type" or body == "folding type":
        send_message("hear will be the link of gate automation videos.",from_)
        send_message("Just I have sent you the videos and catalog for gate automation.",from_)
        send_message("Please select your option from the below to proceed further.",from_)

    elif body == "security systems":
        send_message("hear will be the link of security system videos.", from_)
        send_message("Just I have sent you the videos and catalog for security system.", from_)
        send_message("Please select your option from the below to proceed further.", from_)

    elif body == "request a demo!":
        print("sending request demo reply")
        send_message("website link",from_)
        # send_message("Your convenient place of demo: " ,from_)
    elif body == "contact our pr":
        send_message("Contact Our PR Team",from_)
    elif body == "demo at your place":
        send_message("Your convenient date for demo, user will be sending date and time and location need it to be stored separatly",from_)

    elif body == "demo at our office":
        send_message("Your convenient date for demo, user will be sending date and time and location need it to be stored separatly",from_)
    elif body == "gate automation":
        send_message("Please select your gate type:",from_)

    elif body == "code 11":
        send_message("From Nikhil's Macbook and showing demo for gip  bro", from_)

    elif body == "code 12":
        send_message(" fwrbfiuwanrifuv wajrnfipuawhn", from_)

    elif body == "existing customer":
        send_message("Its great to hear.Please let me know that how can i help you", from_)

    elif body == "new customer":
        send_message("Let you introduce our services to you, can you lend me a click", from_)

    elif body == "career":
        send_message("When it cover to your career, we onwords are the first to identify talents and you are the one",
                     from_)

    elif body == "share your resume":
        send_message("Share your resume to careers@onwords.in", from_)

    # New Customer  ====================================

    # OPEN SMART HOME SOLUTION =============

    elif body == "iot solution":
        send_message("We have a set of smart solutions to make your home smart!", from_)

    # elif body =="automations":
    #     send_message("Click your Automation service", from_)

    # elif body == "smart home":
    #     send_message(["https://sandstorm-chicken-1462.twil.io/assets/Onwords-Smarthome.pdf"], from_)
    #     send_message("Contact Our PR Team", from_)

    elif body == "gate automation":
        send_message(["https://sandstorm-chicken-1462.twil.io/assets/Onwords-GateAutomations.pdf"], from_)
        send_message("Contact Our PR Team", from_)

    elif body == "more":
        send_message("click what type of service you want", from_)

    # elif body == "security systems":
    #     send_message(["https://sandstorm-chicken-1462.twil.io/assets/Onwords-Ajax_Product.pdf"], from_)
    #     send_message("Contact Our PR Team", from_)
        # await send_whatsapp_message(to=from_, body="Contact Our PR Team", media_url=["https://sandstorm-chicken-1462.twil.io/assets/Onwords-Ajax_Product.pdf"])

    elif body == "products":
        send_message(["https://sandstorm-chicken-1462.twil.io/assets/Onwords-SecuritySystems.pdf"], from_)
        send_message("Contact Our PR Team", from_)
        # await send_whatsapp_message(to=from_, body="Contact Our PR Team", media_url=["https://sandstorm-chicken-1462.twil.io/assets/Onwords-SecuritySystems.pdf"])
    elif body == "others":
        send_message("Contact Our PR Team", from_)

    # OPEN IT SOLUTION

    elif body == "it solution":
        send_message("You have several options and here we go...", from_)

    # Application ============

    elif body == "application":
        send_message("Yes You guessed it right we can build both", from_)

    elif body == "android" or body == "ios":
        send_message("Take a look at our work and contact us", from_)
        send_message("Contact Our PR Team", from_)

    # Website ===============
    elif body == "website":
        send_message("Contact Our PR Team", from_)

    # Digital marketing ================

    elif body == "digital marketing":
        send_message("Promote your brand and get in touch with the Digital World", from_)

    elif body == "more....":
        send_message("Lend me click for  what services you want!", from_)

    elif body == "poster design" or body == "logo design":
        send_message("Contact Our PR Team", from_)

    elif body == "seo services" or body == "other services":
        send_message("Contact Our PR Team", from_)

    # Close NEW CUSTOMER ===================

    # Existing CUSTOMER ====================

    # in need new serice ==================
    elif body == "in need new service":
        send_message("Let me introduce our services to you, can you lend me a click", from_)

    elif body == "existing service":
        send_message("Our Executives are ready to assist you 24/7 let us know whats on your need..!", from_)

    # IT SERVICE ======================================

    elif body == "it service":
        send_message("Well you feel into the right mark and choose your service", from_)

    elif body == "website service":
        send_message("Contact Our Web Team", from_)

    elif body == "app service":
        send_message("Contact Our App Team", from_)

    elif body == "digital marketings":
        send_message("Click the service you want", from_)

    elif body == "more...":
        send_message("Lend me click to service you want", from_)

    elif body == "seo":
        send_message("Contact Our Digital Marketing Team", from_)

    elif body == "other service":
        send_message("Contact Our PR Team", from_)

    elif body == "posterdesign service" or body == "logodesign service":
        send_message("Contact Our Media Team", from_)

    # SAMRT HOME SERVICE =================================

    elif body == "iot service":
        send_message("As You know we provide a lot of services let me know  which one it is..!", from_)

    elif body == "home automations" or body == "gate automations":
        send_message("Contact Our RND Team", from_)

    elif body == "more..":
        send_message("As You know we provide a lot of services let me know  which one it is..!!", from_)

    elif body == "security system" or body == "product service" or body == "other service":
        send_message("Contact Our RND Team", from_)

    elif body == "abcd":
        send_message("HX4cfb92724a0680468803090f6cc76295", from_)

    # Close Existing CUSTOMER ====================
    else:
        send_message(f"Oops invalid format, Please type *'Hi'* to go to the welcome message", from_)

        # elif not alreadySent:
        #     send_message(f"Oops invalid format, Please type *'Hi'* to go to the welcome message", from_)

    def session_timeout(message_from):
        try:
            del authlist[message_from]
            send_message(
                "Your *session* has *timeout* due to inactive on the chennal. Please type *'Hi'* to go to the welcome message",
                from_)
        except:
            send_message("Oops invalid format, Please type *'Hi'* to go to the welcome message", from_)

    timer = Timer(900, session_timeout, [message_from])
    timer.start()
    sessions[message_from] = timer


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8182)
