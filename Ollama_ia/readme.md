**# Asistente IA Local con Interfaz Gráfica y Orquestador**



**#Resumen de en qué consiste actualmente**

Este proyecto es una aplicación de escritorio desarrollada en Python que actúa como un asistente personal de Inteligencia Artificial 100% local. Funciona mediante un enrutador híbrido que combina la velocidad del código tradicional de Python con las capacidades de procesamiento de lenguaje natural de un modelo local (Phi-3 a través de Ollama). 



**#Actualmente, la aplicación permite:**

1. Mantener una interfaz gráfica moderna, rápida y en modo oscuro (CustomTkinter) que no se congela gracias al uso de hilos (\*threading\*).

2. Realizar un proceso de \*Onboarding\* automático en el primer inicio para almacenar los datos personales y de ubicación del usuario en un archivo local (`perfil.json`).

3. Inyectar contexto dinámico en tiempo real (fecha, hora exacta y ubicación) para otorgarle consciencia espacial y temporal a la IA.

4. Automatizar el sistema operativo (RPA con PyAutoGUI) para buscar y abrir aplicaciones nativas de Windows de manera fluida.

5. Mantener una memoria conversacional a corto plazo (\*historial de chat\*) y responder preguntas basadas en razonamiento local (como cálculos de tiempo).




**#Qué se tiene que instalar antes de ejecutar**

Para que este software funcione correctamente en tu equipo, debes tener instalados los siguientes componentes previos:



1. Python (versión 3.x recomendada): Asegúrate de tenerlo instalado y añadido a las variables de entorno de tu sistema operativo.

2. Ollama:Debes descargar e instalar Ollama desde su sitio oficial para gestionar modelos locales en tu PC.

3. Descargar el modelo baseAbre tu terminal y descarga el modelo Phi-3 ejecutando el siguiente comando:

-ollama run phi3



**#Librerías que se ocuparon**

El proyecto hace uso de librerías nativas de Python y paquetes de terceros que optimizan la interfaz y la ejecución de tareas. Para instalarlas todas de una vez, puedes usar el gestor de paquetes ejecutando el siguiente comando en tu terminal:



-pip install customtkinter ollama pyautogui

El desglose de librerías utilizadas es el siguiente:



customtkinter: Para la construcción de la interfaz gráfica de usuario (GUI) moderna y adaptable.



ollama: Librería oficial para la comunicación directa entre Python y el modelo local de IA.



pyautogui: Utilizada para la automatización de la interfaz del sistema operativo (RPA) en la apertura de aplicaciones.



threading: Librería nativa de Python para manejar la ejecución de procesos en segundo plano y evitar bloqueos en la interfaz gráfica.



json y os: Librerías nativas para la gestión, lectura y persistencia de datos locales del perfil de usuario.



datetime: Librería nativa para la obtención y sincronización del reloj del sistema.



**#Roadmap (Próximos Pasos)**

1. Integración de Web Scraping: Permitir que el asistente realice búsquedas en internet en tiempo real para consultas de actualidad.

2. Comandos de Voz: Lograr que reconozca la voz para los comandos.



**#Créditos y herramientas utilizadas**

Desarrollo y Arquitectura: Creado por un estudiante de Ingeniería Civil Informática, encargado del diseño lógico, el enrutador híbrido de intenciones y la integración de sistemas operativos.



Asistencia Técnica: Desarrollado con el apoyo de IA generativa utilizada como herramienta de consulta para optimizar la sintaxis de Python, estructurar componentes de la interfaz gráfica y resolver incidencias de alucinación de contexto mediante ingeniería de prompts.

