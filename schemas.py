from typing import List

from pydantic.main import BaseModel


class Customer(BaseModel):
    phone: str
    email: str
    language: str


class SMSNotification(BaseModel):
    phone: str
    text_en: str
    text_ar: str


class EmailRequestBody(BaseModel):
    customers: List[Customer]
    subject_en: str
    subject_ar: str
    body_en: str
    body_ar: str

    class Config:
        schema_extra = {
            "example": {
                "customers": [
                    {"phone": "12121212", "email": "customer1@somedomain.com", "language": "en"},
                    {"phone": "12121212343", "email": "customer2@somedomain.com", "language": "ar"}
                ],
                "subject_en": "Weekly Newsletter",
                "subject_ar": "النشرة الأسبوعية",
                "body_en": "Dear sir, it is good to see you",
                "body_ar": "سيدي العزيز ، من الجيد رؤيتك"
            }
        }


class SMSRequestBody(BaseModel):
    customers: List[Customer]
    text_en: str
    text_ar: str

    class Config:
        schema_extra = {
            "example": {
                "customers": [
                    {"phone": "12121212", "email": "customer1@somedomain.com", "language": "en"},
                    {"phone": "12121212343", "email": "customer2@somedomain.com", "language": "ar"}
                ],
                "text_en": "Hello world",
                "text_ar": "مرحبا بالعالم"
            }
        }
