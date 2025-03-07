from openai import OpenAI

class LLMInitializer:
    """
    A class to initialize and interact with a Large Language Model (LLM) provider.
    Attributes:
        llm_provider (str): The name of the LLM provider. Default is "OpenAI".
        llm_name (str): The name of the LLM model. Default is "gpt-4o".
        client (object): The client object for interacting with the LLM provider.
    Methods:
        __init__():
            Initializes the LLMInitializer with default provider and model.
        intialize_client():
            Initializes and returns the client object for the specified LLM provider.
        get_response(system_prompt, user_prompt, response_format_pydantic_model):
            Sends a prompt to the LLM and returns the formatted response.
            Args:
                system_prompt (str): The system prompt to guide the LLM.
                user_prompt (str): The user prompt to query the LLM.
                response_format_pydantic_model (pydantic.BaseModel): The Pydantic model to format the response.
            Returns:
                object: The parsed response from the LLM.
    """

    def __init__(self):
        self.llm_provider = "OpenAI"
        self.llm_name = "gpt-4o"
        self.client = self.intialize_client()

    def intialize_client(self):
        if self.llm_provider == "OpenAI":
            return OpenAI()
        else:
            raise ValueError("LLM provider not supported")
        
    def get_response(self, system_prompt, user_prompt, response_format_pydantic_model):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        completion = self.client.beta.chat.completions.parse(
            model=self.llm_name,
            messages=messages,
            response_format = response_format_pydantic_model,
            temperature=0.2
        )

        return completion.choices[0].message.parsed
            