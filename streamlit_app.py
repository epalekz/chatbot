import streamlit as st
from openai import OpenAI
import requests
import base64
from io import BytesIO
import json

url = "https://jamtools.co/api/submit"

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = [
        {   'role':'system', 
            'content':"""
                Actua como un entrevistador entendiendo el slang de Colombia.
                Utiliza el humor y el slang de Colombia en tus preguntas.
                Haz tus preguntas de manera informal y amigable.
                Muestra empatia en tus interacciones y no hagas preguntas ofensivas.
                Realiza preguntas de seguimiento en caso de que la respuesta no sea clara o sea demasiado corta.                
                Primero saluda al usuario y preguntale como esta.
                Luego continua con la entrevista.                
                Responde de manera corta y muy conversacional y amigable.        
                Puedes hacer las preguntas en cualquier orden y no puedes repetir las preguntas.
                Puedes utilizar algunas de las siguientes preguntas y algunas variantes sin cambiar el contexto:
                Preguntas:
                    -Valoración y Reconocimiento:
                    ¿Te has sentido valorado en los proyectos donde has trabajado?
                    ¿Crees que tus ideas y propuestas son apreciadas en los proyectos?
                    ¿Consideras que se valoran tus habilidades y capacidades en los proyectos donde participas?
                    -Cambio de proyecto o cambio de cliente:
                    ¿Qué cambiarías de la cultura de trabajo de tu cliente o la empresa donde trabajas?
                    ¿Qué aspectos te gustarían modificar de tu proyecto actual o de tu último proyecto?
                    ¿Te gustaría cambiar de cliente o empresa? ¿Por qué?
                    ¿Crees que puedes obtener mayores beneficios (mejores oportunidades para crecer) trabajando con otro cliente?
                    ¿Con qué frecuencia te gustaría cambiar de cliente?
                    -Conexiones y Relaciones en los Proyectos:
                    ¿Has tenido la oportunidad de conectar con otras personas en tus proyectos?
                    ¿Te llevas bien con los stakeholders de tus clientes? ¿Has tenido algún problema con ellos?
                    ¿Consideras que alguien es o fue un obstáculo en tu proyecto más reciente? ¿Por qué?
                    -Satisfacción con el Cliente y el Proyecto:
                    ¿Con qué cliente te gustaría trabajar y por qué?
                    ¿Consideras útiles las reuniones con tu cliente?
                    ¿Disfrutas de tu proyecto a diario?
                    ¿Sientes que aprendes y te desarrollas en tu proyecto o prefieres un desafío mayor?
                    ¿Sientes que estás creciendo como profesional en tu proyecto actual?
                    ¿Qué es lo que menos te gusta de trabajar para un cliente?
                    -Balance de Vida y Trabajo:
                    ¿Sientes que tienes un buen equilibrio entre vida personal y trabajo en tu proyecto actual o en el último proyecto donde participaste?
                    ¿Cuántas horas diarias crees que le dedicas a tu proyecto?
                    ¿Crees que le dedicas más tiempo del que deberías a tu cliente?
                    ¿Te gustaría tener más tiempo para tus tareas profesionales o personales (desarrollo, cursos, talleres, hobbies)?
                    -Trato y Discriminación:
                    ¿En alguna ocasión te has sentido agredido verbalmente por algún cliente?
                    ¿Has sentido alguna vez un trato diferente por parte de tus clientes por ser de LATAM?
                    ¿Alguna vez has experimentado algún tipo de discriminación trabajando con un cliente?                
            """}
    ]

# Show title and description
st.title("🤖 ChatBot with Text-to-Speech")
st.write(
    "Description of the chatbot..."
    "To use this app, you need to provide an OpenAI API key and an ElevenLabs API key."
)

# Get OpenAI API key
openai_api_key = st.text_input("OpenAI API Key", type="password")
elevenlabs_api_key = st.text_input("ElevenLabs API Key", type="password")

if not openai_api_key or not elevenlabs_api_key:
    st.info("Please add your OpenAI and ElevenLabs API keys to continue.", icon="🗝️")
else:
    # Create an OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # Function to generate speech using ElevenLabs API
    def generate_speech(text, voice_id="IOyj8WtBHdke2FjQgGAr"): # voice_id="pMsXgVXv3BLzUgSXRplE"): # voice_id="21m00Tcm4TlvDq8ikWAM"):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": elevenlabs_api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        response = requests.post(url, json=data, headers=headers)
        return response.content
    
    # Function to generate speech summary using ChatGPT
    def generate_summary(text, voice_id="IOyj8WtBHdke2FjQgGAr"): # voice_id="pMsXgVXv3BLzUgSXRplE"): # voice_id="21m00Tcm4TlvDq8ikWAM"):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": elevenlabs_api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        response = requests.post(url, json=data, headers=headers)
        return response.content

    st.write("Hola. Soy el chatbot Epami, gracias por tomarte el tiempo para realizar esta entrevista. Vamos a comenzar. No estas obligado a responder las preguntas que no quieras, simplemente puedes decirme que pasemos a la siguiente. Si alguna pregunta no se entiende, puedes pedirme que la repite. Vamos a comenzar.")
    
    # Display existing chat messages
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                #VOICE if message["role"] == "assistant":
                    #VOICE audio = generate_speech(message["content"])
                    #VOICE st.audio(audio, format="audio/mp3", autoplay=False)

    # Chat input
    if prompt := st.chat_input(""):
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
            #VOICE audio = generate_speech(assistant_response)
            #VOICE st.audio(audio, format="audio/mp3",autoplay=True)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        
# Only show the "Clear Conversation" button if there's more than just the system message
# It checks if there's more than one message in the conversation (the first message is always the system message).
# If there are additional messages, it displays the "Clear Conversation" button.

if len(st.session_state.messages) > 1:
    if st.button("Terminar Entrevista",type="primary"):
        full_messages =  st.session_state.messages.copy()        
        full_messages.append({
            "role":"system", 
            "content":"crea un resumen de la entrevista en un maximo aproximado de 200 caracteres. Determinando si es positivo o negativo con una escala del 0 al 1 donde zero es totalmente negativo y 1 es totalmente positivo."
            })
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=full_messages,
            temperature=0.4,
        )
        st.title("Analyzando entrevista...")
        payload = json.dumps({
            "link_id": "P0mH7",
            "name": "Epami",
            "comment": response.choices[0].message.content
            })
        headers = {'Content-Type': 'application/json'}
        responseJamtools = requests.request("POST", url, headers=headers, data=payload)
        # Convertir la respuesta a un diccionario de Python
        response_json = json.loads(responseJamtools.text)
        # Acceder al valor de "success"
        success = response_json['success']
        # Validación y mensaje
        if success:
            st.title(":blue[El resumen de la entrevista fue exitoso.]")
        else:
            st.title(":red[El resumen de la entrevista no fue exitoso.]")
        st.session_state.messages = [st.session_state.messages[0]]  # Keep only the system message
        st.rerun()
