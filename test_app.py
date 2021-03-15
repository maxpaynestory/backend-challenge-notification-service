from unittest.mock import patch

from fastapi.testclient import TestClient

from app import api

client = TestClient(api)


def test_send_email_to_customer():
    response = client.post("/email")
    assert response.status_code == 422
    response = client.post(url="/email", json={"some": "wrong"})
    assert response.status_code == 422
    subject_ar = "النشرة الأسبوعية"
    body_ar = "سيدي العزيز ، من الجيد رؤيتك"
    email_input = {
        "customers": [
            {"phone": "12121212343", "email": "customer2@somedomain.com", "language": "ar"}
        ],
        "subject_en": "Weekly Newsletter",
        "subject_ar": subject_ar,
        "body_en": "Dear sir, it is good to see you",
        "body_ar": body_ar
    }
    with patch('app.send_email.apply_async') as function1_mock:
        response = client.post(url="/email", json=email_input)
        assert response.status_code == 200
        assert function1_mock.call_count == 1
        function1_mock.assert_called_with(('customer2@somedomain.com', subject_ar, body_ar))
        email_input["customers"][0]["language"] = "en"
        client.post(url="/email", json=email_input)
        function1_mock.assert_called_with(
            ('customer2@somedomain.com', "Weekly Newsletter", "Dear sir, it is good to see you"))
        email_input["customers"].append({"phone": "12121212343", "email": "customer2@somedomain.com", "language": "ar"})
        email_input["customers"].append({"phone": "12121212343", "email": "customer2@somedomain.com", "language": "fr"})
        client.post(url="/email", json=email_input)
        assert function1_mock.call_count == 5
        function1_mock.assert_called_with(('customer2@somedomain.com', "Weekly Newsletter", "Dear sir, it is good to see you"))


def test_send_sms_to_customer():
    response = client.post("/sms")
    assert response.status_code == 422
    response = client.post(url="/sms", json={"some": "wrong"})
    assert response.status_code == 422
    arabic_text = "مرحبا بالعالم""سيدي العزيز ، من الجيد رؤيتك"
    sms_input = {
        "customers": [
            {"phone": "12121212343", "email": "customer2@somedomain.com", "language": "ar"}
        ],
        "text_en": "Hello world",
        "text_ar": arabic_text
    }
    with patch('app.send_sms.apply_async') as function1_mock:
        response = client.post(url="/sms", json=sms_input)
        assert response.status_code == 200
        assert function1_mock.call_count == 1
        function1_mock.assert_called_with(('12121212343', arabic_text))
        sms_input["customers"][0]["language"] = "en"
        client.post(url="/sms", json=sms_input)
        function1_mock.assert_called_with(('12121212343', "Hello world"))
        sms_input["customers"].append({"phone": "12121212343", "email": "customer2@somedomain.com", "language": "ar"})
        client.post(url="/sms", json=sms_input)
        assert function1_mock.call_count == 4

        # default language is english
        sms_input["customers"] = [{"phone": "12121212343", "email": "customer2@somedomain.com", "language": "fr"}]
        client.post(url="/sms", json=sms_input)
        function1_mock.assert_called_with(('12121212343', "Hello world"))
