# 📋 **Guía Completa para Ejecutar Todos los Tests - VirtualCoffee**

## 🚀 **Preparación del Entorno**

### 1. Asegurar que todos los servicios estén funcionando

```powershell
# Navegar al directorio principal
cd "C:\Users\jagd3\OneDrive\Documentos\universidad\Software l\virtualcoffe"

# Verificar estado de Docker Compose
docker-compose ps

# Si algún servicio está down, reiniciar
docker-compose up -d

# Verificar que todos los servicios respondan
Invoke-RestMethod -Uri "http://localhost:8001/menu" -Method GET    # API Bebidas
Invoke-RestMethod -Uri "http://localhost:8081/actuator/health"     # API Pedidos  
Invoke-RestMethod -Uri "http://localhost:4200" -TimeoutSec 5       # UI Angular
Invoke-RestMethod -Uri "http://localhost:3000" -TimeoutSec 5       # UI React
```

---

## 🐍 **Tests de FastAPI (Python) - API Bebidas**

### Ejecutar Tests Unitarios

```powershell
# Navegar al directorio de la API de bebidas
cd "C:\Users\jagd3\OneDrive\Documentos\universidad\Software l\virtualcoffe\api-bebidas"

# Ejecutar todos los tests con cobertura
python -m pytest tests/ -v --cov=app --cov-report=html:reports/coverage

# Ejecutar tests específicos
python -m pytest tests/test_menu.py -v                    # Solo tests del menú
python -m pytest tests/test_menu.py::TestMenu::test_create_bebida_valida -v  # Test específico

# Ver reporte de cobertura
# El reporte HTML estará en: reports/coverage/index.html
```

**Resultado esperado:** 7 tests pasan ✅

### Análisis de Calidad de Código Python

```powershell
# Análisis con Pylint (calidad general)
python -m pylint app/ --max-line-length=100

# Verificación de tipos con Mypy
python -m mypy app/

# Formateo con Black (verificar formato)
python -m black --check app/ --diff

# Para aplicar formateo automáticamente
python -m black app/
```

---

## ☕ **Tests de Spring Boot (Java) - API Pedidos**

### Ejecutar Tests Unitarios y de Integración

```powershell
# Navegar al directorio de la API de pedidos
cd "C:\Users\jagd3\OneDrive\Documentos\universidad\Software l\virtualcoffe\api-pedidos\pedidos"

# Ejecutar todos los tests con Maven
.\mvnw.cmd test

# Ejecutar solo tests específicos
.\mvnw.cmd test -Dtest=PedidosApplicationTests        # Test de contexto
.\mvnw.cmd test -Dtest=OrderServiceTest              # Tests del servicio
.\mvnw.cmd test -Dtest=CucumberTest                  # Tests BDD

# Ver reporte de cobertura JaCoCo
# El reporte estará en: target/site/jacoco/index.html
```

**Resultado esperado:** 10 tests pasan ✅

### Verificar Cobertura JaCoCo

```powershell
# Generar reporte de cobertura
.\mvnw.cmd jacoco:report

# Verificar si existe el reporte
if (Test-Path "target\site\jacoco\index.html") { 
    Write-Host "✅ Reporte JaCoCo generado correctamente" 
    # Abrir en navegador (opcional)
    Start-Process "target\site\jacoco\index.html"
}
```

---

## 🎭 **Tests BDD (Behavior Driven Development)**

### Tests BDD con Cucumber (Java)

```powershell
# Ya incluidos en los tests de Maven, pero para ejecutar solo BDD:
cd "C:\Users\jagd3\OneDrive\Documentos\universidad\Software l\virtualcoffe\api-pedidos\pedidos"

.\mvnw.cmd test -Dtest=CucumberTest
```

**Resultado esperado:** 5 escenarios BDD pasan ✅

### Verificar archivos .feature

```powershell
# Ver los archivos de especificaciones BDD
Get-Content "src\test\resources\features\pedido.feature"
Get-Content "..\..\features\pedido_exitoso.feature"
Get-Content "..\..\features\bebida_no_disponible.feature"
```

---

## 🌐 **Tests End-to-End (E2E) con Selenium**

### Preparar entorno E2E

```powershell
# Navegar al directorio de tests E2E
cd "C:\Users\jagd3\OneDrive\Documentos\universidad\Software l\virtualcoffe\tests-e2e"

# Verificar dependencias
python -c "import selenium, pytest; print('✅ Dependencias E2E OK')"

# Crear directorio para screenshots
mkdir -Force screenshots
```

### Ejecutar Tests E2E

```powershell
# Test básico de UI Angular
python -m pytest test_angular_flow.py::TestAngularFlow::test_ver_menu_vacio -v -s

# Test básico de funcionalidad (puede fallar por selectores)
python -m pytest test_angular_flow.py::TestAngularFlow::test_agregar_bebida_valida -v -s

# Test de React básico
python -m pytest test_react_flow.py::TestReactFlow::test_realizar_pedido_valido -v -s

# Test de flujo completo (si los selectores coinciden)
python -m pytest test_complete_flow.py -v -s

# Ver screenshots generados en caso de fallos
ls screenshots/
```

**Nota:** Los tests E2E pueden fallar si los selectores `data-testid` no coinciden exactamente con los componentes.

---

## 📊 **Ejecutar TODOS los Tests - Flujo Completo**

### Script para ejecutar todos los tests secuencialmente

