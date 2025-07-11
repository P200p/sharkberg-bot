from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

app = FastAPI()

model_id = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)
chatbot = pipeline("text-generation", model=model, tokenizer=tokenizer)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")
    prompt = f"ตอบกลับด้วยภาษาธรรมชาติ: {message}"
    output = chatbot(prompt, max_new_tokens=100)[0]["generated_text"]
    return {"reply": output.strip()}
