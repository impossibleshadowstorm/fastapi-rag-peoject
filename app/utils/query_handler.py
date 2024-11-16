import os
from app.core.config import settings

os.environ["OPENAI_API_KEY"] = settings.OPEN_AI_SECRET_KEY

from openai import OpenAI


# Initialize OpenAI client
client = OpenAI()


def generate_response(query: str, context: str):
    """Generate a response using OpenAI GPT model with conversation history."""
    prompt = get_prompt(context, query)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        temperature=0,
        max_tokens=50,
    )

    return response.choices[0].message.content


def get_prompt(context, query):
    prompt = f"""Based on the following context, please provide a relevant and contextual response.
    If the answer cannot be derived from the context, only use the conversation history or say "I cannot answer this based on the provided information."

    Context from documents:
    {context}

    Human: {query}

    Assistant:"""
    return prompt


def handle_query(document_data: str, query: str):
    """Processes the query using the document data and OpenAI model."""
    try:
        # Generate response using OpenAI's chat completion
        response_content = generate_response(query=query, context=document_data)
        return {"answer": response_content}
    except Exception as e:
        # Handle errors (like rate limits, etc.)
        return {"error": str(e)}
