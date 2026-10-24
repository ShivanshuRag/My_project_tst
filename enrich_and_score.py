import csv
import logging
import os
import time
import requests

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# API Configuration
API_KEY = os.getenv("ENRICHMENT_API_KEY", "c865ebb5789d41dc93629d5e5d3e82b3")
API_ENDPOINT = "https://emailreputation.abstractapi.com/v1/"  # Replace with actual enrichment provider

INPUT_FILE = "given_data.csv"
OUTPUT_FILE = "leads_enriched_scored.csv"


def query_enrichment_api(email: str, domain: str) -> dict:
    """Enrichment API call with error handling."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    params = {"email": email, "domain": domain}

    try:
        response = requests.get(
            API_ENDPOINT, headers=headers, params=params, timeout=10
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            logging.warning(f"No enrichment data found for: {email}")
            return {}
        elif response.status_code == 429:
            logging.warning("Rate limit hit! Sleeping for 5 seconds...")
            time.sleep(5)
            return {}
        else:
            logging.error(f"API Error {response.status_code} for {email}")
            return {}
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error querying API for {email}: {e}")
        return {}


def calculate_lead_score(enriched_data: dict) -> int:
    """Calculates lead score based on target ICP criteria (Max: 100)."""
    score = 0

    title = enriched_data.get("title", "").lower()
    employees = enriched_data.get("company_headcount", 0)
    industry = enriched_data.get("industry", "").lower()

    # Criteria 1: Decision-maker Seniority (Max: 40)
    if any(
        role in title
        for role in ["founder", "cxo", "ceo", "cto", "vp", "head of"]
    ):
        score += 40
    elif any(role in title for role in ["director", "lead", "manager"]):
        score += 25
    elif "engineer" in title or "developer" in title:
        score += 10

    # Criteria 2: Company Size Fit (Max: 35)
    if 50 <= employees <= 500:
        score += 35  # Sweet spot / Mid-market ICP
    elif 10 <= employees < 50:
        score += 20
    elif employees > 500:
        score += 25  # Enterprise

    # Criteria 3: Industry Fit (Max: 25)
    target_industries = ["saas", "software", "fintech", "information technology"]
    if any(ind in industry for ind in target_industries):
        score += 25

    return score


def process_leads(input_path: str, output_path: str):
    """Ingests, enriches, scores, and exports leads."""
    if not os.path.exists(input_path):
        logging.error(f"File not found: {input_path}")
        return

    processed_leads = []

    with open(input_path, mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            email = row.get("email", "").strip()
            domain = row.get("company_domain", "").strip()
            logging.info(f"Processing lead: {email}")

            # 1. Fetch Enrichment Data
            enrichment = query_enrichment_api(email, domain)

            # Extract fields with safe fallbacks
            job_title = enrichment.get("title", "N/A")
            company_name = enrichment.get("company_name", "N/A")
            headcount = enrichment.get("company_headcount", 0)
            industry = enrichment.get("industry", "N/A")
            linkedin_url = enrichment.get("linkedin_url", "N/A")

            # 2. Score Lead
            lead_score = calculate_lead_score(enrichment)

            # Determine Tier
            if lead_score >= 70:
                tier = "Tier 1 - High Priority"
            elif lead_score >= 40:
                tier = "Tier 2 - Medium Priority"
            else:
                tier = "Tier 3 - Low Priority"

            # 3. Compile Clean Record
            processed_leads.append(
                {
                    "first_name": row.get("first_name", ""),
                    "last_name": row.get("last_name", ""),
                    "email": email,
                    "company_domain": domain,
                    "company_name": company_name,
                    "job_title": job_title,
                    "headcount": headcount,
                    "industry": industry,
                    "linkedin_url": linkedin_url,
                    "lead_score": lead_score,
                    "priority_tier": tier,
                }
            )

            # Politeness delay to avoid rate limiting
            time.sleep(0.2)

    # 4. Save to Clean Output CSV
    if processed_leads:
        fieldnames = list(processed_leads[0].keys())
        with open(output_path, mode="w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed_leads)

        logging.info(f"Successfully processed and saved to {output_path}")


if __name__ == "__main__":
    process_leads(INPUT_FILE, OUTPUT_FILE)