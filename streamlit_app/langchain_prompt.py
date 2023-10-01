OPENAI_API_KEY= ""
OPENAI_ENDOPOINT= "https://.openai.azure.com/"
OPENAI_DEPLOYMENT_NAME="chat"
OPENAI_API_VERSION= "2023-05-15"

import streamlit as st
from langchain.llms import AzureOpenAI
from langchain.prompts import PromptTemplate


def sendMessage(message):

    config = None
    try:
        config = st.session_state.config
    except:
        return "No config file found"

    openai_llm = AzureOpenAI(
        openai_api_base=config['variables']['OPENAI_ENDOPOINT'],
        openai_api_version=config['variables']['OPENAI_API_VERSION'],
        deployment_name=config['variables']['OPENAI_DEPLOYMENT_NAME'],
        openai_api_key=config['variables']['OPENAI_API_KEY'],
        openai_api_type="azure",
        temperature=0)
    
    infoAdicional = "Tu plato favoritos es el gazpacho"
    promptBase = """Eres una asistente de cocina que conoce los principales ingrediente de muchas recetas de cocina. 
    Puedes saludar y ser amable con el usuario si te pregunta como estás, te saluda o similar.
    Puedes hacer lo siguiente:
    Como conoces muchas recetas de cocina sabes nombrar muchos ingredientes.
    Todo lo que esté fuera del ambito de la cocina no debes contestarlo y debes decir al usuario que no entiendes lo que te está diciendo.
    Pregunta: {pregunta}
    Respuesta:"""
    
    prompt_template = PromptTemplate.from_template(promptBase)
    prompt_value = prompt_template.format(pregunta=message)
    # prompt_value = prompt_template.format(pregunta=message, infoAdicional=infoAdicional)
    print(prompt_value)

    tokens = openai_llm.get_num_tokens(prompt_value)
    print("el numero de tokens es", tokens)

    response = openai_llm(prompt_value)
    print(response)

    return response