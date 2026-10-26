import time
import pandas as pd
import requests

# Configuration
CSV_FILE_PATH = "leads(1).csv"
API_KEY = "d13c969b-be7e-4192-8a03-0495bd0e58fb_ftaxdtf"
CAMPAIGN_ID = "4237452"  # Apna Smartlead Campaign ID yahan daalein
API_ENDPOINT = f"https://server.smartlead.ai/api/v1/campaigns/{CAMPAIGN_ID}/leads"

CHUNK_SIZE = 100
DELAY_BETWEEN_CHUNKS = 1


def upload_batch(batch_data, batch_number):
    """Ek single batch (100 leads) ko API par upload karta hai."""
    headers = {"Content-Type": "application/json"}
    params = {"api_key": API_KEY}
    payload = {"lead_list": batch_data}

    try:
        response = requests.post(
            API_ENDPOINT,
            params=params,
            json=payload,
            headers=headers,
            timeout=30,
        )

        if response.status_code in (200, 201):
            print(f"[SUCCESS] Batch {batch_number}: {len(batch_data)} leads uploaded.")
            return True
        else:
            print(f"[FAILED] Batch {batch_number}: Status {response.status_code} - {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Batch {batch_number} network error: {e}")
        return False


def format_leads_for_smartlead(chunk_df):
    """CSV rows ko Smartlead ke expected schema ke according format karta hai."""
    formatted_leads = []

    for _, row in chunk_df.iterrows():
        email = str(row.get("Email", "")).strip()

        # Agar email missing/invalid hai toh skip karein
        if not email or email.lower() == "nan":
            continue

        # Full Name ko first_name aur last_name me split karein
        raw_name = str(row.get("Name", "")).strip()
        first_name = ""
        last_name = ""
        if raw_name and raw_name.lower() != "nan":
            name_parts = raw_name.split(maxsplit=1)
            first_name = name_parts[0]
            if len(name_parts) > 1:
                last_name = name_parts[1]

        # Phone field check
        raw_phone = str(row.get("Phone", "")).strip()
        phone_number = raw_phone if raw_phone and raw_phone.lower() != "nan" else None

        lead_obj = {
            "email": email,
            "first_name": first_name or None,
            "last_name": last_name or None,
            "phone_number": phone_number,
            # Additional custom fields agar campaign template me use karne ho:
            "custom_fields": {
                "full_name": raw_name,
                "phone": phone_number
            }
        }

        # None values ko clean karein taaki payload clean rahe
        lead_obj = {k: v for k, v in lead_obj.items() if v is not None}
        formatted_leads.append(lead_obj)

    return formatted_leads


def process_and_upload_leads():
    """CSV ko chunks me read karke upload karta hai."""
    batch_counter = 1

    try:
        for chunk_df in pd.read_csv(CSV_FILE_PATH, chunksize=CHUNK_SIZE):
            batch_records = format_leads_for_smartlead(chunk_df)

            if not batch_records:
                print(f"[SKIP] Batch {batch_counter}: No valid leads in this chunk.")
                continue

            success = upload_batch(batch_records, batch_counter)
            if not success:
                print(f"[ALERT] Batch {batch_counter} needs review.")

            batch_counter += 1
            time.sleep(DELAY_BETWEEN_CHUNKS)

        print("\nAll batches have been processed.")

    except FileNotFoundError:
        print(f"File not found: {CSV_FILE_PATH}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    process_and_upload_leads()