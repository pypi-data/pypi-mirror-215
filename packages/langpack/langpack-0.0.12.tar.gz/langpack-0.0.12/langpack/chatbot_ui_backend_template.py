"""
Backend for chatbot-ui
"""
import json
import logging
import os
import time

import requests
from flask import Flask, Response, request, stream_with_context
from werkzeug.datastructures import Headers

from langpack import apis

PORT = 5000

app = Flask(__name__)


def create_resps(results, finish_reason):
    data = {
        "id": "chatcmpl",
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": "gpt-3.5-turbo",
        "choices": [
            {
                "delta": {"content": results},
                "index": 0,
                "finish_reason": finish_reason,
            }
        ],
    }

    return data


@app.route("/v1/models", methods=["GET"])
def get_models():
    headers = {
        "Authorization": request.headers.get("Authorization"),
        "Content-Type": "application/json",
    }
    r = requests.get("https://api.openai.com/v1/models", headers=headers)
    resp = Response(r.content, status=r.status_code, content_type="application/json")
    resp.headers["openai-organization"] = request.headers.get("openai-organization", "")
    resp.headers["openai-version"] = request.headers.get("openai-version", "")
    resp.headers["openai-processing-ms"] = request.headers.get("processing-ms", 0)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@app.route("/v1/chat/completions", methods=["POST"])
def post_chat_completions():
    # Three things need to be override for each request:
    # 1. memory
    # 2. temperature
    # 3. openai_api_key

    openai_api_key = request.headers.get("Authorization").replace("Bearer ", "")
    os.environ["OPENAI_API_KEY"] = openai_api_key

    post_data = request.get_json()

    question = post_data["messages"][-1]["content"]
    # temperature = float(post_data.get("temperature", 0.0))

    langchain_app = apis.unpack("app.json")

    langchain_app.memory.chat_memory.clear()
    for msg in post_data["messages"]:
        if msg["role"] == "user":
            langchain_app.memory.chat_memory.add_user_message(msg["content"])
        elif msg["role"] == "assistant":
            langchain_app.memory.chat_memory.add_ai_message(msg["content"])
    langchain_app.memory.load_memory_variables({})

    try:
        results = langchain_app.run(question)
    except Exception as e:
        results = e

    data = create_resps(results, None)
    data_fin = create_resps("[DONE]\n\n", "DONE")

    headers = Headers()
    headers.add("Content-Type", "text/event-stream")
    headers.add("Cache-Control", "no-cache")
    headers.add("Connection", "keep-alive")

    resps = [
        "data: " + json.dumps(data) + "\n\n",
        "data: " + json.dumps(data_fin) + "\n\n",
    ]

    def generate():
        for resp in resps:
            yield resp

    return Response(stream_with_context(generate()), headers=headers)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=PORT)
