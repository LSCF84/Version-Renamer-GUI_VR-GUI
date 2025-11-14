
<div align="center">
   
# Version Renamer GUI (Renombrador de Versiones con Interfaz Gráfica)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Windows](https://img.shields.io/badge/Platform-Windows%2010%2B-success)](https://www.microsoft.com/windows)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5%2B-orange)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)


</div>

## 🌟 Resumen del Proyecto

Esta es una aplicación de escritorio desarrollada en **Python** utilizando **Tkinter** para proporcionar una solución **intuitiva y segura** para renombrar archivos dentro de un directorio, aplicando un sistema de versionado automático.

El objetivo principal es ayudar a desarrolladores y usuarios a gestionar el historial de versiones de sus *scripts* (`.py` en este caso) basados en la fecha de modificación, asegurando que cada archivo antiguo reciba un nuevo nombre único antes de guardar una versión más reciente.

---

## ✨ Características Principales

* **Interfaz Gráfica (GUI):** Desarrollada con Tkinter para una experiencia de usuario sencilla.
* **Versionado Automático:** Renombra archivos en orden de antigüedad (usando la fecha de modificación) asignando versiones crecientes (ej: `nombre_base_v.1.0.py`, `nombre_base_v.1.1.py`, etc.).
* **Gestión de Archivos:** Permite seleccionar el directorio de trabajo y cambiar el nombre base para los nuevos archivos.
* **Seguridad y Exclusión:**
    * Excluye automáticamente el *script* de renombrado en ejecución (`comprobador.py`) para evitar errores.
    * Detecta conflictos de nombres y asigna la siguiente versión disponible.
* **Previsualización:** Muestra una vista previa de los nuevos nombres de archivo antes de ejecutar el renombrado final.
* **Selección Múltiple:** Control granular sobre qué archivos deben ser renombrados mediante *checkboxes* en la lista.

## Tecnologías Utilizadas

| Tecnología | Propósito |
| :--- | :--- |
| **Python** | Lenguaje de programación principal. |
| **Tkinter** | Creación de la Interfaz Gráfica de Usuario (GUI). |
| **`os` & `glob`** | Manejo del sistema de archivos, directorios y obtención de metadatos (fechas de modificación). |
| **`datetime`** | Formateo y gestión de las fechas de modificación. |

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.8 o superior
- Windows 10/11
- Permisos de administrador (recomendado)
---

## Instalación

1.  **Clona el repositorio**
    ```bash
    git clone https://github.com/LSCF84/Renamer-GUI.git
   cd Renamer-GUI
    ```
2.  **Instala dependencias**
    ```bash
    pip install -r requirements.txt
    ```

### 2. Ejecución

Dado que solo utiliza librerías estándar de Python, no se requiere ninguna instalación de paquetes externa.

1.  Descarga o clona el archivo `comprobador.py` en tu máquina.
2.  Ejecuta el *script* desde tu terminal:

    ```bash
    python comprobador.py
    ```

### 3. Guía de Uso Rápido

1.  **Directorio:** Haz clic en **"Examinar"** o introduce la ruta donde se encuentran los archivos `.py` que deseas versionar.
2.  **Nombre Base:** Introduce el nombre que usarán tus archivos renombrados (ej: `proyecto-final`).
3.  **Actualizar Lista:** Haz clic en **"Actualizar Lista"** para cargar todos los archivos `.py` encontrados, ordenados por fecha de modificación (los más antiguos primero).
4.  **Selección:** Utiliza los *checkboxes* o los botones **"Seleccionar Todos" / "Deseleccionar Todos"** para elegir qué archivos serán procesados.

---

## 👨‍💻 Autor

**LSCF**

## ⚙️ Instalación y Dependencias

Para ejecutar este proyecto, necesitas Python 3.x

## 🤝 ¿Quieres contribuir?

¡Claro! Abre un Issue o un Pull Request. Usa la plantilla al crear un Issue.

---

⭐️ Si te sirvió, ¡dale una estrella al repositorio!
