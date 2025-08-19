import os
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def check_endpoint(endpoint, params, api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    apology_message = "Apologies, I am unable to answer this question right now. Something unexpected happened, try asking again!"
    success = False
    error_message = ""

    for i in range(3):
        try:
            res = requests.get(endpoint, json=params, headers=headers)

            if res.status_code != 200:
                error_message = f"JSON STATUS CODE: {res.status_code}"
                continue

            if res.text.strip() == apology_message:
                error_message = "Server Error"
                continue

            success = True
            error_message = ""
            break

        except Exception as e:
            error_message = f"Exception: {str(e)}"
            continue

    return "pass" if success else "fail", error_message

def send_email(subject, body):
    message = Mail(
        from_email=os.environ.get("ALERT_FROM_EMAIL"),
        to_emails=os.environ.get("ALERT_TO_EMAIL"),
        subject=subject,
        plain_text_content=body
    )
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        sg.send(message)
    except Exception as e:
        print(f"Email send failed: {e}")


if __name__ == "__main__":
    endpoint = "https://dev.bg-app-insights.com/v10"
    params = {"list_messages": [{"role": "user", "content": "What is zanu?"}],
            "date_filter":[{"start": "2020-01-01","end":"2025-12-31"}],
            "allowed_data_sources":[],
            "persona":"coba",
            "therapeutic_area":"",
            "username": "beghou",
            "country": []
            }
    api_key = "abcdefgh"

    status, error = check_endpoint(endpoint, params, api_key)

    if status == "fail":
        print(f"Check failed: {error}")
        send_email(
            subject="🚨 API Monitor Alert (FAILED)",
            body=f"The API check failed.\nError: {error}"
        )
    else:
        print("Check passed.")


