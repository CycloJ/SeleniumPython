import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def configurar_navegador():
    """
    Configura el navegador Chrome utilizando WebDriver Manager para manejar 
    automáticamente la instalación de ChromeDriver.
    
    Returns:
        webdriver.Chrome: Instancia del controlador del navegador Chrome.
    """
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def iniciar_sesion(driver, username, password):
    """
    Inicia sesión en Twitter con las credenciales proporcionadas.
    
    Argumentos:
        driver (webdriver.Chrome): Instancia del controlador del navegador.
        username (str): Nombre de usuario o correo electrónico de Twitter.
        password (str): Contraseña de Twitter.
    """
    driver.get("https://twitter.com/login")
    try:
        # Espera que los campos de usuario y contraseña estén disponibles
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))
        user_input = driver.find_element(By.NAME, "text")
        user_input.send_keys(username)
        user_input.send_keys(Keys.RETURN)

        # Espera a que aparezca el campo de contraseña y la ingresa
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        pass_input = driver.find_element(By.NAME, "password")
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.RETURN)
        
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        driver.quit()

def extraer_tweets(driver, cuenta):
    """
    Extrae tweets recientes de la cuenta de Twitter especificada.

    Argumentoss:
        driver (webdriver.Chrome): Instancia del controlador del navegador.
        cuenta (str): Nombre de usuario de Twitter (sin @) de la cuenta de la cual extraer tweets.

    Returns:
        list: Lista de diccionarios que contienen información de los tweets extraídos.
    """
    driver.get(f"https://twitter.com/{cuenta}")
    tweets = []

    while len(tweets) < 20:  # Ajusta el número de tweets que quieres extraer
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Espera para cargar nuevos tweets

        # Extraer elementos de tweet
        tweet_elements = driver.find_elements(By.XPATH, '//article[@role="article"]')
        
        for tweet in tweet_elements:
            try:
                # Extraer los detalles del tweet, junto con un aviso de error
                texto = tweet.find_element(By.XPATH, './/div[2]//div[2]//div[1]').text
                fecha = tweet.find_element(By.XPATH, './/time').get_attribute('datetime')
                retweets = tweet.find_element(By.XPATH, './/div[2]//div[2]//div[2]//div[1]//div[1]').text
                likes = tweet.find_element(By.XPATH, './/div[2]//div[2]//div[2]//div[1]//div[2]').text
                url = tweet.find_element(By.XPATH, './/a').get_attribute('href')
                tweets.append({"Texto": texto, "Fecha": fecha, "Retweets": retweets, "Likes": likes, "URL": url})
            except Exception as e:
                print(f"Error al extraer información del tweet: {e}")
                continue

    return tweets

def guardar_en_csv(tweets, nombre_archivo="tweets.csv"):
    """
    Guarda la lista de tweets en un archivo CSV.

    Argumentos:
        tweets (list): Lista de diccionarios con la información de los tweets.
        nombre_archivo (str): Nombre del archivo CSV de salida (por defecto 'tweets.csv').
    """
    df = pd.DataFrame(tweets)
    df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
    print(f"Datos guardados en {nombre_archivo}")

def main():
    """
    Esta es la funcion principal que coordina la ejecución del script:
    - Carga las credenciales de Twitter desde variables de entorno.
    - Configura el navegador y realiza el inicio de sesión.
    - Extrae los tweets de la cuenta especificada (puede ser cualquier cuenta) y guarda los resultados en un CSV.
    """
    # Cargar las variables de entorno
    usuario = os.getenv("TWITTER_USERNAME")
    contrasena = os.getenv("TWITTER_PASSWORD")

    # Imprimir las credenciales para depuración (simplemente una guia para mi, porque hubieron errores ambiguos durante el desarrollo)
    print(f"Usuario: {usuario}")
    print(f"Contraseña: {contrasena}")

    # Verificación de las credenciales
    if not usuario or not contrasena:  # Verifica si alguna variable esta vacía
        print("Error: Credenciales de Twitter no configuradas correctamente. Revisa las variables de entorno.")
        exit(1)

    cuenta = "ABCDigital"  # En mi caso,elegi guardar los tweets de ABC Color en su twitter.

    driver = configurar_navegador()
    iniciar_sesion(driver, usuario, contrasena)
    tweets = extraer_tweets(driver, cuenta)
    guardar_en_csv(tweets)
    driver.quit()

if __name__ == "__main__":
    main()
