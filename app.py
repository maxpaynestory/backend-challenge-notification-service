import redis
from fastapi import FastAPI
from schemas import SMSRequestBody, EmailRequestBody
from celery import Celery

PORT = 9080
HOST = "0.0.0.0"
REDIS_HOST = "redis"
REDIS_DB = 7

# The number of requests of providers (SMS, Email) can handle per minute are limited.
SMS_RATE = "2/m"
EMAIL_RATE = "3/m"

api = FastAPI()
celery_app = Celery("swvl_test", broker=f"redis://{REDIS_HOST}/{REDIS_DB}")


@celery_app.task(bind=True, rate_limit=SMS_RATE)
def send_sms(self, phone, text):
    print(f"Sending SMS to {phone}")


@celery_app.task(bind=True, rate_limit=EMAIL_RATE)
def send_email(self, email, subject, body):
    print(f"Sending Email to {email}")


@api.post("/sms")
async def send_sms_to_customer(body: SMSRequestBody):
    """This api will help to send arabic and english version of sms to one or more customer."""
    for customer in body.customers:
        if customer.language == "ar":
            send_sms.apply_async((customer.phone, body.text_ar))
        else:
            send_sms.apply_async((customer.phone, body.text_en))
    return {"sent": True}


@api.post("/email")
async def send_email_to_customer(body: EmailRequestBody):
    """This api will help to send arabic and english version of email to one or more customer."""
    for customer in body.customers:
        if customer.language == "ar":
            send_email.apply_async((customer.email, body.subject_ar, body.body_ar))
        else:
            send_email.apply_async((customer.email, body.subject_en, body.body_en))
    return {"sent": True}


if __name__ == '__main__':
    import uvicorn

    print(dir(api))
    uvicorn.run('app:api', host=HOST, port=PORT, log_level='info', reload=True)  # , uds='uvicorn.sock')
