import os
from openai import OpenAI, OpenAIError
from llama_cpp import Llama
import requests
import json

class OpenAIChatbot:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def chat_with_ai(self, user_input):
        try:
            completion = self.client.chat.completions.create(
                model="whisper-1", 
                messages=[{
                    "role": "Je bent een vriendelijke Nederlandse taalcoach.",
                    "content": user_input
                }]
            )
            print(completion.choices[0].text)
            print(dict(completion).get('usage'))
            print(completion.model_dump_json(indent=2))
            return completion.choices[0].text
        except OpenAIError as e:
            return f"Error from OpenAI API: {str(e)}"

class LlamaChatbot:
    def __init__(self, model_path):
        # Validate model path exists before initializing
        if not os.path.exists(model_path):
            raise ValueError(f"Model file not found at path: {model_path}")
            
        try:
            self.llm = Llama(
                model_path=model_path,
                n_ctx=2048,
                n_threads=4,
                verbose=True  # Enable verbose logging for debugging
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Llama model: {str(e)}")
    
    def chat_with_ai(self, user_input):
        try:
            prompt = f"Je bent een vriendelijke Nederlandse taalcoach.\n\nUser: {user_input}\nAssistant:"
            output = self.llm(
                prompt,
                max_tokens=2048,
                temperature=0.7,
                top_p=0.95,
                echo=False
            )
            return output['choices'][0]['text'].strip()
        except Exception as e:
            return f"Error from Llama: {str(e)}"

class LlamaChatbot2:
    def __init__(self, model_path):
        try:
            self.llm = Llama.from_pretrained(
                repo_id="itlwas/Mistral-7B-Instruct-v0.1-Q4_K_M-GGUF",
                filename="mistral-7b-instruct-v0.1-q4_k_m.gguf"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Llama model: {str(e)}")

    def chat_with_ai(self, user_input):
        try:
            response = self.llm.create_chat_completion(
                messages=[
                    {
                        "role": "system", 
                        "content": "Je bent een vriendelijke Nederlandse taalcoach."
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                max_tokens=2048,
                temperature=0.7,
                top_p=0.95
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"Error from Llama: {str(e)}"


class LlamaAPIChatbot:
    def __init__(self, base_url="http://localhost:8000/api", model_name="llama3"):
        self.base_url = base_url
        self.model_name = model_name

    def get_response(self, input_text):
        try:
            url = "http://localhost:8000/api/generate"
            headers = {
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model_name,
                "prompt": input_text,
                "stream": True
            }

            # Send the request with stream=True to handle streaming responses
            with requests.post(url, headers=headers, data=json.dumps(payload), stream=True) as response:
                response.raise_for_status()

                full_text = ""
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            full_text += data.get("response", "")
                        except json.JSONDecodeError:
                            print("Received non-JSON line:", line)

                return full_text
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    def chat_with_ai(self, user_input):
        input_text = f"Je bent een vriendelijke Nederlandse taalcoach. User zegt: {user_input}"
        response = self.get_response(input_text)
        return response


class ChatbotFactory:
    @staticmethod
    def create_chatbot(model_type="openai", **kwargs):
        """
        Factory method to create appropriate chatbot instance
        Args:
            model_type: "openai" or "llama"
            **kwargs: Additional arguments to pass to the chatbot constructor
        Returns:
            Instance of OpenAIChatbot or LlamaChatbot
        """
        if model_type.lower() == "openai":
            return OpenAIChatbot()
        elif model_type.lower() == "llama3":
            return LlamaChatbot2()
        elif model_type.lower() == "llamaapi":
            return LlamaAPIChatbot()
        else:
            raise ValueError(f"Unknown model type: {model_type}. Choose 'openai' or 'llama'")
