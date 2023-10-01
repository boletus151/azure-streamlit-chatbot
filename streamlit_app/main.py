import streamlit as st
import yaml
from llm_bot import dummy_bot, echo_bot #contains logic for bot's response
from langchain_chat_prompt_examples import promptExamplesSendMessage
from langchain_chat_prompt import cookingChatSendMessage
from langchain_prompt import sendMessage

AzureOpenAI = "AzureOpenAI"
AzureChatOpenAI = "AzureChatOpenAI"
AzureChatOpenAIExamples = "AzureChatOpenAIExamples"

# Read config yaml file
with open('./streamlit_app/config.yml', 'r') as file:
    config = yaml.safe_load(file)

st.session_state.config = config

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "AzureOpenAI"

def sendChat(message):
    if st.session_state.selected_model == AzureOpenAI:
        return sendMessage(message)
    elif st.session_state.selected_model == AzureChatOpenAIExamples:
        return promptExamplesSendMessage(message)
    elif st.session_state.selected_model == AzureChatOpenAI:        
        return cookingChatSendMessage(message)
    else: return "No model selected"


title = config['streamlit']['title']
avatar = {
    'user': None,
    'assistant': config['streamlit']['avatar']
}

# Set page config
st.set_page_config(
    page_title=config['streamlit']['tab_title'], 
    page_icon=config['streamlit']['page_icon'], 
    )

# Set sidebar
def setRadioButton():
    selected = st.session_state.radio_id
    setSelected(selected)
    
st.sidebar.title("About")
st.sidebar.info(config['streamlit']['about'])

method = st.sidebar.radio(
    "Choose a method",
    [AzureChatOpenAIExamples+"-Ingredients", AzureChatOpenAI+"-Cooking", AzureOpenAI],
    index=0,
    on_change=setRadioButton,
    key="radio_id"
)

# Set logo
st.image(config['streamlit']['logo'], width=50)

# Set page title
st.title(title)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [] 
    st.session_state.messages.append({
        "role": "assistant", 
        "content": config['streamlit']['assistant_intro_message']
        })

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=avatar[message["role"]]):
        st.markdown(message["content"])


def getTitleBySelectedModel(selected_model):
    if selected_model == AzureChatOpenAIExamples:
        return config['streamlit']['ingredients_examples']
    elif selected_model == AzureChatOpenAI:        
        return config['streamlit']['cook_conversation']
    elif selected_model == AzureChatOpenAI:        
        return config['streamlit']['only_azureopenai']

def setSelected(model):
    st.session_state.selected_model = model.split("-")[0]
    title = getTitleBySelectedModel(st.session_state.selected_model)
    st.session_state.messages[-1]["content"] = title
    for message in st.session_state.messages:
        print(message)


# React to user input
if prompt := st.chat_input("Send a message"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response    
    response = sendChat(prompt)
    with st.chat_message("assistant", avatar=config['streamlit']['avatar']):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


    