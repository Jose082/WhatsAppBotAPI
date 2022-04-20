import base64
import io
import matplotlib.pyplot as plt
from matplotlib.image import imread
from fastapi import FastAPI, Form, Response, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from time import sleep

# from twilio.rest import Client
# from twilio.twiml.messaging_response import Message, MessagingResponse
# from twilio.request_validator import RequestValidator

# from app.bot import GPTBot
# from app.configuration import ACCOUNT_SID, AUTH_TOKEN
from app.image import ImageRequest, ImageResponse, ImageModel

app = FastAPI()
# client = Client(ACCOUNT_SID, AUTH_TOKEN)
# bot = GPTBot()
image_model = ImageModel()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# @app.post("/text/reply")
# async def reply_chat(request: Request, WaId: str = Form(...), ProfileName: str = Form(...), Body: str = Form(...)):
#     response = MessagingResponse()
#     validator = RequestValidator(AUTH_TOKEN)
#     form_request = await request.form()
#     if not validator.validate(
#         str(request.url),
#         form_request,
#         request.headers.get("X-Twilio-Signature", "")
#     ):
#         raise HTTPException(status_code=400, detail="Error in Twilio Signature")
#
#     # Process user message
#     bot_response = bot.reply(unique_id=WaId, user_name=ProfileName, message=Body)
#
#     # Create twilio body message
#     message = Message()
#     message.body(bot_response)
#
#     response.append(message)
#     return Response(content=str(response), media_type="application/xml")


@app.post("/image/reply")
async def reply_chat(request: ImageRequest) -> ImageResponse:
    encoded_image = base64.b64decode(request.image)
    image = imread(io.BytesIO(encoded_image))
    response = image_model.classify_image(image)
    return response
