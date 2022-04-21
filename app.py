import io
import requests
import base64
from PIL import Image
from image import ImageModel

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
image_model = ImageModel()

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
async def reply_chat(request: Request):
    tw_response = MessagingResponse()
    validator = RequestValidator(AUTH_TOKEN)
    form_request = await request.form()
    if not validator.validate(
            str(request.url),
            form_request,
            request.headers.get("X-Twilio-Signature", "")
    ):
        raise HTTPException(status_code=400, detail="Error in Twilio Signature")
    if 'MediaUrl0' in form_request.keys():
        image_url = form_request['MediaUrl0']

        img_data = requests.get(image_url).content
        with open('image.jpg', 'wb') as handler:
            handler.write(img_data)

        image_file = open('image.jpg', 'rb')
        encoded_image = base64.b64encode(image_file.read())
        encoded_string = encoded_image.decode('utf-8')

        try:
            encoded_image = base64.b64decode(encoded_string)
            pil_image = Image.open(io.BytesIO(encoded_image)).convert('RGB')
            model_responses = image_model.classify_image(pil_image)
            response = ""
            for model_response in model_responses:
                probability = model_response['probability'] * 100
                response += f"Clase: {model_response['name'].title()} Probabilidad: {probability}% \n"
        except Exception as error:
            return HTTPException(status_code=400,
                                 detail=f"Error processing the image. Additional information {str(error)}")

    else:
        whatsapp_id = form_request['WaId']
        profile_name = form_request['ProfileName']
        body = form_request['Body']
        response = bot.reply(unique_id=whatsapp_id, user_name=profile_name, message=body)

    # Create twilio body message
    message = Message()
    message.body(response)

    tw_response.append(message)
    return Response(content=str(tw_response), media_type="application/xml")
