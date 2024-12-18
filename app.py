from flask import Flask, jsonify
import subprocess
import os
import logging

app = Flask(__name__)

# Set up logging (to log version at startup)
logging.basicConfig(level=logging.INFO)


# Function to fetch the latest Git tag or fallback to commit hash
def get_git_version():
    try:
        # Attempt to get the latest Git tag
        version = (
            subprocess.check_output(["git", "describe", "--tags", "--always"])
            .strip()
            .decode()
        )
    except subprocess.CalledProcessError:
        version = "unknown"
    return version


# Automatically fetch version from Git tags
VERSION = get_git_version()

# Log version at app startup
logging.info(f"App started with version: {VERSION}")


@app.route("/version", methods=["GET"])
def get_version():
    """Endpoint to return the version of the app."""
    return jsonify({"version": VERSION})


@app.after_request
def add_version_to_response(response):
    """Add version to the response headers."""
    response.headers["X-App-Version"] = VERSION
    return response


if __name__ == "__main__":
    # Use environment variable for production setup
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
