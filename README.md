  Instrucciones para la Ejecución del Script de Extracción de Tweets
Este documento proporciona las instrucciones detalladas para ejecutar el script de Python diseñado para extraer tweets de una cuenta específica de Twitter utilizando Selenium. El script almacena la información extraída en un archivo CSV para su posterior análisis.

  Requisitos Previos:
Tener instalado Python 3.7 o una versión superior.
Contar con una instalación actualizada de Google Chrome.
Poseer credenciales válidas de Twitter (nombre de usuario o correo electrónico y contraseña).

  Instalación de Dependencias:
Para ejecutar el script correctamente, se requiere la instalación de ciertas dependencias de Python. A continuación, se detallan los pasos necesarios para configurar el entorno y realizar dicha instalación:

  Clonación del Repositorio:
Clone el repositorio en su máquina local utilizando el siguiente comando:
    git clone https://github.com/tu_usuario/TwitterScraper.git
    cd TwitterScraper
    
Creación y Activación del Entorno Virtual:
Es recomendable crear un entorno virtual para aislar las dependencias del proyecto. Para ello, siga los pasos correspondientes a su sistema operativo:
En Windows:
    python -m venv venv
    .\venv\Scripts\activate

Instalación de Dependencias Requeridas:
Con el entorno virtual activado, instale las dependencias necesarias ejecutando el siguiente comando:
    pip install -r requirements.txt
Asegúrese de que el archivo requirements.txt contenga las siguientes bibliotecas:

selenium
webdriver_manager
pandas
python-dotenv

  Configuración de las Credenciales de Twitter:
El script requiere credenciales de Twitter para iniciar sesión y extraer tweets. Configure las credenciales como variables de entorno siguiendo las instrucciones a continuación:

En Windows:
Abra el "Símbolo del sistema" (CMD).
  Ejecute los siguientes comandos:

    setx TWITTER_USERNAME "tu_usuario_o_correo"
    setx TWITTER_PASSWORD "tu_contraseña"
Cierre y vuelva a abrir la terminal de VSCode para aplicar los cambios.

  Ejecución del Script:
Asegúrese de que el entorno virtual esté activado.

  Ejecute el script mediante el siguiente comando:
    python twitter_scraper.py

  Resultados de la Ejecución:
Al ejecutar el script, se abrirá automáticamente una ventana de Google Chrome que procederá a iniciar sesión en Twitter, 
extraer los tweets recientes de la cuenta especificada y guardar los resultados en un archivo CSV denominado tweets.csv. 
Este archivo se generará en el mismo directorio del script.
