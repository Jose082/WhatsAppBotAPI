FROM python:3.9

ENV API_RETURN ${API_RETURN}
ENV ACCOUNT_SID ${ACCOUNT_SID}
ENV AUTH_TOKEN ${AUTH_TOKEN}
ENV TWILIO_PHONE_NUMBER ${TWILIO_PHONE_NUMBER}
ENV OPENAI_API_KEY ${OPENAI_API_KEY}

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
