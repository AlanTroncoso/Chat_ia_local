import customtkinter as ctk
import ollama
import threading
import json
import os
import pyautogui
import time
import datetime

# 1. Configuración base de la interfaz
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
ventana = ctk.CTk()
ventana.geometry("450x550")
ventana.title("Mi Asistente IA")

archivo_perfil = 'perfil.json'

# 2. Lógica de Onboarding (Creación o lectura del perfil)
def configurar_perfil():
    if not os.path.exists(archivo_perfil):
        print("Primera vez iniciando... pidiendo datos.")
        
        # Ventanas emergentes para pedir los datos
        dialogo_nombre = ctk.CTkInputDialog(text="Bienvenido. ¿Cuál es tu nombre?", title="Configuración (1/4)")
        nombre = dialogo_nombre.get_input()
        
        dialogo_genero = ctk.CTkInputDialog(text="¿Cuál es tu género?", title="Configuración (2/4)")
        genero = dialogo_genero.get_input()
        
        dialogo_cumple = ctk.CTkInputDialog(text="¿Cuándo es tu cumpleaños?", title="Configuración (3/4)")
        cumple = dialogo_cumple.get_input()
        
        dialogo_ubicacion = ctk.CTkInputDialog(text="¿En qué ciudad y país estás?", title="Configuración (4/4)")
        ubicacion = dialogo_ubicacion.get_input()
        
        # Diccionario con validación básica por si dejas un campo en blanco
        nuevo_perfil = {
            "nombre": nombre if nombre else "Usuario",
            "genero": genero if genero else "no especificado",
            "cumpleaños": cumple if cumple else "desconocido",
            "ubicacion": ubicacion if ubicacion else "desconocida"
        }
        
        # Guarda físicamente el archivo en tu PC
        with open(archivo_perfil, 'w') as archivo:
            json.dump(nuevo_perfil, archivo)
            
        return nuevo_perfil
        
    else:
        # Si el archivo ya existe, lo lee silenciosamente
        print("Perfil encontrado. Cargando datos...")
        with open(archivo_perfil, 'r') as archivo:
            return json.load(archivo)

# Ejecutamos la validación del perfil
mi_perfil = configurar_perfil()

# 3. Construcción Dinámica del Prompt del Sistema
def generar_prompt_sistema():
    ahora = datetime.datetime.now()
    # Formateamos la hora en lenguaje natural para evitar que la IA alucine
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    fecha_hora_texto = f"las {ahora.strftime('%H:%M')} del {ahora.day} de {meses[ahora.month - 1]} de {ahora.year}"
    
    return f"""Eres mi asistente personal de IA integrado en mi PC local. 
Mi nombre es {mi_perfil['nombre']}, mi género es {mi_perfil['genero']}, mi cumpleaños es el {mi_perfil['cumpleaños']} y me encuentro en {mi_perfil['ubicacion']}.

CONTEXTO DINÁMICO (TIEMPO REAL):
En este momento exacto son {fecha_hora_texto}. Utiliza este dato de forma obligatoria si te pregunto la hora, la fecha, o si me pides calcular cuánto falta para un evento en mi zona horaria.

Dirígete a mí por mi nombre de forma amigable y profesional. No me preguntes mis datos personales porque ya los sabes."""

# Iniciamos el historial del chat inyectando las instrucciones maestras
historial_chat = [{'role': 'system', 'content': generar_prompt_sistema()}]

# 4. Elementos de la interfaz gráfica
caja_chat = ctk.CTkTextbox(ventana, width=410, height=450, state="disabled", wrap="word")
caja_chat.pack(pady=10)

