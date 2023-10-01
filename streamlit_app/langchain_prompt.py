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
    
    preguntaString = "Quiero cocinar pollo"

    if len(message) == 1 or message == "":
        message = preguntaString

    infoAdicional = "lo quiero hacer al horno"
    promptBase = """Eres una asistente de recetas de cocina que ayuda a los usuarios a encontrar recetas de cocina.
    Pregunta: {pregunta}
    InfoAdicional: {infoAdicional}
    Respuesta:"""
    
    # Instantiation using from_template (recommended)
    # prompt_template = PromptTemplate.from_file("./streamlit_app/prompt_templates/recipe_assistant.yml")
     
     # Instantiation using from_template (recommended)
    prompt_template = PromptTemplate.from_template(promptBase)
    prompt_value = prompt_template.format(pregunta=preguntaString, infoAdicional=infoAdicional)
    print(prompt_value)

    tokens = openai_llm.get_num_tokens(prompt_value)
    print("el numero de tokens es", tokens)

    response = openai_llm.generate(prompt_value)
    print(response)

    return response