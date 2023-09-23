import openai
import os
openai.api_key = "*****************************"

def summarize(text):
    try:
        augmented_prompt = f"Summarize this text: {text}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=augmented_prompt,
            temperature=0.5,
            max_tokens=1024,
        )
        summary = response.choices[0].text.strip()
        return summary
    except Exception as error:
        print("There is an error", error)
        return None
    
