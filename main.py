import base64
import json
import os
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = "YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME"

def trigger_github_action(request):
    # Parse Pub/Sub message
    envelope = request.get_json()
    if not envelope:
        return "No Pub/Sub message received", 400
    if 'message' not in envelope:
        return "Invalid Pub/Sub message format", 400

    pubsub_message = envelope['message']
    data = pubsub_message.get('data')
    if data:
        message_json = json.loads(base64.b64decode(data).decode('utf-8'))
        # You can add filtering logic here, for example to parse repository or tag info

    # Call GitHub repository_dispatch API to trigger workflow
    url = f"https://api.github.com/repos/{GITHUB_REPO}/dispatches"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_TOKEN}"
    }
    payload = {
        "event_type": "artifact-image-push"
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 204:
        return "Workflow triggered", 200
    else:
        return f"GitHub API error: {response.text}", response.status_code
