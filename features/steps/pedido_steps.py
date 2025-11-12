from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import json

# Given steps
@given('que la API de bebidas está disponible')
def step_api_disponible(context):
    """Verificar que la API de bebidas responde"""
    try:
        response = requests.get('http://localhost:8000/menu')
        assert response.status_code == 200
        context.api_url = 'http://localhost:8000'
    except requests.exceptions.ConnectionError:
        context.api_url = 'http://api-bebidas:8000'  # Docker network name

@given('existe una bebida "{nombre}" en tamaño "{tamaño}" con precio {precio:f}')
def step_bebida_existe(context, nombre, tamaño, precio):
    """Crear bebida en la API"""
    data = {"name": nombre, "size": tamaño, "price": precio}
    response = requests.post(f'{context.api_url}/menu', json=data)
    assert response.status_code == 201

@given('NO existe una bebida llamada "{nombre}"')
def step_bebida_no_existe(context, nombre):
    """Verificar que la bebida no existe en el menú"""
    response = requests.get(f'{context.api_url}/menu')
    menu = response.json()
    bebida_existe = any(item['name'] == nombre for item in menu)
    assert not bebida_existe, f"La bebida {nombre} no debería existir"

@given('existe una bebida "{nombre}" solo en tamaño "{tamaño}"')
def step_bebida_tamaño_especifico(context, nombre, tamaño):
    """Verificar que la bebida existe solo en el tamaño especificado"""
    data = {"name": nombre, "size": tamaño, "price": 3.00}
    requests.post(f'{context.api_url}/menu', json=data)

@given('que estoy en la página de pedidos')
def step_en_pagina_pedidos(context):
    """Navegar a la página de pedidos"""
    try:
        context.driver.get('http://localhost:3000')  # React app
    except:
        context.driver.get('http://ui-pedidos:3000')  # Docker network

# When steps
@when('selecciono la bebida "{nombre}"')
def step_seleccionar_bebida(context, nombre):
    """Seleccionar bebida del menú"""
    wait = WebDriverWait(context.driver, 10)
    bebida_element = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{nombre}')]"))
    )
    bebida_element.click()

@when('selecciono el tamaño "{tamaño}"')
def step_seleccionar_tamaño(context, tamaño):
    """Seleccionar tamaño de la bebida"""
    wait = WebDriverWait(context.driver, 10)
    tamaño_element = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{tamaño}')]"))
    )
    tamaño_element.click()

@when('hago clic en "Realizar Pedido"')
def step_hacer_pedido(context):
    """Hacer clic en el botón de realizar pedido"""
    wait = WebDriverWait(context.driver, 10)
    boton_pedido = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Realizar Pedido')]"))
    )
    boton_pedido.click()

@when('intento pedir "{bebida}" en tamaño "{tamaño}"')
def step_intentar_pedido(context, bebida, tamaño):
    """Intentar realizar un pedido específico"""
    context.execute_steps(f'''
        Cuando selecciono la bebida "{bebida}"
        Y selecciono el tamaño "{tamaño}"
        Y hago clic en "Realizar Pedido"
    ''')

@when('hago un pedido de "{bebida}" en tamaño "{tamaño}"')
def step_hacer_pedido_especifico(context, bebida, tamaño):
    """Hacer un pedido específico"""
    context.execute_steps(f'''
        Cuando selecciono la bebida "{bebida}"
        Y selecciono el tamaño "{tamaño}"
        Y hago clic en "Realizar Pedido"
    ''')

@when('intento enviar el formulario sin nombre de bebida')
def step_formulario_vacio(context):
    """Intentar enviar formulario vacío"""
    wait = WebDriverWait(context.driver, 10)
    boton_pedido = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Realizar Pedido')]"))
    )
    context.boton_pedido = boton_pedido

# Then steps
@then('el pedido debe ser creado exitosamente')
def step_pedido_exitoso(context):
    """Verificar que el pedido fue creado exitosamente"""
    wait = WebDriverWait(context.driver, 10)
    success_message = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
    )
    assert success_message.is_displayed()

@then('debo ver el mensaje "{mensaje}"')
def step_verificar_mensaje(context, mensaje):
    """Verificar que aparece el mensaje esperado"""
    wait = WebDriverWait(context.driver, 10)
    message_element = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{mensaje}')]"))
    )
    assert message_element.is_displayed()

@then('el pedido debe aparecer en el historial con estado "{estado}"')
def step_verificar_estado_historial(context, estado):
    """Verificar el estado del pedido en el historial"""
    wait = WebDriverWait(context.driver, 10)
    estado_element = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{estado}')]"))
    )
    assert estado_element.is_displayed()

@then('el precio del pedido debe ser {precio:f}')
def step_verificar_precio(context, precio):
    """Verificar el precio del pedido"""
    wait = WebDriverWait(context.driver, 10)
    precio_element = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{precio}')]"))
    )
    assert precio_element.is_displayed()

@then('si la bebida existe en ese tamaño')
def step_si_bebida_existe(context):
    """Verificar si la bebida existe en el tamaño especificado"""
    # Esta es una condición, no una acción
    pass

@then('El pedido debe ser confirmado')
def step_pedido_confirmado(context):
    """Verificar que el pedido fue confirmado"""
    context.execute_steps('''
        Entonces el pedido debe ser creado exitosamente
    ''')

@then('el historial debe actualizarse automáticamente')
def step_historial_actualizado(context):
    """Verificar que el historial se actualizó"""
    wait = WebDriverWait(context.driver, 10)
    historial = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "historial-pedidos"))
    )
    assert historial.is_displayed()

@then('el pedido debe ser rechazado')
def step_pedido_rechazado(context):
    """Verificar que el pedido fue rechazado"""
    wait = WebDriverWait(context.driver, 10)
    error_element = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
    )
    assert error_element.is_displayed()

@then('debo ver el mensaje de error "{mensaje}"')
def step_verificar_mensaje_error(context, mensaje):
    """Verificar mensaje de error específico"""
    wait = WebDriverWait(context.driver, 10)
    error_element = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{mensaje}')]"))
    )
    assert error_element.is_displayed()

@then('el pedido debe tener estado "{estado}"')
def step_verificar_estado(context, estado):
    """Verificar el estado del pedido"""
    wait = WebDriverWait(context.driver, 10)
    estado_element = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{estado}')]"))
    )
    assert estado_element.is_displayed()

@then('debo ver "{mensaje}"')
def step_verificar_mensaje_generico(context, mensaje):
    """Verificar cualquier mensaje en pantalla"""
    wait = WebDriverWait(context.driver, 10)
    message_element = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{mensaje}')]"))
    )
    assert message_element.is_displayed()

@then('el botón de envío debe estar deshabilitado')
def step_boton_deshabilitado(context):
    """Verificar que el botón está deshabilitado"""
    assert not context.boton_pedido.is_enabled()

@then('debo ver un mensaje de validación')
def step_mensaje_validacion(context):
    """Verificar que aparece un mensaje de validación"""
    wait = WebDriverWait(context.driver, 10)
    validation_message = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "validation-message"))
    )
    assert validation_message.is_displayed()
