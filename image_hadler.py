from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler
import base64


def convert_bytes_to_base64(image_bytes):
    encoded_string = base64.b64encode(image_bytes).decode("utf-8")
    return "data:image/jpeg;base64,"+ encoded_string


def handle_image(image_bytes, user_massage):

    chat_handler = Llava15ChatHandler(clip_model_path="./models/llava/mmproj-model-f16.gguf")
    llm = Llama(
        model_path="./models/llava/ggml-model-q5_k.gguf",
        chat_handler=chat_handler,
        logits_all=True,
        n_ctx=2048, 
    )
    image_base64 = convert_bytes_to_base64(image_bytes)
    output = llm.create_chat_completion(
        messages = [
            {"role": "system", "content": "You are an assistant who perfectly describes images."},
                {
                "role": "user",
                    "content": [
                        {"type" : "text", "text": "What's in this image?"},
                        {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg" } }
                    ]
                }
            ]
        )
    print(output)
    return output["choices"][0]["message"]["content"]