def procesar_mensaje():
    mensaje_usuario = entrada_texto.get()
    
    if not mensaje_usuario:
        return
        
    # Mostrar el mensaje del usuario en la UI
    caja_chat.configure(state="normal")
    caja_chat.insert("end", f"Tú: {mensaje_usuario}\n\n")
    caja_chat.configure(state="disabled")
    
    entrada_texto.delete(0, "end") 

    def llamar_ia():
        try:
            # Filtro rápido para detectar intenciones de abrir programas
            mensaje_min = mensaje_usuario.lower()
            es_orden_abrir = any(palabra in mensaje_min for palabra in ["abre ", "abrir ", "inicia ", "iniciar ", "ejecuta "])

            if es_orden_abrir:
                # --- MODO 1: ABRIR APLICACIONES ---
                caja_chat.configure(state="normal")
                caja_chat.insert("end", "IA está analizando el comando...\n")
                caja_chat.configure(state="disabled")
                
                prompt_extractor = f"""
                Extrae el nombre exacto de la aplicación que el usuario quiere abrir del siguiente texto: "{mensaje_usuario}".
                REGLAS ESTRICTAS:
                1. Devuelve la palabra EXACTAMENTE como la escribió el usuario.
                2. NO corrijas la ortografía.
                3. NO intentes adivinar el nombre real del programa.
                4. NO añadas palabras extra, saludos ni explicaciones.
                Respuesta esperada: Solo el nombre crudo de la app.
                """
                analisis = ollama.chat(model='phi3', messages=[{'role': 'user', 'content': prompt_extractor}])
                app_extraida = analisis['message']['content'].strip().replace(".", "").replace('"', '').replace("'", "")

                caja_chat.configure(state="normal")
                caja_chat.delete("end-2l", "end-1l") 
                caja_chat.insert("end", f"IA: Entendido, buscando y abriendo '{app_extraida}'...\n\n")
                caja_chat.see("end")
                caja_chat.configure(state="disabled")
                
                # Ejecución en Windows
                pyautogui.press("win") 
                time.sleep(0.5)        
                pyautogui.write(app_extraida) 
                time.sleep(0.5)
                pyautogui.press("enter")   
                
                # Actualización de memoria
                historial_chat.append({'role': 'user', 'content': mensaje_usuario})
                historial_chat.append({'role': 'assistant', 'content': f"Acabo de abrir la aplicación {app_extraida} con éxito."})
                
            else:
                # --- MODO 2: CHARLA NORMAL CON TIEMPO DINÁMICO ---
                caja_chat.configure(state="normal")
                caja_chat.insert("end", "IA está escribiendo...\n")
                caja_chat.configure(state="disabled")
                
                # Actualizamos el reloj y contexto de la IA justo antes de que procese el mensaje
                historial_chat[0]['content'] = generar_prompt_sistema()
                
                historial_chat.append({'role': 'user', 'content': mensaje_usuario})
                
                respuesta = ollama.chat(model='phi3', messages=historial_chat)
                texto_ia = respuesta['message']['content']
                
                historial_chat.append({'role': 'assistant', 'content': texto_ia})
                
                caja_chat.configure(state="normal")
                caja_chat.delete("end-2l", "end-1l") 
                caja_chat.insert("end", f"IA: {texto_ia}\n\n")
                caja_chat.see("end") 
                caja_chat.configure(state="disabled")
                
        except Exception as e:
            caja_chat.configure(state="normal")
            caja_chat.insert("end", "[Error de conexión o ejecución]\n\n")
            caja_chat.configure(state="disabled")

    # Ejecutar la IA en un hilo secundario
    hilo_ia = threading.Thread(target=llamar_ia)
    hilo_ia.start()

# Caja de texto inferior y botón
entrada_texto = ctk.CTkEntry(ventana, width=300, placeholder_text="Escribe un comando aquí...")
entrada_texto.pack(side="left", padx=(20, 10), pady=10)
entrada_texto.bind("<Return>", lambda event: procesar_mensaje())

boton_enviar = ctk.CTkButton(ventana, text="Enviar", width=90, command=procesar_mensaje)
boton_enviar.pack(side="right", padx=(0, 20), pady=10)

# Lanzar la aplicación
ventana.mainloop()