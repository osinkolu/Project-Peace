import streamlit as st
import pandas as pd
import cohere 
import os
from streamlit_option_menu import option_menu
#cohere_api_key = os.environ['cohere_api_key']
cohere_api_key = "T1OdZvYpypbU24ShULboDcLRPelL5rxvyQU4sBKN"
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

if "sender_chat" not in st.session_state:
    st.session_state.sender_chat = []

if "receiver_chat" not in st.session_state:
    st.session_state.receiver_chat = []

if "prev_message_was_toxic" not in st.session_state:
    st.session_state.prev_message_was_toxic = False

if "prev_message_was_toxic1" not in st.session_state:
    st.session_state.prev_message_was_toxic1 = False

if "combined_chat" not in st.session_state:
    st.session_state.combined_chat = []

def Toxicity_detector(text):
    inputs = [text]
    response = co.classify(  
        model='large',  
        inputs=inputs,  
        examples=examples)
    return(response[0].prediction)

################ Function to Detoxify Text in two steps - restructure text and Retain language #########################################333

def Detoxify_text(text):
    return(Rewrite_text(Detoxify_text2(text)))

################ Detoxify Text ###############################################3333

def Detoxify_text2(text):
    response = co.generate(
    model='command-xlarge-20221108',
    prompt='rewrite this text in a benign way: '+ text,
    max_tokens=30,
    temperature=0.9,
    k=0,
    p=0.75,
    frequency_penalty=0,
    presence_penalty=0,
    stop_sequences=[],
    return_likelihoods='NONE')
    print(response.generations[0].text)
    return(response.generations[0].text.split("\n")[1])


########################### Rewrite Text in original Language #####################################################################


def Rewrite_text(text):
    language = co.detect_language(texts=[text]).results[0].language_name
    response = co.generate(
    model='command-xlarge-20221108',
    prompt='rewrite this text'+ "in {} :".format(language) + text,
    max_tokens=30,
    temperature=0.9,
    k=0,
    p=0.75,
    frequency_penalty=0,
    presence_penalty=0,
    stop_sequences=[],
    return_likelihoods='NONE')
    print(response.generations[0].text)
    return(response.generations[0].text.split("\n")[1])


############# Receiver's Page #####################################################################

def Receiver():

    with st.form(key = 'formR', clear_on_submit=False):
        text_message = st.text_area("Write message here")
        submit_button = st.form_submit_button(label="send")

    if submit_button:
        if Toxicity_detector(text_message) == "Benign":
            st.session_state.receiver_chat.append(text_message)
        else:
            try:
                st.session_state.receiver_chat.append(Detoxify_text(text_message))
            except Exception:
                st.warning("Text retracted, Could not detoxify")

    for i in st.session_state.receiver_chat[-5:]:
        st.write(i+"\n")
        print(i)

################################ Sender's Page ###########################################################

def Sender():

    with st.form(key = 'formS', clear_on_submit=True):
        text_message = st.text_area("Write message here")
        submit_button = st.form_submit_button(label="send")

    if submit_button or st.session_state.prev_message_was_toxic:
        if Toxicity_detector(text_message) == "Benign":
            st.session_state.sender_chat.append(text_message)
        else:
            st.session_state.prev_message_was_toxic = True
            st.error("This message is toxic, should i detoxify it?")
            col1,col2, col3 = st.columns([1,1,1])
            with col1:
                if st.button('Yes, detoxify'):
                    print("Detoxifying.....................................................")
                    try:
                        st.session_state.sender_chat.append(Detoxify_text(text_message))
                        st.session_state.prev_message_was_toxic = False
                    except Exception:
                        st.warning("Text retracted, Could not detoxify")
            with col2:
                if st.button("No, send as is"):
                    st.session_state.sender_chat.append(text_message)
                    st.session_state.prev_message_was_toxic = False
            with col3:
                if st.button("Retract message"):
                    st.success("Message retracted")
                    st.session_state.prev_message_was_toxic = False
                    
    for i in st.session_state.sender_chat[-5:]:
        st.write(i+"\n")
        print(i)
    
def Sender1():

    with st.form(key = 'formS1', clear_on_submit=True):
        text_message1 = st.text_area("User 1")
        submit_button1 = st.form_submit_button(label="send")

    if submit_button1 or st.session_state.prev_message_was_toxic1:
        if Toxicity_detector(text_message1) == "Benign":
            st.session_state.combined_chat.append(text_message1)
        else:
            st.session_state.prev_message_was_toxic1 = True
            st.error("This message is toxic, should i detoxify it?")
            col4,col5, col6 = st.columns([1,1,1])
            with col4:
                if st.button('Yes, detoxify'):
                    print("Detoxifying.....................................................")
                    try:
                        st.session_state.combined_chat.append(Detoxify_text(text_message1))
                        st.session_state.prev_message_was_toxic1 = False
                    except Exception:
                        st.warning("Text retracted, Could not detoxify")
            with col5:
                if st.button("No, send as is"):
                    st.session_state.combined_chat.append(text_message1)
                    st.session_state.prev_message_was_toxic1 = False
            with col6:
                if st.button("Retract message"):
                    st.success("Message retracted")
                    st.session_state.prev_message_was_toxic1 = False
                    
    for i in st.session_state.combined_chat[-5:]:
        st.write(i+"\n")
        print(i)

def Sender2():

    with st.form(key = 'formS2', clear_on_submit=True):
        text_message2 = st.text_area("User 2")
        submit_button = st.form_submit_button(label="send")

    if submit_button or st.session_state.prev_message_was_toxic:
        if Toxicity_detector(text_message2) == "Benign":
            st.session_state.combined_chat.append(text_message2)
        else:
            st.session_state.prev_message_was_toxic = True
            st.error("This message is toxic, should i detoxify it?")
            col7,col8, col9 = st.columns([1,1,1])
            with col7:
                if st.button('Yes, detoxify'):
                    print("Detoxifying.....................................................")
                    try:
                        st.session_state.combined_chat.append(Detoxify_text(text_message2))
                        st.session_state.prev_message_was_toxic = False
                    except Exception:
                        st.warning("Text retracted, Could not detoxify")
            with col8:
                if st.button("No, send as is"):
                    st.session_state.combined_chat.append(text_message2)
                    st.session_state.prev_message_was_toxic = False
            with col9:
                if st.button("Retract message"):
                    st.success("Message retracted")
                    st.session_state.prev_message_was_toxic = False
                    
    for i in st.session_state.combined_chat[-5:]:
        st.write(i+"\n")
        print(i)

##################################### Runner #########################################################################

if __name__ == "__main__":
        # ===================== Set page config and background =======================
    # Main panel setup
    # Set website details
    st.set_page_config(page_title ="Project Peace", 
                       page_icon=':desktop_computer:', 
                       layout='centered')
    """## Project Peace"""
    with st.expander("About"):
        st.write("This App was built for the Cohere 2023 hackathon, Project peace is built on top of Cohere's cutting Edge NLP models, and leveraged to help detect hate speech and detoxify them accross various languages")
        st.write("Find below a comprehensive list of supported languages.")
        st.dataframe(pd.read_csv("supported languages cohere.csv"))

    with st.sidebar:
        my_page = option_menu(
            menu_title=None,
            options = ["Receiver's Mode","Sender's Mode", "Combined"],
            icons=["arrow-down-right-circle-fill", "send", "send"],
        )
    if my_page == "Receiver's Mode":
        Receiver()
    elif my_page == "Sender's Mode":
        Sender()
    elif my_page == "Combined":
            Sender1()
            Sender2()


    else:
        st.write("Noting to see here use the side menu")