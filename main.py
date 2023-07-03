from datetime import datetime, timedelta
from fastapi import BackgroundTasks, FastAPI, Request
import requests, keys, pyrebase, uvicorn,time,json
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from threading import Timer

app = FastAPI()

sessions = {}
authlist={}
account_sid = keys.account_sid
auth_token = keys.auth_token
client = Client(account_sid, auth_token)

databse = pyrebase.initialize_app(keys.config)
db = databse.database()


def send_message(reply,to,_from="whatsapp:+917708630275"):
    try:
        # client.messages.create(
        #                     content_sid=reply,
        #                     from_=_from,
        #                     content_variables=json.dumps({
        #                         '1': 'Name'
        #                       }),
        #                       to=to
        #                   )
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


def reply(body, _from):
    try:
        userData = db.child(_from).get().val()
        if userData == None:

            user = False
        elif userData['name'] == False:
            send_message('May I rembember your name as {}\nreply with "yes" to save your name\n"no" to reenter'.format(body.capitalize()))
            db.child(_from).update({'name': body,'pending':'yes or no'})
        elif userData['pending'] =='yes or no':
            if body == "yes":
                send_message('saving your name as {}'.format(userData['name'].capitalize()))
                db.child(_from).update({'name': userData['name'],'pending':'none'})

            elif body == "no":
                send_message('ok, Please enter your name again')
                db.child(_from).update({'name': False})
            else:
                send_message('Please reply with yes or no')
        else:
            user  =True
    except:
       send_message('Can\'t handle the current laod. surver is too busy.\nError code is 12')


    if user:
        name = userData['name'].capitalize()
    else:
        send_message('Hey,\nBefore answering that may I know what shall I call you?\nEnter your name:')
        db.child(_from).update({'name': False,'firstAskedQuestion':body})
        return
    
@app.post("/webhook")
async def webhook(request: Request):
    alreadySent = False
    # Handle the webhook request
    data = await request.form()
    message_body = data.get("Body")
    message_from = data.get("From")
    body = message_body.lower()
    from_ = message_from.lower()
    ProfileName = data.get("ProfileName")
    if message_from in sessions:
        timer = sessions[message_from]
        timer.cancel()
    
    if body == "hai" or body == "hi":
        send_message(f"Hi {ProfileName}! Welcome to ONWORDS. I am ONYX , The Personalised assistant for ONWORDS. Let me know something about you,can you lend me a click.", from_)
        # send_message(f"Hi {ProfileName}! Welcome to *ONWORDS*. I Am *ONYX*.",from_)
        if message_from not in authlist:
            authlist[message_from] = message_from
        alreadySent = True

    if message_from in authlist:
        if not body == "hai" or not body== "hi":
            if body == "t":
                send_message("yes its working",from_)
            elif body =="existing customer":
                send_message("Its great to hear.Please let me know that how can i help you",from_)
                
            elif body =="new customer":
                send_message("Let me introduce our services to you, can you lend me a click",from_)
                
            elif body =="career":
                send_message("When it cover to your career, we onwords are the first to identify talents and you are the one",from_)

            elif body =="share your resume":
                send_message("Share your resume to careers@onwords.in",from_)

            # New Customer  ====================================

            # OPEN SMART HOME SOLUTION =============

            elif body =="smart home solution":
                send_message("We have a set of smart solutions to make your home smart",from_)

            # elif body =="automations":
            #     send_message("Click your Automation service", from_)
                
            elif body =="home automation" or body =="gate automation":
                send_message("Contact us...", from_)
                send_message(["https://sandstorm-chicken-1462.twil.io/assets/Onwords-GateAutomations.pdf"],from_)    

            elif body =="more":
                send_message("click what type of service you want", from_)

            elif body =="security systems" or body =="products" or body =="others":
                send_message("Contact us...", from_) 
                send_message(["https://sandstorm-chicken-1462.twil.io/assets/Onwords-SecuritySystems.pdf"],from_)        

            # OPEN IT SOLUTION
                
            elif body =="it solution":
                send_message("You have several options and here we go...",from_)

            # Application ============    

            elif body =="application":
                send_message("Yes You guessed it right we can build both",from_)

            elif body == "android" or body == "ios":
                send_message("Take a look at our work and contact us", from_)
                send_message("Contact us...", from_) 
                  
            # Website ===============
            elif body == "website":
                send_message("Contact us...", from_)
        
            # Digital marketing ================  

            elif body == "digital marketting":
                send_message("Promote your brand and get in touch with the Digital World", from_)    

            elif body =="More....":
                send_message("Lend me click for  what services you want",from_)

            elif body =="poster design" or body == "logo design":
                send_message("Contact us...",from_)        

            elif body == "seo services" or body == "other services":   
                send_message("Contact us...", from_)

            # Close NEW CUSTOMER ===================

            # Existing CUSTOMER ====================

            # in need new serice ==================
            elif body =="in need new service":
                send_message("Let me introduce our services to you, can you lend me a click",from_)

            elif body =="existing service":
                send_message("Our Executives are ready to assist you 24/7 let us know whats on your need..!",from_)

            #IT SERVICE ======================================

            elif body =="it service":
                send_message("Well you feel into the right mark and choose your service",from_)

            elif body == "website service" or body == "app service":
                send_message("Contact us...", from_)

            elif body =="digital marketings":
                send_message("Click the service you want",from_)

            elif body =="more...":
                send_message("Lend me click to service you want",from_)

            elif body =="seo" or body =="other service":
                send_message("Contact us...", from_)

            elif body =="posterdesign service" or body =="logodesign service":
                send_message("Contact us...", from_)            

            # SAMRT HOME SERVICE =================================

            elif body =="smart home service":
                send_message("As You know we provide a lot of services let me know  which one it is..!",from_)

            elif body == "home automations" or body == "gate automations":
                send_message("Contact us...", from_)

            elif body=="more..":
                send_message("As You know we provide a lot of services let me know  which one it is..!!", from_)
                
            elif body == "security system" or body == "product service" or body =="other service":
                send_message("Contact us...", from_)

            elif body == "abcd":
                send_message("HX4cfb92724a0680468803090f6cc76295", from_)   

            # Close Existing CUSTOMER ====================
            elif not alreadySent:
                send_message(f"Oops invalid format,Please type *'Hai'* to go to the welcome message", from_)     
        

    def session_timeout(message_from):
        try:
            del authlist[message_from]
            send_message(f"Your *session* has *timeout* due to inactive on the chennal. Please type *'Hai'* to go to the welcome message", from_)
        except:
            send_message(f"Oops invalid format,Please type *'Hai'* to go to the welcome message", from_)
    timer = Timer(900, session_timeout,[message_from])
    timer.start()
    sessions[message_from] = timer

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=1111, reload=True)