```powershell
# Crear script de ejecución completa
$rootDir = "C:\Users\jagd3\OneDrive\Documentos\universidad\Software l\virtualcoffe"

Write-Host "🚀 INICIANDO SUITE COMPLETA DE TESTS - VIRTUALCOFFEE" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# 1. Tests FastAPI Python
Write-Host "🐍 1. EJECUTANDO TESTS FASTAPI (PYTHON)..." -ForegroundColor Cyan
cd "$rootDir\api-bebidas"
$pythonResult = python -m pytest tests/ -v --cov=app
Write-Host "✅ Tests FastAPI completados" -ForegroundColor Green

# 2. Tests Spring Boot Java  
Write-Host "☕ 2. EJECUTANDO TESTS SPRING BOOT (JAVA)..." -ForegroundColor Cyan
cd "$rootDir\api-pedidos\pedidos"
$javaResult = .\mvnw.cmd test -q
Write-Host "✅ Tests Spring Boot completados" -ForegroundColor Green

# 3. Análisis de calidad Python
Write-Host "🔍 3. ANÁLISIS DE CALIDAD PYTHON..." -ForegroundColor Cyan
cd "$rootDir\api-bebidas"
python -m pylint app/ --max-line-length=100 --score=y
Write-Host "✅ Análisis de calidad completado" -ForegroundColor Green

# 4. Tests E2E básicos
Write-Host "🌐 4. EJECUTANDO TESTS E2E BÁSICOS..." -ForegroundColor Cyan
cd "$rootDir\tests-e2e"
python -m pytest test_angular_flow.py::TestAngularFlow::test_ver_menu_vacio -v
Write-Host "✅ Tests E2E básicos completados" -ForegroundColor Green

Write-Host "🎉 SUITE COMPLETA DE TESTS FINALIZADA" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
```

---

## 📈 **Verificar Reportes y Cobertura**

### Locations de reportes generados

```powershell
# Reporte de cobertura Python (HTML)
Start-Process "$rootDir\api-bebidas\reports\coverage\index.html"

# Reporte de cobertura Java (JaCoCo HTML)  
Start-Process "$rootDir\api-pedidos\pedidos\target\site\jacoco\index.html"

# Screenshots de tests E2E (en caso de fallos)
ls "$rootDir\tests-e2e\screenshots\"

# Logs de Cucumber (BDD)
Get-Content "$rootDir\api-pedidos\pedidos\target\cucumber-reports.html"
```

---

## 🛠️ **Troubleshooting - Solución de Problemas**

### Si los servicios Docker no responden

```powershell
# Reiniciar servicios completamente
docker-compose down
docker-compose up -d --build

# Verificar logs de servicios problemáticos
docker logs api-bebidas --tail 20
docker logs api-pedidos --tail 20
docker logs ui-bebidas --tail 20
docker logs ui-pedidos --tail 20
```

### Si fallan tests E2E por selectores

```powershell
# Los tests E2E pueden fallar porque los selectores data-testid no coinciden exactamente
# Para verificar elementos disponibles, revisar:
# - ui-bebidas/src/app/components/add-bebida/add-bebida.component.html
# - ui-pedidos/src/components/OrderForm.js

# Elementos esperados vs reales:
# Angular: data-testid="input-name" ✅ (existe)
# React: data-testid="input-drink-name" ❌ (real: "input-product-name-0")
```

### Si fallan tests unitarios

```powershell
# Verificar versiones de dependencias
python -m pytest --version
.\mvnw.cmd --version

# Limpiar caché y reinstalar dependencias
pip install --upgrade -r requirements.txt  # Para Python
.\mvnw.cmd clean install                   # Para Maven
```

---

## 📋 **Checklist de Tests Completados**

### ✅ **Backend Tests**
- [ ] FastAPI Python: 7 tests unitarios
- [ ] Spring Boot Java: 10 tests (unitarios + integración)
- [ ] BDD Cucumber: 5 escenarios  

### ✅ **Quality Analysis**
- [ ] Pylint: Análisis de código Python
- [ ] JaCoCo: Cobertura de código Java
- [ ] Black: Formateo de código Python

### ⚠️ **E2E Tests** (Opcional - pueden necesitar ajustes)
- [ ] Test básico Angular UI
- [ ] Test básico React UI  
- [ ] Test flujo completo

### 📊 **Reports Generated**
- [ ] Cobertura HTML Python
- [ ] Cobertura HTML Java (JaCoCo)
- [ ] Screenshots E2E (si hay fallos)

---

## 🎯 **Resultado Esperado**

Al completar esta guía deberías tener:

- **✅ 17 tests unitarios pasando** (7 Python + 10 Java)
- **✅ 5 scenarios BDD pasando** 
- **✅ Cobertura > 60%** en ambos proyectos
- **✅ Análisis de calidad completo**
- **⚠️ Tests E2E básicos funcionando**

**¡Total: 22+ tests ejecutados exitosamente!** 🎉

---

## 📝 **Comandos Rápidos de Referencia**

### Tests básicos (ejecutar desde directorio raíz)
```powershell
# Tests Python
cd api-bebidas && python -m pytest tests/ -v

# Tests Java  
cd api-pedidos/pedidos && .\mvnw.cmd test

# Tests E2E básicos
cd tests-e2e && python -m pytest test_angular_flow.py::TestAngularFlow::test_ver_menu_vacio -v
```

### Análisis de calidad
```powershell
# Python
cd api-bebidas && python -m pylint app/ --max-line-length=100

# Ver cobertura Java
cd api-pedidos/pedidos && Start-Process target/site/jacoco/index.html
```

### Verificar servicios
```powershell
docker-compose ps
curl http://localhost:8001/menu
curl http://localhost:8081/actuator/health
```