import speech_recognition as sr
import ollama
import warnings
import json
import os
import pyautogui
import time
import datetime
import dateparser

warnings.filterwarnings("ignore")

ARCHIVO_CALENDARIO = 'calendario.json'
MODELO = 'qwen2.5:7b'

# --- CAPA DE PERSISTENCIA Y CONTEXTO ---
def cargar_json(ruta, valor_por_defecto):
    if not os.path.exists(ruta):
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(valor_por_defecto, f, indent=4, ensure_ascii=False)
        return valor_por_defecto
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return valor_por_defecto

def guardar_json(ruta, datos):
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

# Inicializamos la memoria de Jarvis
PERSONALIDAD_JARVIS = {
    'role': 'system',
    'content': (
        "Eres Jarvis, un asistente autónomo e inteligente. Responde siempre en español. "
        "Sé educado, ingenioso y eficiente. Si el usuario te pide una acción que requiera "
        "una herramienta, ejecútala de inmediato sin rodeos."
    )
}
historial_conversacion = [PERSONALIDAD_JARVIS]

# --- CAPA 3: HERRAMIENTAS REALES (Python) ---

def abrir_aplicacion(nombre_app: str) -> str:
    print(f"\n[🔧 ACCIÓN PYTHON] -> Abriendo: '{nombre_app}'")
    try:
        pyautogui.press("win")
        time.sleep(0.4)
        pyautogui.write(nombre_app)
        time.sleep(0.4)
        pyautogui.press("enter")
        return f"Aplicación '{nombre_app}' ejecutada correctamente."
    except Exception as e:
        return f"Error al abrir la aplicación: {e}"

def leer_calendario() -> str:
    print(f"\n[🔧 ACCIÓN PYTHON] -> Consultando base de datos...")
    calendario = cargar_json(ARCHIVO_CALENDARIO, [])
    if not calendario:
        return "Tu agenda está completamente vacía, señor."
    
    respuesta = "Tienes los siguientes eventos en tu agenda:\n"
    for e in calendario:
        respuesta += f"- {e['fecha']}: {e['detalle']}\n"
    return respuesta

def agregar_evento(fecha: str, descripcion: str) -> str:
    print(f"\n[🔧 ACCIÓN PYTHON] -> Calculando fecha para: '{descripcion}'")
    hoy_str = datetime.datetime.now().strftime('%Y-%m-%d')
    
    fecha_calc = dateparser.parse(fecha, languages=['es'], settings={'PREFER_DATES_FROM': 'future'})
    fecha_iso = fecha_calc.strftime('%Y-%m-%d') if fecha_calc else hoy_str
    
    calendario = cargar_json(ARCHIVO_CALENDARIO, [])
    calendario.append({"fecha": fecha_iso, "detalle": descripcion})
    guardar_json(ARCHIVO_CALENDARIO, calendario)
    
    return f"Entendido, he agendado '{descripcion}' para el {fecha_iso}."

def eliminar_evento(palabra_clave: str) -> str:
    print(f"\n[🔧 ACCIÓN PYTHON] -> Buscando '{palabra_clave}' para eliminar...")
    calendario = cargar_json(ARCHIVO_CALENDARIO, [])
    cantidad_original = len(calendario)
    
    calendario_nuevo = [e for e in calendario if palabra_clave.lower() not in e["detalle"].lower()]
    
    if len(calendario_nuevo) < cantidad_original:
        guardar_json(ARCHIVO_CALENDARIO, calendario_nuevo)
        return f"Los eventos relacionados con '{palabra_clave}' han sido eliminados de la agenda."
    else:
        return f"No encontré ningún evento que coincida con '{palabra_clave}'."

def obtener_hora_actual() -> str:
    ahora = datetime.datetime.now()
    hora_formateada = ahora.strftime('%I:%M %p')
    print(f"\n[🔧 ACCIÓN PYTHON] -> Consultando reloj interno...")
    return f"Son las {hora_formateada}."

# MAPEO DE FUNCIONES REALES
HERRAMIENTAS_MAPA = {
    'abrir_aplicacion': abrir_aplicacion,
    'leer_calendario': leer_calendario,
    'agregar_evento': agregar_evento,
    'eliminar_evento': eliminar_evento,
    'obtener_hora_actual': obtener_hora_actual
}

