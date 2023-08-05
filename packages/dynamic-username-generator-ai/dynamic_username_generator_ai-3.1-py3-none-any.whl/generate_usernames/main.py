import requests


def generate_usernames(user_name, OPENAI_API_KEY, username_for=None):
    prompt_parts = [
        f"I want you to help in creating 20 different usernames",
        f"for platform {username_for} " if username_for else "",
        f"for '{user_name}'."
    ]

    prompt = " ".join(prompt_parts)
    generated_usernames = generate_username(prompt.strip(), OPENAI_API_KEY)
    return generated_usernames


def generate_username(prompt, OPENAI_API_KEY):
    url = 'https://api.openai.com/v1/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    data = {
        "model": 'text-davinci-003',
        "prompt": prompt,
        "temperature": 1,
        "max_tokens": 300
    }
    # print(url, headers, data)
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        generated_usernames_str = response_data['choices'][0]['text'].strip()
        generated_usernames = clean_response(generated_usernames_str)
        return generated_usernames
    else:
        return None


def clean_response(names_string: str) -> list:
    names = names_string.split("\n")
    result_names = []
    for name in names:
        s_names = name.strip().split(".")
        if len(s_names) > 1:
            result_names.append(s_names[1].strip())
    return result_names
