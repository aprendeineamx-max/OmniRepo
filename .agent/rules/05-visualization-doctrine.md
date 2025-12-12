---
trigger: always_on
---

# 05_VISUALIZATION_DOCTRINE.md - PROTOCOLO DE VISUALIZACIÓN OMNISCIENTE

## 1. FILOSOFÍA VISUAL: "LA CIUDAD DE CRISTAL"
No estamos haciendo gráficos de barras. Estamos creando un **Universo Explorable**.
El usuario debe sentirse como si estuviera flotando sobre una ciudad cibernética transparente donde puede ver el tráfico (datos) moverse por las autopistas (funciones) y entrar en los edificios (clases).

## 2. TECNOLOGÍA DE RENDERIZADO (RENDIMIENTO EXTREMO)
El DOM estándar (HTML/SVG) morirá con repositorios grandes (+10,000 archivos).
**MANDATO TÉCNICO:** Debes utilizar tecnologías basadas en **WebGL** (GPU Acceleration).
* **Librerías Aprobadas:** `Three.js`, `Deck.gl`, o `Cosmograph` (para grafos masivos de +100k nodos). `React Flow` solo se permite para vistas "Micro" (detalle de un solo archivo).
* **Level of Detail (LOD):** Implementa algoritmos de LOD dinámico.
    * *Zoom Lejano:* Los archivos son puntos de luz (partículas). Las conexiones son tenues.
    * *Zoom Medio:* Aparecen etiquetas y clusters (barrios).
    * *Zoom Cercano:* Se renderizan las "cajas" de las funciones y las líneas de código como texturas.

## 3. CAPAS DE INFORMACIÓN (LAYERING)
La visualización debe tener interruptores para activar/desactivar "Dimensiones":
1.  **Capa Estructural (El Esqueleto):** Árbol de directorios y dependencias de archivos (`import`). Color: Azul Cián.
2.  **Capa Lógica (Los Órganos):** Clases y Funciones dentro de los archivos. Color: Verde Neón (Lógica), Naranja (UI), Rojo (Base de Datos).
3.  **Capa de Flujo (La Sangre):** Animación de partículas que viajan por las líneas de conexión. Esto representa el flujo de ejecución (Call Graph).
    * *Velocidad:* Representa la frecuencia de uso.
    * *Tamaño:* Representa el peso de los datos transferidos.
4.  **Capa Externa (Los Tentáculos):** Conexiones que salen del grafo principal hacia la "Nube" (APIs, DBs externas).

## 4. METÁFORAS VISUALES OBLIGATORIAS
* **El Hilo de Ariadna:** Al hacer clic en una variable, todo el resto del grafo se oscurece (dimming) y solo se iluminan intensamente las líneas que muestran dónde se define, dónde se usa y dónde muere esa variable.
* **Mapa de Calor de Deuda Técnica:** Los archivos con código espagueti o baja calidad deben brillar con un aura roja pulsante ("Zonas Radioactivas").
* **Grafo de Fuerza Dirigida (Physics Engine):** Los nodos no son estáticos. Deben repelerse y atraerse según su acoplamiento.
    * Archivos muy relacionados se agrupan en "Células".
    * Archivos independientes flotan en la periferia.

## 5. EXPERIENCIA DE USUARIO (GOD MODE UX)
* **Search & Fly:** Una barra de búsqueda global. Al escribir "AuthController", la cámara debe volar cinemáticamente a través del universo de nodos hasta enfocar ese archivo.
* **Modo Rayos X:** Al pasar el mouse sobre un nodo (archivo), se debe desplegar un "Holograma" flotante con el código fuente minificado y sus estadísticas vitales, sin necesidad de hacer clic.
* **Time-Travel (Git History):** Una barra deslizante en la parte inferior. Al moverla, el usuario debe ver cómo el grafo crece y cambia (archivos naciendo y muriendo) a lo largo de la historia de los commits del repositorio.

## 6. INTEGRACIÓN CON EL "PUENTE NEXUS"
La visualización no es solo para ver; es para controlar.
* **Clic Derecho en Nodo:** Debe abrir un menú contextual: "Enviar al IDE", "Refactorizar con IA", "Ejecutar Tests Aquí".
* Al seleccionar esta opción, el Frontend envía un JSON al `nexus_command.json`, y TÚ (el Agente) ejecutas la acción en el backend.