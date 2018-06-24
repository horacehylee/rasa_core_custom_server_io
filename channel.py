import logging

from flask import Blueprint, request, jsonify
import requests
from rasa_core.channels.channel import UserMessage, OutputChannel
from rasa_core.channels.rest import HttpInputComponent
import json

logger = logging.getLogger(__name__)


class CollectingOutputChannel(OutputChannel):
    """Output channel that collects send messages in a list
    (doesn't send them anywhere, just collects them)."""

    def __init__(self):
        self._messages = []

    def clear(self):
        self._messages.clear()

    def get_messages(self):
        return self._messages

    def send_text_message(self, recipient_id, message):
        self._messages.append(message)

    def send_text_with_buttons(self, recipient_id, message, buttons):
        self._messages.append(
            {"recipient_id": recipient_id, "text": message, "data": buttons})


class CustomInputCollectingComponent(HttpInputComponent):
    """A custom http input channel.
    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa Core and
    retrieve responses from the agent."""

    def __init__(self, url, access_token=None):
        self.out_channel = CollectingOutputChannel()

    def blueprint(self, on_new_message):
        custom_webhook = Blueprint('custom_webhook', __name__)

        @custom_webhook.route("/", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @custom_webhook.route("/webhook", methods=['POST'])
        def receive():
            payload = request.json
            sender_id = payload.get("sender", None)
            text = payload.get("message", None)

            # clear previous messages first
            self.out_channel.clear()

            on_new_message(UserMessage(text, self.out_channel, sender_id))

            # append messages from this request
            messages = self.out_channel.get_messages()

            return jsonify({"messages": messages})

        return custom_webhook

###
# ======
###


class CustomOutputChannel(OutputChannel):
    """A bot that uses a custom channel to communicate."""

    def __init__(self, url, access_token):
        self.access_token = access_token
        self.url = url

    def send_text_message(self, recipient_id, message):
        # you probably use http to send a message
        url = self.url
        if self.access_token is not None:
            headers = {"Auth-token": self.access_token}
        else:
            headers = {}

        data = {
            'message': message
        }

        requests.post(
            url,
            json=data,
            headers=headers
        )


class CustomInputComponent(HttpInputComponent):
    """A custom http input channel.
    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa Core and
    retrieve responses from the agent."""

    def __init__(self, url, access_token=None):
        self.out_channel = CustomOutputChannel(url, access_token)

    def blueprint(self, on_new_message):
        custom_webhook = Blueprint('custom_webhook', __name__)

        @custom_webhook.route("/", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @custom_webhook.route("/webhook", methods=['POST'])
        def receive():
            payload = request.json
            sender_id = payload.get("sender", None)
            text = payload.get("message", None)
            on_new_message(UserMessage(text, self.out_channel, sender_id))
            return jsonify({"status": "success"})

        return custom_webhook
