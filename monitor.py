import os
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def check_endpoint(endpoint, params, api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    apology_message = "Apologies, I am unable to answer this question right now. Something unexpected happened, try asking again!"
    success = False
    error_message = ""

    for _ in range(3):
        try:
            res = requests.get(endpoint, json=params, headers=headers)

            if res.text.strip().endswith(apology_message):
                error_message = "Server Error"
                continue

            if res.status_code != 200:
                error_message = f"JSON STATUS CODE: {res.status_code}"
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
    endpoints = {
        "Dev v7": "https://dev.bg-app-insights.com/v7",
        "UAT v7": "https://uat.bg-app-insights.com/v7",
        "Prod v7": "https://prod.bg-app-insights.com/v7",
        "Dev v8": "https://dev.bg-app-insights.com/v8",
        "UAT v8": "https://uat.bg-app-insights.com/v8",
        "Prod v8": "https://prod.bg-app-insights.com/v8"
    }

    api_keys = {
        "Dev v7": "abcdefgh",
        "UAT v7": "t31VJnwkQ4GEC75D0j2YBxeEO",
        "Prod v7": "IX6DUsnStDyre41lbTzQwViv8",
        "Dev v8": "abcdefgh",
        "UAT v8": "t31VJnwkQ4GEC75D0j2YBxeEO",
        "Prod v8": "IX6DUsnStDyre41lbTzQwViv8"
    }

    params = {
        "list_messages": [{"role": "user", "content": "What is zanu?"}],
        "date_filter": [{"start": "2020-01-01", "end": "2025-12-31"}],
        "allowed_data_sources": [],
        "persona": "coba",
        "therapeutic_area": "",
        "username": "beghou",
        "country": []
    }
    # api_key = "abcdefgh"

    for env_name, endpoint in endpoints.items():
        api_key = api_keys[env_name]
        status, error = check_endpoint(endpoint, params, api_key)

        if status == "fail":
            print(f"[{env_name}] Check failed: {error}")
            send_email(
                subject=f"🚨 API Monitor Alert - {env_name} (DOWN)",
                body=f"The {env_name} API check failed.\n\nError: {error}"
            )
        else:
            print(f"[{env_name}] Check passed.")
