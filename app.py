from fastapi import FastAPI, Form, Response, Request, HTTPException

from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.request_validator import RequestValidator

from bot import GPTBot
from configuration import ACCOUNT_SID, AUTH_TOKEN

from pyngrok import ngrok
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
client = Client(ACCOUNT_SID, AUTH_TOKEN)
bot = GPTBot()

public_url = ngrok.connect(5000).public_url
print(f'Ngrok public_url: {public_url}/reply')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post("/reply")
async def reply_chat(request: Request, WaId: str = Form(...), ProfileName: str = Form(...), Body: str = Form(...)):
    response = MessagingResponse()
    validator = RequestValidator(AUTH_TOKEN)
    form_request = await request.form()
    if not validator.validate(
        str(request.url),
        form_request,
        request.headers.get("X-Twilio-Signature", "")
    ):
        raise HTTPException(status_code=400, detail="Error in Twilio Signature")

    # Process user message
    bot_response = bot.reply(unique_id=WaId, user_name=ProfileName, message=Body)

    # Create twilio body message
    message = Message()
    message.body(bot_response)

    response.append(message)
    return Response(content=str(response), media_type="application/xml")
