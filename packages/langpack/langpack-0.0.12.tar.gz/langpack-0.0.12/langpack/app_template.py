""" Example
curl -H "Content-Type: application/json" \
    -X POST -d '{{"input_key"}: }' \
    http://127.0.0.1:5000/predict
"""

from flask import Flask, jsonify, request, send_from_directory

from langpack import apis

langchain_app = apis.unpack("app.json")

app = Flask(__name__, static_folder="static")


@app.route("/chat", methods=["GET"])
def chat():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if type(langchain_app).__name__ == "AgentExecutor":
        result = langchain_app(data["query"])
    else:
        result = langchain_app(data)

    print(result)

    return jsonify({"result": result[{"output_key"}]})


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
