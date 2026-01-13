from netra import Netra
import os
from dotenv import load_dotenv
import uuid
import git

load_dotenv()

NETRA_API_KEY = os.getenv("NETRA_API_KEY")
NETRA_ENDPOINT = os.getenv("NETRA_OTLP_ENDPOINT")

if not NETRA_API_KEY or not NETRA_ENDPOINT:
    raise ValueError("NETRA_API_KEY and NETRA_OTLP_ENDPOINT environment variables must be set.")

HEADERS = f"x-api-key={NETRA_API_KEY}"
def initialize_netra():
    print("Initializing Netra observability...")
    Netra.init(
        app_name="kv-github-agent",
        headers=HEADERS,
        trace_content=True,
        disable_batch=True
    )
    Netra.set_tenant_id("kv-interns")

def initialize_netra_session():
    print("Initializing Netra session...")
    Netra.set_session_id(uuid.uuid4().hex)
    Netra.set_user_id(git.get_author_info()["name"])