# ESQUEMAS FORMALES JSON PARA OLLAMA
esquemas_herramientas = [
    {
        'type': 'function',
        'function': {
            'name': 'abrir_aplicacion',
            'description': 'Abre un software o aplicación instalada en el sistema operativo usando el buscador de Windows.',
            'parameters': {
                'type': 'object',
                'properties': {'nombre_app': {'type': 'string', 'description': 'Nombre de la aplicación (ej: notepad, chrome, calc)'}},
                'required': ['nombre_app']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'leer_calendario',
            'description': 'Lee y devuelve todos los eventos actuales en la agenda del usuario.',
            'parameters': {'type': 'object', 'properties': {}}
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'agregar_evento',
            'description': 'Agrega una nueva tarea o evento al calendario.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'fecha': {'type': 'string', 'description': 'Fecha expresada por el usuario (ej: mañana, el lunes, 25 de diciembre)'},
                    'descripcion': {'type': 'string', 'description': 'El detalle del evento (ej: cita médica, reunión de trabajo)'}
                },
                'required': ['fecha', 'descripcion']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'eliminar_evento',
            'description': 'Elimina eventos del calendario buscando una palabra clave.',
            'parameters': {
                'type': 'object',
                'properties': {'palabra_clave': {'type': 'string', 'description': 'Palabra clave del evento a borrar (ej: médico, dentista)'}},
                'required': ['palabra_clave']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'obtener_hora_actual',
            'description': 'Obtiene la hora y fecha actual del sistema operativo.',
            'parameters': {'type': 'object', 'properties': {}}
        }
    }
]

# --- CAPA 1: ESCUCHA (Whisper) ---

def escuchar_microfono() -> str:
    reconocedor = sr.Recognizer()
    reconocedor.pause_threshold = 2.0 
    
    with sr.Microphone() as fuente:
        print("\n[🎙️] Ajustando ruido... (1 seg)")
        reconocedor.adjust_for_ambient_noise(fuente, duration=1.0)
        print("[🎙️] Jarvis escuchando... (Puedes pausar al hablar)")
        try:
            audio = reconocedor.listen(fuente, timeout=5, phrase_time_limit=15)
            print("[⚙️] Transcribiendo con Whisper...")
            texto = reconocedor.recognize_whisper(audio, model="base", language="spanish").strip()
            print(f"✅ Tú: '{texto}'")
            return texto
        except Exception:
            return ""

# --- CAPA 2: PROCESAMIENTO (Qwen 2.5) ---

def procesar_con_ia(texto_usuario: str):
    if not texto_usuario:
        return
        
    print("[🧠] Qwen 2.5 analizando intención...")
    historial_conversacion.append({'role': 'user', 'content': texto_usuario})
    
    try:
        respuesta = ollama.chat(
            model=MODELO, 
            messages=historial_conversacion,
            tools=esquemas_herramientas
        )

        llamadas_herramientas = respuesta['message'].get('tool_calls')

        if llamadas_herramientas:
            # Añadimos la intención de usar herramientas al historial de Ollama
            historial_conversacion.append(respuesta['message'])
            
            for herramienta in llamadas_herramientas:
                nombre = herramienta['function']['name']
                args = herramienta['function']['arguments']
                
                # Forzar conversión a diccionario si viene en string JSON plano
                if isinstance(args, str):
                    args = json.loads(args)
                
                print(f"🤖 [RAZONAMIENTO] Ejecutando función: {nombre} | Parámetros: {args}")
                
                if nombre in HERRAMIENTAS_MAPA:
                    # Ejecución dinámica usando desempaquetado de argumentos (**args)
                    resultado_accion = HERRAMIENTAS_MAPA[nombre](**args)
                    print(f"✅ [RESULTADO]: {resultado_accion}")
                    
                    # Le enviamos el resultado de la función a Ollama para que construya la frase final
                    historial_conversacion.append({
                        'role': 'tool',
                        'content': resultado_accion,
                        'name': nombre
                    })
            
            # Segunda llamada para que la IA dé su confirmación hablada al usuario
            respuesta_final = ollama.chat(model=MODELO, messages=historial_conversacion)
            texto_final = respuesta_final['message']['content']
            print(f"🤖 [JARVIS]: {texto_final}")
            historial_conversacion.append({'role': 'assistant', 'content': texto_final})
            
        else:
            texto_final = respuesta['message']['content']
            print(f"🤖 [JARVIS]: {texto_final}")
            historial_conversacion.append({'role': 'assistant', 'content': texto_final})
            
    except Exception as e:
        print(f"❌ Error en procesamiento de IA: {e}")

# --- BUCLE PRINCIPAL ---

if __name__ == "__main__":
    print("=== NÚCLEO AUTÓNOMO INICIADO ===")
    print("Di 'apagar' para detener el sistema.")
    
    while True:
        comando_voz = escuchar_microfono()
        
        # Limpieza básica para el comando de apagado
        comando_limpio = comando_voz.lower().replace(".", "").strip()
        if comando_limpio in ["apagar", "salir", "terminar", "apágate"]:
            print("Apagando sistema...")
            break
            
        procesar_con_ia(comando_voz)
