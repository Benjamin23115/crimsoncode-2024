import tempfile
import websockets
import json
import aiohttp
import os
import sys

async def voice_request(hash_str: str, text: str = None):
    try:
        async with websockets.connect("ws://indigo:7860/queue/join") as ws:
            response = await ws.recv()
            if json.loads(response)["msg"] != "send_hash":
                raise ValueError("The response was invalid.")

            await ws.send(json.dumps({"fn_index": 59, "session_hash": hash_str}))
            
            while True:
                response = await ws.recv()
                response_data = json.loads(response)
                if response_data["msg"] == "estimation":
                    continue
                elif response_data["msg"] == "send_data":
                    data_format = [ text, "\\n", "None",
                            "", "zuckerburg", None, 0, 1,
                            None, 4, 100, 0.2, "DDIM", 8,
                            0, 0.8, 1, 1, 2, 2,
                            ["Conditioning-Free"],
                            False, False
                        ]
                    await ws.send(json.dumps({"fn_index": 59, "session_hash": hash_str, "data": data_format}))
                elif response_data["msg"] == "process_starts":
                    continue
                elif response_data["msg"] == "progress":
                    continue
                elif response_data["msg"] == "process_completed":
                    file_url = "http://indigo:7860/file=" + response_data["output"]["data"][0]["name"]
                    file_path = os.path.join(tempfile.gettempdir(), f"tuff2dbug/{hash_str}.wav")
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    async with aiohttp.ClientSession() as session:
                        async with session.get(file_url) as response:
                            if response.status == 200:
                                with open(file_path, 'wb') as file:
                                    while True:
                                        chunk = await response.content.read(1024)
                                        if not chunk:
                                            break
                                        file.write(chunk)
                            else:
                                raise ValueError(f"Failed to download the file. Status: {response.status}")
                    return file_path
                else:
                    raise ValueError("The response was invalid.")
                
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        raise Exception("An exception occurred: " + exc_tb.tb_frame.f_code.co_filename + ":" + str(exc_tb.tb_lineno))