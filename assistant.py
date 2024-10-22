import json
import time
from pprint import pprint

from openai import OpenAI

from dall_e import DallE
from secret.keys import OPENAI_API_KEY

ASSISTANT_ID = "asst_PNgJ8gWduFNFrjv819CYJZWG"

"""
available tools:
{
  "name": "generate_image",
  "description": "Takes a prompt in string and returns once an image is generated",
  "strict": true,
  "parameters": {
    "type": "object",
    "required": [
      "prompt"
    ],
    "properties": {
      "prompt": {
        "type": "string",
        "description": "The text prompt for generating the image"
      }
    },
    "additionalProperties": false
  }
}

"""


class Assistant:
    def __init__(self):
        self._client = OpenAI(api_key=OPENAI_API_KEY)
        self._assistant = self._client.beta.assistants.retrieve(ASSISTANT_ID)
        self._thread = self._client.beta.threads.create()

        # tools
        self._dalle = DallE()

    def get_reponse(self, user: str, prompt: str) -> dict:
        """Returns response from assistant in dict:
        {
            "response": "message content",
            "file_path": "file path" (optional)
        }
        """

        result = {}  # dict to store response

        message = self._client.beta.threads.messages.create(
            thread_id=self._thread.id,
            role="user",
            content=prompt,
        )

        run = self._client.beta.threads.runs.create(
            thread_id=self._thread.id,
            assistant_id=ASSISTANT_ID,
            instructions=f"Refer to the user as {user}",
        )

        while run.status != "completed":
            print(run.status)
            run = self._client.beta.threads.runs.retrieve(
                thread_id=self._thread.id, run_id=run.id
            )

            if run.status == "requires_action":
                print("handling required action")
                tool_list = run.required_action.submit_tool_outputs.tool_calls
                print(tool_list)
                tool_outputs = []
                for tool in tool_list:
                    if tool.function.name == "generate_image":
                        arg = json.loads(tool.function.arguments)["prompt"]
                        image_path = self._dalle.generate_image(arg)
                        result["file_path"] = image_path

                        tool_outputs.append(
                            {
                                "tool_call_id": tool.id,
                                "output": "Done",
                            }
                        )

                        # submit tool output
                        self._client.beta.threads.runs.submit_tool_outputs(
                            thread_id=self._thread.id,
                            run_id=run.id,
                            tool_outputs=tool_outputs,
                        )
            elif run.status == "queued":
                print("Queued")
                time.sleep(1)
            elif run.status == "in_progress":
                print("In progress")
                time.sleep(1)
            elif run.status == "expired":
                raise Exception("Run expired")
            elif run.status == "cancelling" or run.status == "cancelled":
                raise Exception("Run cancelled")
            elif run.status == "failed":
                raise Exception("Run failed")

        response = self._client.beta.threads.messages.list(thread_id=self._thread.id)
        result["response"] = response.data[0].content[0].text.value

        return result


if __name__ == "__main__":
    a = Assistant()
    resp = a.get_reponse("user", "a cute cat")
    pprint(resp)
    pprint(type(resp))
    print(type(resp.get("response")))
