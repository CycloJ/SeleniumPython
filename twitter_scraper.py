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

# Configurar el navegador usando WebDriver Manager
def configurar_navegador():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Función para iniciar sesión en Twitter
def iniciar_sesion(driver, username, password):
    driver.get("https://twitter.com/login")
    try:
        # Espera que los campos de usuario y contraseña estén disponibles
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))
        user_input = driver.find_element(By.NAME, "text")
        user_input.send_keys(username)
        user_input.send_keys(Keys.RETURN)

        # Esperar y escribir la contraseña
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        pass_input = driver.find_element(By.NAME, "password")
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.RETURN)
        
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        driver.quit()

# Función para extraer tweets
def extraer_tweets(driver, cuenta):
    driver.get(f"https://twitter.com/{cuenta}")
    tweets = []

    while len(tweets) < 20:  # Ajusta el número de tweets que quieres extraer
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Esperar a que se carguen nuevos tweets

        # Extraer elementos de tweet
        tweet_elements = driver.find_elements(By.XPATH, '//article[@role="article"]')
        
        for tweet in tweet_elements:
            try:
                texto = tweet.find_element(By.XPATH, './/div[2]//div[2]//div[1]').text
                fecha = tweet.find_element(By.XPATH, './/time').get_attribute('datetime')
                retweets = tweet.find_element(By.XPATH, './/div[2]//div[2]//div[2]//div[1]//div[1]').text
                likes = tweet.find_element(By.XPATH, './/div[2]//div[2]//div[2]//div[1]//div[2]').text
                url = tweet.find_element(By.XPATH, './/a').get_attribute('href')
                tweets.append({"Texto": texto, "Fecha": fecha, "Retweets": retweets, "Likes": likes, "URL": url})
            except:
                continue

    return tweets

# Función para guardar en CSV
def guardar_en_csv(tweets, nombre_archivo="tweets.csv"):
    df = pd.DataFrame(tweets)
    df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
    print(f"Datos guardados en {nombre_archivo}")

# Función principal para ejecutar el script
def main():
    # Cargar las variables de entorno
    usuario = os.getenv("TWITTER_USERNAME")
    contrasena = os.getenv("TWITTER_PASSWORD")

    # Imprimir las credenciales para depuración
    print(f"Usuario: {usuario}")
    print(f"Contraseña: {contrasena}")

    # Verificación de las credenciales
    if not usuario or not contrasena:  # Verifica si alguna variable es None o vacía
        print("Error: Credenciales de Twitter no configuradas correctamente. Revisa las variables de entorno.")
        exit(1)

    cuenta = "ABCDigital"  # Cambia esto por el nombre de usuario de la cuenta que deseas extraer sin el @

    driver = configurar_navegador()
    iniciar_sesion(driver, usuario, contrasena)
    tweets = extraer_tweets(driver, cuenta)
    guardar_en_csv(tweets)
    driver.quit()

if __name__ == "__main__":
    main()
