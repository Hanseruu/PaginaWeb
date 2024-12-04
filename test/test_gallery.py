import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()

    service = Service(r"C:\chromedriver-win64\chromedriver_131.0.6778.85.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    yield driver  # Le pasa el driver a las pruebas
    
    driver.quit()  # Cierra el navegador después de la prueba

def test_register_and_login(driver):
    # Abrir la página inicial
    driver.get("file:///C:/Users/Hans/Desktop/PaginaWeb/PaginaWeb/index.html")

    # Hacer clic en el botón de 'Sign up' para abrir el formulario de registro
    register_button = driver.find_element(By.ID, "registerBtn")
    register_button.click()

    # Espera a que el formulario de registro esté visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "register"))
    )

    # Llenar los campos de registro
    first_name = driver.find_element(By.ID, "first-name")
    last_name = driver.find_element(By.ID, "last-name")
    register_email = driver.find_element(By.ID, "register-email")
    register_password = driver.find_element(By.ID, "register-password")

    first_name.send_keys("Hansell")
    last_name.send_keys("Boni")
    register_email.send_keys("Hansell.boni@gmail.com")
    register_password.send_keys("123456")

    # Hacer clic en el botón de registro
    register_submit_button = driver.find_element(By.XPATH, '//input[@value="Register"]')
    register_submit_button.click()

    # Esperar a que el formulario de registro se oculte y el de login sea visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "login"))
    )

    # Iniciar sesión con las credenciales registradas
    login_email = driver.find_element(By.ID, "login-email")
    login_password = driver.find_element(By.ID, "login-password")

    login_email.send_keys("Hansell.boni@gmail.com")
    login_password.send_keys("123456")

    # Hacer clic en el botón de login
    submit_button = driver.find_element(By.XPATH, '//input[@value="Sign In"]')
    submit_button.click()

    # Verificar que después del login, se redirige a la página home.html
    WebDriverWait(driver, 10).until(EC.url_contains("home.html"))

    # Tomar una captura de pantalla para confirmar que estamos en la página correcta
    driver.save_screenshot("home_page_after_login.png")

    # Verificar que la URL contiene "home.html", indicando que se ha redirigido correctamente
    assert "home.html" in driver.current_url

    # Verificar galería de arte
    driver.save_screenshot("gallery_home.png")

    # Asegurarse de que el botón flotante "+" esté presente y clickeable
    floating_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, "floating-btn"))
    )

    floating_button.click()  # Clic en el botón flotante para mostrar los botones de subida

    # Esperar hasta que el contenedor de subida sea visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "upload-container"))
    )

    # Verifica si el contenedor de subida es visible
    upload_container = driver.find_element(By.ID, "upload-container")
    assert upload_container.is_displayed()

    # Verificar que el botón de "Subir Imagen" esté visible y clickeable
    upload_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    assert upload_button.is_displayed()

    # Esperar un momento para asegurar que el archivo se haya cargado
    time.sleep(5)

    # Tomar captura antes de continuar
    driver.save_screenshot("before_wait.png")

    # Esperar para que el usuario vea la imagen cargada
    input("Presiona Enter para continuar después de que veas la imagen subida en la página...")

    # Tomar captura de la imagen subida
    driver.save_screenshot("image_uploaded.png")
    try:
        close_modal_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal .close"))
        )
        close_modal_button.click()
    except:
        pass

    # Hacer clic en el botón "Galería de Viajes" para redirigir a viajes.html
    gallery_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Galería de Viajes')]")
    gallery_button.click()

    # Verificar que la URL cambia a viajes.html
    WebDriverWait(driver, 5).until(EC.url_contains("viajes.html"))

    # Dar tiempo para que subas otra foto en la galería de viajes
    input("Presiona Enter cuando hayas subido una foto en la galería de viajes...")


    # Esperar a que el archivo se cargue
    time.sleep(5)
        
    # Espera para que el usuario vea la imagen cargada
    input("Presiona Enter para continuar después de que veas la imagen subida en la página...")

    # Tomar captura de la imagen subida
    driver.save_screenshot("image_uploaded_viajes.png")
    
    # Finalizar la prueba
    time.sleep(2)
    
    gallery_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Contacto')]")
    gallery_button.click()

    WebDriverWait(driver, 10).until(EC.url_contains("contacto.html"))

    author = driver.find_element(By.ID, "author")
    comment = driver.find_element(By.ID, "comment")

    author.send_keys("Hansell Boni")
    comment.send_keys("¡Este es un comentario de prueba!")

    # Hacer clic en el botón de "Enviar Comentario"
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    # Esperar 2 segundos para que el comentario se agregue y se vea
    time.sleep(2)

    # Verificar que el comentario y el autor aparezcan en la sección de comentarios
    comment_section = driver.find_element(By.ID, "commentsSection")

    # Buscar el comentario más reciente
    last_comment = comment_section.find_elements(By.CLASS_NAME, "comment-box")[-1]
    comment_author = last_comment.find_element(By.CLASS_NAME, "author").text
    comment_message = last_comment.find_element(By.CLASS_NAME, "message").text

    # Verificar si el nombre y el comentario son correctos
    assert comment_author == "Hansell Boni"
    assert comment_message == "¡Este es un comentario de prueba!"

    # Tomar una captura de pantalla para confirmar visualmente
    driver.save_screenshot("confirmation_comentario.png")

    # Finalizar la prueba
    time.sleep(2)