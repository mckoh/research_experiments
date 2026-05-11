# %%
from requests import post, get
from datetime import datetime
from os import getenv
from os.path import basename


NOTION_TOKEN = getenv("NOTION_TOKEN")
DATABASE_ID = getenv("DATABASE_ID")

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_notion_entry(title, description, date=datetime.now().isoformat()):
    create_url = "https://api.notion.com/v1/pages"

    data = {
        "URL": {"title": [{"text": {"content": title}}]},
        "Description": {"rich_text": [{"text": {"content": description}}]},
        "Last modified": {"date": {"start": date}}
    }

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": data
    }

    response = post(create_url, headers=headers, json=payload)
    return response.status_code


if __name__ == "__main__":

    new_files = getenv("NEW_FILES", "").split()

    print(new_files)

    for file_path in new_files:
        if file_path.startswith("notebooks/") and file_path.endswith(".ipynb"):
            filename = basename(file_path)
            status = create_notion_entry(filename, file_path)
            print(f"Datei {filename} verarbeitet. Status: {status}")
# %%
