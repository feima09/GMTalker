import copy
import json
import time
import os
from utils import httpx_client, get_logger, config
import requests

logging = get_logger()
home_dir = os.getcwd()


class OpenAI:
    def __init__(self):
        self.config = config.Config.get("GPT", {})
        
        self.api_endpoint = self.config.get("api_endpoint", "")
        
        self.headers = copy.deepcopy(self.config.get("request_header", {}))
        self.headers['Authorization'] = f"Bearer {self.config.get('api_key', 'empty')}"
        self.headers["Content-Type"] = "application/json; charset=UTF-8"
        
        self.reset_body()
        
        self.prompt = config.Prompt
            
        self.assistant_message = ""
        
    
    def set_body(self, message: str) -> dict:
        messages = self.body.get("messages", [])
        
        if self.body is None:
            messages.append({
                "role": "system",
                "content": self.prompt
            })
            messages.append({
                "role": "user",
                "content": message
            })
        else:
            messages.append({
                "role": "assistant",
                "content": self.assistant_message
            })
            messages.append({
                "role": "user",
                "content": message
            })
            self.assistant_message = ""
            
        self.body["messages"] = messages
        
        return self.body
    
    
    async def generate_stream(self, message: str):
        try:
            start_time = time.time()
                
            async with httpx_client.stream(
                "POST",
                self.api_endpoint,
                json=self.set_body(message),
                headers=self.headers,
            ) as response:
                first_repsonse_time = time.time()
                logging.info(f"First received response time: {first_repsonse_time - start_time:.2f}s")
                
                response.raise_for_status()
                
                chunk_total = 0
                
                async for chunk in response.aiter_bytes():
                    if chunk:
                        chunk_total += 1
                        yield chunk
            
            end_time = time.time()
            logging.info(f"All data received time: {end_time - first_repsonse_time:.2f}s")
            logging.info(f"Average chunk time: {(end_time - first_repsonse_time) / chunk_total:.2f}s")
            logging.info(f"All response time: {end_time - start_time:.2f}s")
                    
            yield None
        except Exception as e:
            raise Exception(f"Failed to request GPT service: {e}")


    def get_response_content(self, response) -> str:
        try:
            json_data = json.loads(response)
            content = json_data['choices'][0]['delta'].get('content', '')
            return content
        
        except json.JSONDecodeError:
            logging.error(f"Failed to parse JSON data: {response}")
            return ""
        

    async def create_text_stream(self, gpt_stream):
        buffer = b""
        split_bytes = b""
        async for chunk in gpt_stream:
            if chunk is None:
                break
            buffer += chunk
            
            if b"\r\n\r\n" in buffer:
                split_bytes = b"\r\n\r\n"
            elif b"\n\n" in buffer:
                split_bytes = b"\n\n"
            else:
                continue
                
            while split_bytes in buffer:
                line: bytes
                line, buffer = buffer.split(split_bytes, 1)
                text = line.decode("utf-8")
                
                if "data:" in text:
                    text = text.split("data:")[1].strip()
                    if text == "[DONE]":
                        yield None
                        break
                    
                    content = self.get_response_content(text)
                    if content:
                        yield content
                        self.assistant_message += content


    @staticmethod
    async def output_stream(gpt_stream):
        chunk: bytes
        async for chunk in gpt_stream:
            if chunk is None:
                break
            yield chunk
            
    
    def reset_body(self):
        self.body = copy.deepcopy(self.config.get("request_body", ""))
        self.body["stream"] = True


    def test(self):
        try:
            self.__init__()
            self.body["stream"] = False
            response = requests.post(
                self.api_endpoint,
                json=self.set_body("这是一条测试信息。"),
                headers=self.headers,
                timeout=10
            )
            if response.status_code != 200:
                raise Exception(f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
            else:
                return True, "测试通过"
        except Exception as e:
            return False, str(e)
        finally:
            self.reset_body()

