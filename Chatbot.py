import streamlit as st
import groq


#VARIABLES
height_contenedor = 500
status_stream = True

#CHAT
modelos = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "meta-llama/llama-guard-4-12b"]
def pagina ():
    st.set_page_config(page_title="Jaimito",page_icon="👽")

    st.title("Jaimito IA")
    st.text("¿En que te puedo ayudar?")
    

    st.sidebar.title("Modelos disponibles")
    modelo_seleccionado = st.sidebar.selectbox("¿Que Modelo vas a usar?", options=modelos, index=0)
    return modelo_seleccionado

def usuario():
    clave_secreta = st.secrets["CLAVE_API"] 
    return groq.Groq(api_key= clave_secreta) 


#Esta funcion procesa el prompt del usuario dependiendo el modelo
def configurar_modelo(cliente,modelo,prompt):
    return cliente.chat.completions.create(
        model = modelo, 
        messages = [{"role": "user", "content": prompt}], 
        stream = status_stream
    )

def inicio():
    if "mensajes" not in st.session_state: #si no hay un mensaje
        st.session_state.mensajes = [] #guarda los mensajes del usuario

def actualizar_historial(rol,avatar,contenido): 
    st.session_state.mensajes.append({"role": rol,"content": contenido ,
                                      "avatar" : avatar
                                     })
    
def historial():   
    for i in st.session_state.mensajes:
        with st.chat_message(i["role"], avatar=i["avatar"]): 
            st.write(i["content"]) 
def area_chat():  
    contenedor = st.container(height=height_contenedor, border=True)
    #contenedor es el rectangulo en donde se muestra el codigo  
    with contenedor:  #se abre y se cierra de forma segura el contenedor
        historial()
    
def respuesta_chat(respuesta):
    respuesta_real = ""
    for frase in  respuesta:
        if frase.choices[0].delta.content: #cada vez que encuentra esas frases en el contenido, se agregan a la respuesta real 
            respuesta_real += frase.choices[0].delta.content 
            yield frase.choices[0].delta.content #se escribe de a poquito la respuesta
    return respuesta_real

def main():
    modelo_usuario = pagina()
    cliente_usuario = usuario() 
    inicio()

    area_chat()
    prompt_usuario = st.chat_input("Sin miedo que no muerdo: ")

    if prompt_usuario:
        actualizar_historial("user", "🧠",prompt_usuario) #escribe el usuario
        respuesta = configurar_modelo(cliente_usuario, modelo_usuario,prompt_usuario)

        if respuesta:
            with st.chat_message("assistant"):
                respuesta_chatbot = st.write_stream(respuesta_chat(respuesta))
                actualizar_historial("assistant", "🤓", respuesta_chatbot) #responde el Chat
                st.rerun() 

if __name__ == "__main__":

    main()
