
import litserve as ls
from llama_cpp import Llama
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

class SimpleLitAPI(ls.LitAPI):
    def setup(self, device):
        self.llm = Llama(
            model_path="Llama-3.2-1B-Instruct-Q4_K_M.gguf",
            verbose=False 
        )
    def decode_request(self, request):
        return request

    def predict(self, input):
        temperature = input.get("temperature", 1.0) 
        max_tokens = input.get("max_tokens", 100)
        top_k = input.get("top_k", 50)  
        top_p = input.get("top_p", 0.9)       
        repeat_penalty = input.get("repeat_penalty", 1.0) 
        return self.llm.create_chat_completion(
            messages=input["messages"],
            temperature=temperature,
            max_tokens=max_tokens,
            top_k=top_k,
            top_p=top_p,
            repeat_penalty=repeat_penalty,
        )

    def encode_response(self, output):
        return {"output": output}
    
    def authorize(self, auth: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        if auth.scheme != "Bearer" or auth.credentials != "1234":
            raise HTTPException(status_code=401, detail="Bad token")
        
if __name__ == "__main__":
    api = SimpleLitAPI()
    server = ls.LitServer(api, accelerator="cpu")
    server.run(port=7860)