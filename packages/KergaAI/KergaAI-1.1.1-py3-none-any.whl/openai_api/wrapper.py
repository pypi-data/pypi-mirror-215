import json as JSON
import os
import re
from dotenv import load_dotenv
import openai


def text(resp: str) -> dict:
    if not "response_ok" in resp:
        return "Error: No 'response_ok' in response, failure."
    return resp['response_ok'].strip()


def json(resp: str) -> dict:
    if not "response_ok" in resp:
        return {"Error": "No 'response_ok' in response, failure."}
    data = resp['response_ok'].strip()

    rep = re.findall(
        r"#stj(.*?)#enj", data, re.DOTALL)

    if rep:
        res = JSON.loads(rep[0])
        # print("Result: ", res)
        return res
    else:
        return {"Error": f"'#stj' and '#enj' not found in {data}"}


def gpt(prompt, model="text-davinci-003", temperature=0.75,
             max_tokens=100, top_p=1):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("You must define your API key")
    openai.api_key = api_key
    print(f"API key found: {api_key[:5]}*****")

    print(f"Prompt: ```\n{prompt}\n```")

    try:
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=0,
            presence_penalty=0
        )
        try:
            rep = response['choices'][0]['text']
        except Exception as e:
            print(f"Could not process {response}")
            return {"error_1": e}

        return {"response_ok": rep}

        # resultats = re.findall(
        #     r"#stj(.*?)#enj", response, re.DOTALL)
        # if resultats:
        #     res = JSON.loads(resultats[0])
        #     print("Result: ", res)
        #     return res

    except Exception as e:
        return {"error_2": e}
