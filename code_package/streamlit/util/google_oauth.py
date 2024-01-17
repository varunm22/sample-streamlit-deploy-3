import streamlit as st
import os
from streamlit_oauth import OAuth2Component
import base64
import json
from code_package.util.cloud import get_aws_parameter

AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
REVOKE_ENDPOINT = "https://oauth2.googleapis.com/revoke"
REQUIRE_OAUTH_IN_LOCAL = False


def oauth():
    if os.environ.get("LOCAL_STREAMLIT") and not REQUIRE_OAUTH_IN_LOCAL:
        return

    if "auth" in st.session_state:
        if st.button("Logout"):
            del st.session_state["auth"]
            del st.session_state["token"]
            st.rerun()
    else:
        oauth = json.loads(get_aws_parameter("/streamlit/oauth"))["web"]

        if os.environ.get("LOCAL_STREAMLIT"):
            redirect = "http://localhost:8501"
        else:
            redirect = oauth["redirect_uris"][-1]

        # create a button to start the OAuth2 flow
        oauth2 = OAuth2Component(
            oauth["client_id"],
            oauth["client_secret"],
            AUTHORIZE_ENDPOINT,
            TOKEN_ENDPOINT,
            TOKEN_ENDPOINT,
            REVOKE_ENDPOINT,
        )

        result = oauth2.authorize_button(
            name="Continue with Google",
            icon="https://www.google.com.tw/favicon.ico",
            redirect_uri=redirect,
            scope="openid email profile",
            key="google",
            extras_params={"prompt": "consent", "access_type": "offline"},
            use_container_width=True,
        )

        if result:
            # decode the id_token jwt and get the user's email address
            id_token = result["token"]["id_token"]
            # verify the signature is an optional step for security
            payload = id_token.split(".")[1]
            # add padding to the payload if needed
            payload += "=" * (-len(payload) % 4)
            payload = json.loads(base64.b64decode(payload))
            email = payload["email"]
            st.session_state["auth"] = email
            st.session_state["token"] = result["token"]
            st.rerun()
        else:
            st.stop()
