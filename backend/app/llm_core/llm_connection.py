from langchain_ollama import ChatOllama

from backend import config


def get_llm():
    if config.llm_provider == "ollama":
        return ChatOllama(
            model=config.MODEL,
            temperature=0.3,
        )

    raise ValueError(
        f"Unsupported LLM provider: {config.llm_provider}"
    )

def test_llm():
    llm=get_llm()
    response = llm.invoke(
        "tell me a joke in 10 words"
    )

    return (response.content)

#print(test_llm())