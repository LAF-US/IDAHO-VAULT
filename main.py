import atexit
import logging
import os

from flask import Flask, request
from posthog import Posthog


def create_posthog_client():
    project_token = os.getenv("POSTHOG_PROJECT_TOKEN")
    if not project_token:
        if os.getenv("FLASK_DEBUG", "0").lower() in ("1", "true", "yes"):
            raise RuntimeError(
                "POSTHOG_PROJECT_TOKEN variable required by PostHog is missing or "
                "un-configured, this causes events to be silently missed. This error "
                "stops appearing once POSTHOG_PROJECT_TOKEN is configured"
            )
        logging.getLogger(__name__).warning(
            "PostHog is not configured; analytics events will not be captured."
        )
        return None

    return Posthog(
        project_token,
        host=os.getenv("POSTHOG_HOST"),
        enable_exception_autocapture=True,
    )


posthog_client = create_posthog_client()
if posthog_client:
    atexit.register(posthog_client.shutdown)


app = Flask(__name__)


@app.errorhandler(500)
def capture_internal_server_error(error):
    if posthog_client:
        posthog_client.capture_exception(
            getattr(error, "original_exception", error)
        )
    return "Internal Server Error", 500


@app.route('/', methods=['POST'])
def handler():
    """
    Placeholder for the Vault Sync Service.
    This endpoint will listen for GitHub webhooks.
    """
    print("Webhook received. The Nest Bridge is active.")
    if posthog_client:
        posthog_client.capture("webhook_received")
    # In the full implementation, this service would:
    # 1. Verify the GitHub webhook signature.
    # 2. Process the webhook payload.
    # 3. Interact with Secret Manager, Cloud Storage, and Pub/Sub as needed.
    return "OK", 200

if __name__ == "__main__":
    app.run(
        debug=os.environ.get("FLASK_DEBUG", "0").lower() in ("1", "true", "yes"),
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8080))
    )
