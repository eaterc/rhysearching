import os
import requests

def main():
    endpoint = os.environ["NEWSLETTER_ENDPOINT"]

    response = requests.post(
        endpoint,
        headers={"Content-Type": "application/json"},
        json={}
    )

    print("Status:", response.status_code)
    print("Response:", response.text)

    response.raise_for_status()

if __name__ == "__main__":
    main()