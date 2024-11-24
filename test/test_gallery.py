import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()

    service = Service(r"C:\chromedriver-win64\chromedriver_131.0.6778.85.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    yield driver  # Le pasa el driver a las pruebas
    
    driver.quit()  # Cierra el navegador después de la prueba

# Prueba principal
def test_homepage(driver):
    driver.get("file:///C:/Users/Hans/Desktop/PaginaWeb/PaginaWeb/index.html")

    # Esperar hasta que el formulario de login esté visible
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "login"))
    )

    # Simular el registro para que los datos estén en localStorage
    driver.execute_script(""" 
        localStorage.setItem('firstName', 'Test');
        localStorage.setItem('lastName', 'User');
        localStorage.setItem('email', 'testuser@example.com');
        localStorage.setItem('password', 'testpassword123');
    """)

    login_email = driver.find_element(By.ID, "login-email")
    login_password = driver.find_element(By.ID, "login-password")
    
    # Completar el formulario de login
    login_email.send_keys("testuser@example.com")
    login_password.send_keys("testpassword123")
    driver.save_screenshot("login_informacion.png")

    # Hacer clic en el botón de login
    submit_button = driver.find_element(By.XPATH, '//input[@value="Sign In"]')
    submit_button.click()
    driver.save_screenshot("login_exitoso.png")

    # Manejar posibles alertas (si la autenticación falla)
    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = Alert(driver)
        alert.accept()  # Cierra la alerta de "Usuario o contraseña incorrectos"
    except:
        pass  # Si no hay alerta, continúa

    # Esperar a que se redirija a la página "home.html"
    WebDriverWait(driver, 30).until(EC.url_contains("home.html"))
    
    assert "home.html" in driver.current_url

    assert driver.title == "Galería de Arte"

    gallery_images = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".gallery-item img"))
    )

    # Verificar que hay imágenes en la galería
    assert len(gallery_images) > 0

    # Hacer clic en la primera imagen para abrir el modal
    gallery_images[0].click()

    # Esperar hasta que el modal esté visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "gallery-modal"))
    )
    driver.save_screenshot("homepage_photozoom.png")

    # Verificar que el modal contiene la imagen correcta
    modal_image = driver.find_element(By.ID, "modal-img")
    assert modal_image.get_attribute("src") == gallery_images[0].get_attribute("src")
    driver.save_screenshot("gallery_images.png")

    #  simular el clic en el botón de registro y tomar una captura de pantalla de la página de registro ---
    
    # Regresar a la página de inicio (index.html) antes de hacer clic en el registro
    driver.get("file:///C:/Users/Hans/Desktop/PaginaWeb/PaginaWeb/index.html")
    
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "login"))
    )
    
    register_button = driver.find_element(By.ID, "registerBtn")
    register_button.click()

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "register"))
    )

    driver.save_screenshot("registration_page.png")

    assert driver.title == "Login & Registro"  
