import json
import os
import requests

# 1. API Configuration
API_KEY = os.getenv("APOLLO_API_KEY", "4zoetmhulW6pUhabUOfoRw")
URL = "https://api.apollo.io/api/v1/contacts/search"

# 2. Request Headers
headers = {
    "Cache-Control": "no-cache",
    "Content-Type": "application/json",
    "X-Api-Key": API_KEY,
}

# 3. Payload (Search parameters)
payload = {
    # "q_keywords": "software engineer",  # Contact name, job title ya keyword
    "page": 1,
    "per_page": 10,  # 10 contacts fetch karne ke liye
}


def search_contacts():
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=15)

        # Status code check
        if response.status_code == 403:
            print(
                "Error 403: Yeh endpoint aapke current Apollo plan me enabled nahi hai."
            )
            print("Response:", response.text)
            return

        response.raise_for_status()
        data = response.json()

        # Contacts list extract karein
        contacts = data.get("contacts", [])

        if not contacts:
            print("Koi contact match nahi hua.")
            return

        print(f"Total Found: {len(contacts)} contacts\n")

        for idx, person in enumerate(contacts, start=1):
            name = person.get("name", "N/A")
            title = person.get("title", "N/A")
            email = person.get("email", "N/A")
            organization = person.get("organization_name", "N/A")
            linkedin = person.get("linkedin_url", "N/A")

            print(f"{idx}. {name}")
            print(f"   - Role: {title}")
            print(f"   - Company: {organization}")
            print(f"   - Email: {email}")
            print(f"   - LinkedIn: {linkedin}")
            print("-" * 40)

        # JSON file me dump karein
        with open("contacts_data.json", "w", encoding="utf-8") as f:
            json.dump(contacts, f, indent=4)
        print("\nFull data 'contacts_data.json' me save ho gaya.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error: {http_err} - {response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    search_contacts()