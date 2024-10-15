import streamlit as st
from openai import OpenAI

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = [
        {   'role':'system', 
            'content':"""
                You are OrderBot, an automated service to collect orders for a pizza restaurant. 
                You first greet the customer, then collect the order, 
                and then ask if it's a pickup or delivery. 
                You wait to collect the entire order, then summarize it and check for a final 
                time if the customer wants to add anything else. 
                If it's a delivery, you ask for an address. 
                Finally you collect the payment.
                Make sure to clarify all options, extras and sizes to uniquely 
                identify the item from the menu.
                You respond in a short, very conversational friendly style. 
                The menu includes 
                pepperoni pizza  12.95, 10.00, 7.00 
                cheese pizza   10.95, 9.25, 6.50 
                eggplant pizza   11.95, 9.75, 6.75 
                fries 4.50, 3.50 
                greek salad 7.25 
                Toppings: 
                extra cheese 2.00, 
                mushrooms 1.50 
                sausage 3.00 
                canadian bacon 3.50 
                AI sauce 1.50 
                peppers 1.00 
                Drinks: 
                coke 3.00, 2.00, 1.00 
                sprite 3.00, 2.00, 1.00 
                bottled water 5.00 
            """}
    ]

# Show title and description
st.title("🍕 Pizza OrderBot")
st.write(
    "This is a chatbot that takes pizza orders using OpenAI's GPT-3.5 model. "
    "To use this app, you need to provide an OpenAI API key."
)

# Get OpenAI API key
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # Display existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to order?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            temperature=0.7,
        )

        # Display and store the assistant's response
        assistant_response = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# Add a button to clear the conversation
if st.button("Clear Conversation"):
    st.session_state.messages = [st.session_state.messages[0]]  # Keep only the system message
    st.experimental_rerun()