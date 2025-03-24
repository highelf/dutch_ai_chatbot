import requests
import json
class LlamaAPI:
    def __init__(self, base_url, model_name):
        self.base_url = base_url
        self.model_name = model_name

    def get_response(self, input_text):
        try:
            url = "http://localhost:8000/api/generate"
            headers = {
                "Content-Type": "application/json"
            }

            payload = {
#                "role": "Je bent een vriendelijke Nederlandse taalcoach.",
            #    "content": input_text,
                "model": "llama3",
                "prompt": input_text,
                "stream": True  # this is essential to receive chunked stream response
            }

            # Send the request with stream=True to handle streaming responses
            with requests.post(url, headers=headers, data=json.dumps(payload), stream=True) as response:
                response.raise_for_status()

                full_text = ""
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            # Uncomment this to print each chunk as it arrives
                            # print("Partial:", data.get("response", ""))
                            full_text += data.get("response", "")
                        except json.JSONDecodeError:
                            print("Received non-JSON line:", line)

                return full_text
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    def answer_question(self, question):
        input_text = f"Je bent een vriendelijke Nederlandse taalcoach. User zegt: {question}"
        response = self.get_response(input_text)
        return response

    def generate_text(self, prompt):
        input_text = f"{prompt}..."
        response = self.get_response(input_text)
        return response

api = LlamaAPI("http://localhost:8000/api", "llama3")

question = "Hoi"
answer = api.answer_question(question)
print(answer)
