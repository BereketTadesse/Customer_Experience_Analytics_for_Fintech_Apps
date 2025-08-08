from google_play_scraper import reviews, Sort
import pandas as pd
from datetime import datetime

# Define official package IDs and display names
apps = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp"
}

# Master list to hold all reviews
all_reviews = []

# Scrape 500 reviews per app
for app_name, package_id in apps.items():
    print(f"🔍 Scraping reviews for {app_name}...")
    
    # Fetch reviews
    result, _ = reviews(
        package_id,
        lang='en',
        country='et',
        sort=Sort.NEWEST,
        count=1000  # Aim to collect 400+ usable reviews
    )

    # Parse and store
    for r in result:
        all_reviews.append({
            "App": app_name,
            "ReviewText": r.get("content", ""),
            "Rating": r.get("score", ""),
            "ReviewDate": r.get("at").strftime('%Y-%m-%d') if r.get("at") else "",
            "Source": "Google Play"
        })

# Create DataFrame
df = pd.DataFrame(all_reviews)

# Save as CSV
df.to_csv("mobile_bank_reviews.csv", index=False, encoding="utf-8-sig")
print("✅ Saved all reviews to 'mobile_bank_reviews.csv'")
