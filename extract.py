# %%
from requests import post, get
from datetime import datetime
from os import getenv


NOTION_TOKEN = getenv("NOTION_TOKEN")
DATABASE_ID = getenv("DATABASE_ID")


headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_page(title, description, date=datetime.now().isoformat()):
    create_url = "https://api.notion.com/v1/pages"

    data = {
        "URL": {
            "title": [
                {"text": {"content": title}}
            ]
        },

        "Description": {
            "rich_text": [
                {"text": {"content": description}}
            ]
        },

        "Last modified": {
            "date": {"start": date}
        }
    }

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": data
    }

    response = post(create_url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Erfolg! Datensatz wurde erstellt.")
    else:
        print(f"Fehler: {response.status_code}")
        print(response.text)

# Beispiel-Daten für die Spalten deiner Datenbank
# Wichtig: Die Keys (z.B. "Name") müssen exakt so heißen wie deine Spalten in Notion

create_page("Test 2", "Description")

# %%
