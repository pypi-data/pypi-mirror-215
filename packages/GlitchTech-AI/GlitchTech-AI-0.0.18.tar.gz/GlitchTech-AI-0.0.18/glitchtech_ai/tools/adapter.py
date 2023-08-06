import requests


class OpenAi:
    def __init__(self, **kwargs):
        self.prompt = kwargs.get("prompt")
        self.token = kwargs.get("token")
        self.temperature = kwargs.get("temperature", 0.7)
        self.persistent_messages = kwargs.get("persistent_messages", True)

        self.host = "https://api.openai.com"
        self.headers = {}
        self.session_usage = {}

        self.messages = []

        self.data = {
            "model": "gpt-3.5-turbo",
            "temperature": self.temperature,
        }

        if self.token:
            self._update_headers()

    def update_prompt(self, prompt: str):
        """
        Update OpenAI prompt.
        :param prompt:
        :return:
        """
        self.prompt = prompt
        return self.prompt

    def update_token(self, token: str):
        """
        Update headers with OpenAI token.
        :param token:
        :return:
        """
        self.token = token
        return self._update_headers()

    def chat_completions(self, user_input: str) -> str:
        """
        Utilize OpenAI's Chat Completions endpoint.
        :param user_input:
        :return: Contents
        """

        if not self.token:
            return "[!] No API token detected."

        url = f"{self.host}/v1/chat/completions"

        self.data["messages"] = self._manage_messages(user_input=user_input)

        r = requests.post(url, headers=self.headers, json=self.data)

        if r.json().get("error"):
            self.data["messages"].pop()
            return f"[!] {r.json().get('error')}"

        if r.json().get("usage"):
            self.session_usage = self._add_dicts(
                r.json().get("usage"), self.session_usage
            )

        return self._get_content(ai_resp=r.json())

    @staticmethod
    def _add_dicts(dict1, dict2):
        result = {}
        for key in dict1.keys() | dict2.keys():
            result[key] = dict1.get(key, 0) + dict2.get(key, 0)
        return result

    @staticmethod
    def _get_content(ai_resp: dict):
        if ai_resp.get("choices"):
            messages = [
                choice["message"].get("content")
                for choice in ai_resp.get("choices")
                if choice.get("message")
            ]
            return "\n".join(messages)

    def _update_headers(self):
        self.headers = {"Authorization": f"Bearer {self.token}"}
        return self.headers

    def _manage_messages(self, user_input: str) -> list[dict]:
        if not self.persistent_messages:
            self.messages = []

        if not self.messages and self.prompt:
            self.messages.append({"role": "system", "content": self.prompt})

        self.messages.append({"role": "user", "content": user_input})
        return self.messages


if __name__ == "__main__":
    oa = OpenAi()
    print(
        oa.chat_completions(user_input="What do you call yourself?"),
        oa.session_usage,
        sep="\n",
    )
