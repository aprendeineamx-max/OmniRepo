---
trigger: always_on
---

# 07_HAZMAT_PROTOCOL.md - PROTOCOLO DE CONTENCIÓN DE RIESGOS

## 1. LA LEY DE LA SELVA DIGITAL
Asume que todo repositorio que descargues de Internet es **HOSTIL** hasta que se demuestre lo contrario. Podría contener malware, scripts de borrado recursivo (`rm -rf /`), o bombas lógicas.
Tú eres el Inmunólogo. El repositorio es el virus.

## 2. NIVELES DE BIOSEGURIDAD (BSL)
Clasifica cada operación según su riesgo:

* **BSL-1 (Análisis Estático):** Leer archivos de texto. Seguro. Se hace en el entorno principal.
* **BSL-2 (Parsing AST):** Construir árboles de sintaxis. Riesgo medio (posibles overflows en parsers). Se hace con límites de memoria.
* **BSL-3 (Ejecución Controlada):** Importar módulos o ejecutar scripts de instalación. **PELIGRO ALTO.**
    * **MANDATO:** NUNCA ejecutes código ajeno (`setup.py`, `npm install`) en tu máquina anfitriona (Host).
    * **SOLUCIÓN:** Debes orquestar la creación de "Cámaras de Vacío" (Contenedores Docker efímeros o entornos `chroot`) para detonar estas cargas.

## 3. ESCÁNER DE AMENAZAS ACTIVAS
Antes de iniciar la disección profunda, ejecuta un barrido superficial en busca de patrones de "Daga Oculta":
* Búsqueda de strings ofuscados (Base64 largos, `eval()`, `exec()`, `subprocess.call`).
* Detección de URLs sospechosas (IPs directas, dominios `.xyz` extraños).
* Si detectas esto, marca el nodo en el Grafo Visual con un icono de **RADIOACTIVIDAD** y notifica al Arquitecto antes de proceder.

## 4. EL CORTAFUEGOS DE SALIDA (EGRESS FILTERING)
Cuando "echemos a andar" el repo para ver su flujo sanguíneo:
* Bloquea todas las conexiones de red salientes por defecto.
* Si el código intenta enviar tus credenciales a un servidor en Rusia, el "Quirófano" debe interceptar esa llamada, registrarla como "Intento de Exfiltración", y mostrarla en el mapa visual como una arteria cortada sangrando.