from fastapi import FastAPI
from chatbot import ChatbotFactory


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Dutch Learning AI Bot is running!"}

@app.post("/chat/")
async def chat(request: dict):
    import os
    from pathlib import Path

    user_input = request.get("message", "")

    chatbot = ChatbotFactory.create_chatbot(model_type="llamaapi")
    response = chatbot.chat_with_ai(user_input)
    return {"response": response}

