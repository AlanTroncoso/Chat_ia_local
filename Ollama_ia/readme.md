# Asistente IA Local Autónomo (Arquitectura de Agentes & Function Calling)

Resumen del Proyecto
Este proyecto es un asistente personal de inteligencia artificial 100% local, diseñado bajo una arquitectura modular de agentes autónomos. El sistema abandona los enrutadores basados en expresiones regulares frágiles y utiliza *Function Calling (Llamadas a Herramientas)* nativo mediante *Qwen 2.5 (7B)* y procesamiento de voz con *Whisper*, permitiendo una interacción fluida, natural y libre de alucinaciones operativas.

Características Principales
1. Capa de Escucha (STT Local): Transcripción de voz a texto en tiempo real utilizando OpenAI Whisper, optimizado para ejecutarse de manera local y con un umbral de pausa adaptado para el habla natural.
2. Razonamiento y Function Calling: Uso de *Qwen 2.5 (7B)* a través de Ollama, aprovechando su soporte nativo para evaluar intenciones del usuario y extraer automáticamente argumentos estructurados para ejecutar código en Python.
3. Persistencia y Memoria de Contexto:** Mantiene un historial de conversación dinámico y gestiona bases de datos locales (`calendario.json`) para la administración de eventos.
4. Automatización del Sistema Operativo (RPA):** Capacidad de interactuar con Windows mediante `pyautogui` para la apertura dinámica de software y utilidades del sistema.
5. Procesamiento de Lenguaje Natural Temporal:** Integración con `dateparser` para interpretar expresiones de tiempo relativas (ej: "mañana", "el próximo lunes") y calcular fechas exactas en formato ISO.

---
# Requisitos Previos

Antes de clonar o ejecutar el proyecto en tu equipo, asegúrate de contar con lo siguiente:
1. Python (versión 3.10 o superior)** instalado y añadido a las variables de entorno.
2. Ollama instalado en tu sistema operativo para la gestión de modelos locales.
3. Modelo de IA configurado:** Abre tu terminal y descarga el modelo optimizado para *Function Calling*:
   ```bash
   ollama pull qwen2.5:7b
# Librerías y Dependencias

El proyecto requiere las siguientes librerías de Python para el procesamiento de audio, IA y automatización:

Bash
pip install ollama openai-whisper SpeechRecognition pyautogui dateparser soundfile
Desglose de Tecnologías:
ollama: Comunicación directa con el servidor local de modelos de IA.

openai-whisper & SpeechRecognition: Motor de conversión de voz a texto (STT).

soundfile: Librería auxiliar de decodificación de audio para Whisper.

pyautogui: Automatización de interfaz de usuario para el control del sistema operativo.

dateparser: Análisis y conversión avanzada de fechas en lenguaje natural.

json & os & unicodedata: Persistencia de datos, control del sistema y normalización de textos.

Roadmap (Próximos Pasos)
Capa de Síntesis de Voz (TTS): Integración de motores de voz locales (como Kokoro u Ollama TTS) para que el asistente responda de manera hablada.

Expansión de Herramientas (Tools): Incorporación de módulos para consulta de clima, control multimedia y automatización avanzada de archivos locales para el equipo de desarrollo.

Créditos y Autoría
Desarrollo y Arquitectura: Creado por un estudiante de Ingeniería Civil Informática, enfocado en el diseño de arquitecturas desacopladas, patrones de agentes autónomos y optimización de flujos de desarrollo en equipo.
