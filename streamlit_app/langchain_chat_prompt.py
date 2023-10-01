import streamlit as st
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

def cookingChatSendMessage(message):

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

    preguntaString = "Quiero cocinar {receta}".format(receta=message)
    systemContext = """Eres una asistente de recetas de cocina que ayuda a los usuarios a encontrar recetas de cocina y le dice como hacerlas.
     Puedes saludar y ser amable con el usuario si te pregunta como estás, te saluda o similar.
     Puedes hacer lo siguiente:
     Contestar a aquello que esté relacionado con la cocina.
     Contestar osas sobre temas culinarios además de poder dar respuestas relacionadas con cualquier instrumento que se requiera para cocinar.
     Puedes también hablar sobre platos típicosde países o regiones
     Puedes hablar de gustos personales que puedan tener los habitantes de un lugar en en concreto.
     Todo lo que esté fuera del ambito de la cocina no debes contestarlo y debes decir al usuario que no entiendes lo que te está diciendo 
     """
        
    system_message = SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[],template=systemContext))    
       
    user_message_template = PromptTemplate.from_template("{texto}")
    user_message = HumanMessagePromptTemplate(prompt=user_message_template)

    chat_prompt = ChatPromptTemplate.from_messages([user_message, system_message])    
    chat_prompt_value = chat_prompt.format_prompt(texto=preguntaString).to_messages()
    print(chat_prompt_value)

    response = openai_llm(chat_prompt_value)
    print(response)

    return response.content