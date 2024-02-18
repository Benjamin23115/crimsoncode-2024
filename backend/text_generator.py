from langchain_community.llms import KoboldApiLLM
import asyncio

instruction = "You are an AI designed to correct misreads of OCR-read PDFs. Some characters will be misread, such as n being read as m or i being read as l. Some characters may be also be missing.  Use as much of the context as you can to determine the meaning and the corrections required. You will give only the corrected version of the input with no additional comments. Your first input is as follows:"

llm = KoboldApiLLM(endpoint="http://indigo:5001/api/v1/generate",
  stop = ["<|end_of_turn|>"],
  max_context_length = 2048,
  max_length = 100,
  quiet = False,
  rep_pen = 1.1,
  rep_pen_range = 256,
  rep_pen_slope = 1,
  temperature = 0.5,
  tfs = 1,
  top_a = 0,
  top_k = 100,
  top_p = 0.9,
  typical = 1
)

async def generate_text_async(prompt):
    try:
        llm_text = await asyncio.to_thread(llm, "GPT4 Correct User:\n" + instruction + prompt + "\n<|end_of_turn|>GPT4 Correct Assistant:\n")
        return llm_text
    except Exception as e:
        return f"Error occurred: {e}"