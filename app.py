import streamlit as st
import cohere 
import os
cohere_api_key = os.environ['cohere_api_key']
co = cohere.Client(cohere_api_key)
from cohere.classify import Example

examples = [
    Example("you are hot trash", "Toxic"),  
    Example("go to hell", "Toxic"),
    Example("get rekt moron", "Toxic"),  
    Example("get a brain and use it", "Toxic"), 
    Example("say what you mean, you jerk.", "Toxic"), 
    Example("Are you really this stupid", "Toxic"), 
    Example("I will honestly kill you", "Toxic"),  
    Example("yo how are you", "Benign"),  
    Example("I'm curious, how did that happen", "Benign"),  
    Example("Try that again", "Benign"),  
    Example("Hello everyone, excited to be here", "Benign"), 
    Example("I think I saw it first", "Benign"),  
    Example("That is an interesting point", "Benign"), 
    Example("I love this", "Benign"), 
    Example("We should try that sometime", "Benign"), 
    Example("You should go for it", "Benign")
    ]

if "chat" not in st.session_state:
    st.session_state.chat = []

def Toxicity_detector(text):
    inputs = [text]
    response = co.classify(  
        model='large',  
        inputs=inputs,  
        examples=examples)
    return(response[0].prediction)


def Detoxify_text(text):
    response = co.generate(
    model='command-xlarge-20221108',
    prompt='detoxify this text: '+ text ,
    max_tokens=30,
    temperature=0.9,
    k=0,
    p=0.75,
    frequency_penalty=0,
    presence_penalty=0,
    stop_sequences=[],
    return_likelihoods='NONE')
    return(response.generations[0].text.split("\n")[1])


def main():
    
    # ===================== Set page config and background =======================
    # Main panel setup
    # Set website details
    st.set_page_config(page_title ="Project Peace", 
                       page_icon=':desktop_computer:', 
                       layout='centered')
    """## Project Peace"""

    with st.expander("About"):
        st.write("This App was built for the Cohere 2023 hackathon, Project peace is built on top of Cohere's cutting Edge NLP models, and leveraged to help detect hate speech and detoxify them accross various languages")

    with st.form(key = 'form1', clear_on_submit=False):
        text_message = st.text_area("Write message here")
        submit_button = st.form_submit_button()

    if submit_button:
        if Toxicity_detector(text_message) == "Benign":
            st.session_state.chat.append(text_message)
        else:
            st.session_state.chat.append(Detoxify_text(text_message))

    for i in st.session_state.chat:
        st.write(i+"\n")
        print(i)



if __name__ == "__main__":
    main()