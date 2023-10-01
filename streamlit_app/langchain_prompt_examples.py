import streamlit as st
from langchain.llms import AzureOpenAI
from langchain.prompts import PromptTemplate, FewShotPromptTemplate


def promptExamplesSendMessage(message):
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

    # preguntaString = "Cuáles son los principales ingredientes de: {receta}".format(receta=message)
    preguntaString = "{receta}".format(receta=message)
    systemContext = """Eres una asistente de cocina que conoce los principales ingrediente de muchas recetas de cocina. 
    Puedes saludar y ser amable con el usuario si te pregunta como estás, te saluda o similar.
    Puedes hacer lo siguiente:
    Como conoces muchas recetas de cocina sabes nombrar muchos ingredientes.
    Todo lo que esté fuera del ambito de la cocina no debes contestarlo y debes decir al usuario que no entiendes lo que te está diciendo."""
    
    examples = [
        { "pregunta": "Cuál es el principal ingrediente de la ensalada", "respuesta": "Una ensalada puede ser de muchos tipos pero en general suele ser la lechuga" },
        { "pregunta": "Cuál es el principal ingrediente de la lasagna", "respuesta": "La lasaña puede ser de carne o verduras pero en general todas llevan láminas de pasta, queso y bechamel" },
        { "pregunta": "Cuál es el principal ingrediente de un postre", "respuesta": "Dependiendo del postre, pero en general todos llevan azucar" },
    ]
    examples_template = "Pregunta: {pregunta}\nRespuesta: {respuesta}\n"
    examples_promt_template = PromptTemplate(input_variables=["pregunta", "respuesta"], template=examples_template)
    # print("These are the examples:")
    # for example in examples:
    #     print(examples_promt_template.format(**example))
    
    prompt_examples = FewShotPromptTemplate(example_prompt=examples_promt_template,
                                            examples=examples,
                                            prefix=systemContext,
                                            suffix="pregunta:{pregunta}\nrespuesta:",
                                            input_variables=["pregunta"])
    prompt_examples_value = prompt_examples.format_prompt(pregunta=preguntaString).to_messages()
    # print("This is the prompt:")
    # print(prompt_examples_value[0].content)

    # to test
    # examples_message_template = PromptTemplate.from_template(template=examples_template)
    # examples_message = examples_message_template.format(pregunta=examples[0]["pregunta"], respuesta=examples[0]["respuesta"]).to_messages()

    response = openai_llm.generate(prompt_examples_value)
    
    print("Pregunta: {pregunta}".format(pregunta=preguntaString))
    print(response.content)

    return response.content