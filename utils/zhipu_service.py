from zhipuai import ZhipuAI
import base64


class ZhipuService:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self.client = ZhipuAI(api_key=api_key)

    def open_img_to_base64(self, img_file: str) -> str:
        img_base = base64.b64encode(img_file.read()).decode("utf-8")
        return img_base

    def bytes_to_base64(self, img_bytes: bytes) -> str:
        img_base = base64.b64encode(img_bytes).decode("utf-8")
        return img_base

    def _chat_with_verion_model(
        self, content: str, img_base: str, model="glm-4v-plus"
    ) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": img_base}},
                        {
                            "type": "text",
                            "text": content,
                        },
                    ],
                }
            ],
            stream=True,
        )
        for chunk in response:
            yield (chunk.choices[0].delta.content)

    def chat_stream(self, content: str, img_base: str = None, model="glm-4v-plus"):
        if model == "glm-4v-plus":
            yield from self._chat_with_verion_model(content, img_base)
