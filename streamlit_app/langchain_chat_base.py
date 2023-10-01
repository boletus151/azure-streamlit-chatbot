OPENAI_API_KEY= ""
OPENAI_ENDOPOINT= "https://.openai.azure.com/"
OPENAI_DEPLOYMENT_NAME="chat"
OPENAI_API_VERSION= "2023-05-15"

import streamlit as st
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

def sendChat(message):

    config = None
    try:
        config = st.session_state.config
    except:
        return "No config file found"

    openai_llm = AzureChatOpenAI(
    openai_api_base=config['variables']['OPENAI_ENDOPOINT'],
    openai_api_version=config['variables']['OPENAI_API_VERSION'],
    deployment_name=config['variables']['OPENAI_DEPLOYMENT_NAME'],
    openai_api_key=config['variables']['OPENAI_API_KEY'],
    openai_api_type="azure",
    temperature=0)


    if len(message) == 1:
        message = "supercalifragilisticoespiralidoso"
    openai_llm([HumanMessage(content=message)])
    message = [
        SystemMessage(content="You are a helpful assistant that translates any language to English."),
        HumanMessage(content=message)
    ]
    result = openai_llm(message)
    # batch_messages = [
    #     [
    #         SystemMessage(content="You are a helpful assistant that translates English to French."),
    #         HumanMessage(content="I love programming.")
    #     ],
    #     [
    #         SystemMessage(content="You are a helpful assistant that translates English to French."),
    #         HumanMessage(content="I love artificial intelligence.")
    #     ],
    # ]
    # result = chat.generate(batch_messages)
    return result
