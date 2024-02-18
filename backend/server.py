from flask import Flask, jsonify, request
from voice_ai import voice_request
from text_generator import generate_text_async
from ocr import pdfToString
import os
import random
import string
import tempfile
import threading
import asyncio
import base64

app = Flask(__name__)

async def process_request(hash_str: str, file_path : str, status_path: str):
    try:
        with open(status_path, "w") as f:
            f.writelines('{"status": "processing", "state": "1"}\n')

        text = pdfToString(file_path)
        print("Read text: " + text)

        with open(status_path, "w") as f:
            f.writelines('{"status": "processing", "state": "2"}\n')

        corrected_text = await generate_text_async(text)
        print("Corrected text: " + corrected_text)

        with open(status_path, "w") as f:
            f.writelines('{"status": "processing", "state": "3"}\n')

        url = await voice_request(hash_str, corrected_text)

        print(url)

        encoded = ""

        with open(url, "rb") as f:
            encoded_f1 = base64.b64encode(f.read())
            encoded = "data:audio/wav;base64," + str(encoded_f1)

        with open(status_path, "w") as f:
            f.writelines('{"status": "done", "data": "' + encoded + '"}\n')

    except Exception as e:
        with open(status_path, "a") as f:
            f.writelines('{"status": "failed", "error": "' + str(e) + '"}\n')

def process_rq_to_async(hash_str: str, file_path: str, status_path: str):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(process_request(hash_str, file_path, status_path))
        loop.close()
    except Exception as e:
        with open(status_path, "a") as f:
            f.writelines('{"status": "failed", "error": "' + str(e) + '"}\n')

@app.route("/submit", methods=['POST'])
def submit_request():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "File parameter is missing."}), 400


        # Generate a 10 character random ASCII hash
        random_hash = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        print("Hash: " + random_hash)

        file = request.files["file"]

        file_path = os.path.join(tempfile.gettempdir(), f"tuff2dbug/{random_hash}.pdf")
        status_path = os.path.join(tempfile.gettempdir(), f"tuff2dbug/{random_hash}.txt")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)
        
        with open(status_path, "w") as f:
            f.writelines('{"status": "pending"}')

        print("Processing request...")

        t = threading.Thread(target=process_rq_to_async, args=(random_hash, file_path, status_path,), daemon=True)
        t.start()

        return jsonify({"status": "processing", "hash": random_hash}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/status", methods=['GET'])
def get_status():
    hash_str = request.args.get("hash")
    
    if not hash_str.isalnum():
        return jsonify({"error": "hash is invalid"})
    
    file_path = os.path.join(tempfile.gettempdir(), f"tuff2dbug/{hash_str}.txt")

    output = ""

    try:
        with open(file_path) as f:
            output = f.read()
    except Exception as e:
        return jsonify({"error": "hash is invalid"})

    return output

if __name__ == "__main__":
    app.run(debug=True)