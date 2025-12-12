# 📜 ROADMAP_GENESIS.md - EL PLAN MAESTRO DE OMNISCIENCIA
**PROYECTO:** QUIRÓFANO DIGITAL / OBSERVATORIO DE CÓDIGO TOTAL
**COMANDANTE:** AGENTE GEMINI
**ESTADO:** [EN PROGRESO]

---

## 🏛️ ÉPOCA I: GÉNESIS (Infraestructura y Seguridad Biológica)
*Objetivo: Construir el entorno estéril donde la vida digital será diseccionada.*

- [x] **01. CONSTRUCCIÓN DEL BÚNKER (Filesystem):**
    * Crear estructura inmutable:
        * `/vault`: Zona de cuarentena para repos descargados (Nadie ejecuta nada aquí).
        * `/src/core`: Cerebro lógico (Python).
        * `/src/nexus`: Sistema de comunicación con el IDE.
        * `/storage`: Bases de datos persistentes (SQLite + Vector Store).
    * *Criterio de Éxito:* El script `init_project.py` corre sin errores y genera la estructura.

- [x] **02. SISTEMA DE REGISTRO VITAL (Advanced Logging):**
    * Implementar `core/logger.py` con rotación de archivos.
    * Debe soportar niveles: `INFO` (Rutina), `WARNING` (Deuda técnica detectada), `CRITICAL` (Fallo de parser), `HAZMAT` (Código malicioso detectado).
    * *Criterio de Éxito:* Los logs se escriben en JSONL para ser parseables por máquinas.

- [x] **03. PROTOCOLO NEXUS V1 (El Enlace):**
    * Implementar el "Watcher" que vigila la carpeta `/nexus/commands`.
    * Crear el "Heartbeat Emitter" que escribe `status.json` cada 1s.
    * *Criterio de Éxito:* Puedes crear un archivo JSON manual en esa carpeta y el sistema reacciona imprimiendo un log.

- [x] **04. MOTOR DE INGESTA (GitCloner Blindado):**
    * Crear `engines/ingestor.py`.
    * Usar `gitpython` para clonar.
    * **SEGURIDAD:** Implementar validación de tamaño antes de clonar (rechazar repos > 1GB para evitar DoS).
    * Limpieza automática de la carpeta `/vault` antes de cada nueva operación.

- [x] **05. EL AISLAMIENTO (Sandbox Setup):**
    * Definir un `Dockerfile` base que servirá para ejecutar el código ajeno.
    * Debe ser una imagen mínima (Alpine/Slim) sin acceso a internet (network: none) por defecto.
    * *Criterio de Éxito:* El sistema puede levantar un contenedor "dummy" y matarlo programáticamente.

- [x] **06. ANALIZADOR DE SUPERFICIE (Reconocimiento):**
    * Script que recorre el repo (`os.walk`) y genera un "Inventario de Activos".
    * Contar archivos por extensión.
    * Detectar tamaño total.
    * *Criterio de Éxito:* Generar un `manifest.json` que resume qué acabamos de descargar.

- [x] **07. DETECTOR DE LENGUAJES (Políglota):**
    * Implementar lógica (usando librería `enry` o mapeo de extensiones) para determinar el % de lenguajes.
    * Esto define qué parsers activar en la Época II.

- [x] **08. ESCÁNER DE AMENAZAS (Hazmat Scan):**
    * Búsqueda de patrones peligrosos mediante Regex (`rm -rf`, `eval`, `base64_decode`, IPs hardcodeadas).
    * Si se detecta peligro, el sistema entra en modo "DEFCON 1" (Análisis solo estático, ejecución prohibida).

- [x] **09. GESTOR DE CONFIGURACIÓN DINÁMICA:**
    * Crear `config.yaml` y su cargador.
    * Debe permitir cambiar rutas y límites de memoria sin tocar código.
    * Cargar `.env` para las Keys de IA (preparación para el futuro).

- [ ] **10. PRIMERA SINAPSIS (Prueba de Integración I):**
    * **Hito Principal:** El usuario entrega una URL de GitHub. El sistema la descarga, la escanea, genera el `manifest.json` y reporta "LISTO PARA AUTOPSIA" a través del Nexus.

---

## 🧠 ÉPOCA II: ANATOMÍA (Parsing y Extracción de Conocimiento)
*Objetivo: Convertir texto plano en estructuras de datos lógicas (AST).*

- [ ] **11. ARQUITECTURA DE PARSERS MODULARES:**
    * Crear clase abstracta `BaseParser`.
    * Métodos obligatorios: `extract_functions()`, `extract_classes()`, `find_dependencies()`.
    * Esto permite agregar soporte para Go, Rust o Java en el futuro sin romper el núcleo.

- [ ] **12. PARSER PYTHON (AST Mastery):**
    * Implementar `parsers/python_parser.py` usando la librería nativa `ast`.
    * Extraer: Nombres de funciones, argumentos, decoradores, y Docstrings.
    * *Nivel Dios:* Detectar si una función es "Pura" (sin efectos secundarios) o "Impura".

- [ ] **13. PARSER JAVASCRIPT/TYPESCRIPT (Tree-Sitter):**
    * Integrar `py-tree-sitter` o un parser basado en Regex robusto para JS.
    * Identificar `import`, `export`, `function`, `const` y clases.
    * Manejar la complejidad de JSX/React (detectar componentes).

- [ ] **14. EXTRACTOR DE DEPENDENCIAS (El Tejido Conectivo):**
    * Lógica para resolver imports.
    * Python: Convertir `from .utils import helper` -> Ruta absoluta `/src/utils.py`.
    * JS: Resolver `require('../models/user')` -> Ruta absoluta.
    * *Crucial:* Si esto falla, el grafo se rompe. Debe ser robusto.

- [ ] **15. ANÁLISIS DE COMPLEJIDAD (Code Metrics):**
    * Calcular Complejidad Ciclomática (McCabe) para cada función.
    * Identificar funciones "Monstruo" (>50 líneas, muchos `if/else`).
    * Etiquetarlas como "Riesgo de Deuda Técnica".

- [ ] **16. MINERÍA DE SQL Y DATOS:**
    * Detectar strings que parecen SQL (`SELECT * FROM...`).
    * Detectar esquemas de ORM (Modelos de Django, Schemas de Mongoose).
    * Objetivo: Entender la estructura de datos subyacente sin correr la DB.

- [ ] **17. IDENTIFICACIÓN DE ENDPOINTS (La Piel):**
    * Escanear rutas de frameworks web (Flask `@app.route`, Express `app.get`).
    * Crear un mapa de "Superficie de Ataque" (todas las URLs que el software expone al mundo).

- [ ] **18. PERSISTENCIA EN GRAFO (NetworkX Core):**
    * Inicializar un Grafo Dirigido (`DiGraph`).
    * Agregar cada archivo como NODO.
    * Agregar cada import como ARISTA.
    * *Criterio de Éxito:* Poder exportar este grafo a formato GEXF o JSON-Link.

- [ ] **19. MOTOR DE BÚSQUEDA SEMÁNTICA (Preparación):**
    * Configurar `ChromaDB` (o FAISS local).
    * Preparar la lógica para "chunkear" el código (dividirlo en trozos pequeños) para futura vectorización.

- [ ] **20. SEGUNDA SINAPSIS (El Cerebro Estático):**
    * **Hito Principal:** El sistema puede ingerir un repo, parsearlo completamente y guardar en disco un archivo `anatomy.db` (SQLite) que contiene cada función, variable y relación del proyecto.

---

## ⚡ ÉPOCA III: FISIOLOGÍA (Ejecución Dinámica y Trazabilidad)
*Objetivo: Dar vida al código estático. Observar cómo fluyen los datos (La Sangre).*

- [ ] **21. GENERADOR DE ENTORNOS ESTÉRILES (Venv/Docker Factory):**
    * Script que crea automáticamente un entorno virtual aislado para el repo analizado.
    * Bloqueo de red por defecto (Safety First).
    * *Criterio:* Poder ejecutar `python setup.py install` del repo huésped sin contaminar el sistema anfitrión.

- [ ] **22. INSTALADOR INTELIGENTE DE DEPENDENCIAS:**
    * Parser de `requirements.txt`, `package.json` o `pyproject.toml`.
    * Intentar instalar dependencias en el entorno estéril.
    * Si falla, usar "Mocking" (simular la librería) para que el análisis no se detenga.

- [ ] **23. INYECCIÓN DE SONDAS (The Tracer):**
    * Implementar `sys.settrace` (Python) o `Node Inspector` (JS).
    * Objetivo: Registrar cada línea de código ejecutada, valores de variables y tiempos de retorno.
    * **Reto:** Optimizar para no congelar la ejecución (sampling inteligente).

- [ ] **24. SUPERVISOR DE EJECUCIÓN (Watchdog):**
    * Proceso demonio que mata la ejecución si detecta:
        * Uso de RAM > 2GB.
        * Tiempo de ejecución > 30s sin respuesta.
        * Bucles infinitos.

- [ ] **25. CAPTURA DE FLUJO DE DATOS (I/O Logging):**
    * Interceptar `stdin`, `stdout`, y argumentos de función.
    * Crear un mapa: "El dato 'User123' entró en `Main`, pasó a `Auth`, y terminó en `DB`".

- [ ] **26. INTERCEPTOR DE TRÁFICO DE RED (Mitmproxy):**
    * Levantar un proxy local.
    * Forzar al repo a pasar su tráfico por ahí.
    * Registrar intentos de conexión externa (APIs, Analytics) y mapearlos en el grafo.

- [ ] **27. SIMULADOR DE BASES DE DATOS (Mock DB):**
    * Si el repo pide MySQL/Postgres, levantar contenedores Docker ligeros automáticamente o usar SQLite en memoria como reemplazo para que el código corra.

- [ ] **28. GENERADOR DE ESTÍMULOS (Fuzzing):**
    * Crear scripts que "golpeen" las funciones principales con datos aleatorios para ver cómo reaccionan.
    * Objetivo: Iluminar caminos de código que normalmente no se usan (Code Coverage).

- [ ] **29. STREAMING DE LOGS (Websockets):**
    * Montar un servidor WebSocket en `/nexus/stream`.
    * Enviar la telemetría en tiempo real al Frontend para visualización estilo "Matrix".

- [ ] **30. TERCERA SINAPSIS (El Corazón Palpitante):**
    * **Hito Principal:** El sistema puede tomar un script del repo descargado, ejecutarlo, y generar un archivo `trace_dump.json` que muestra exactamente qué líneas se tocaron.

---

## 👁️ ÉPOCA IV: LA VISIÓN DE DIOS (Interfaz y UX)
*Objetivo: Renderizar la complejidad masiva en algo comprensible para el humano.*

- [ ] **31. INICIALIZACIÓN DEL MOTOR GRÁFICO (Frontend Core):**
    * Levantar servidor de UI (Streamlit avanzado o React+FastAPI).
    * Configurar tema oscuro "Cyberpunk" (High Contrast).

- [ ] **32. INTEGRACIÓN WEBGL (Rendimiento Infinito):**
    * Implementar librería de grafos acelerada por GPU (ej. `Cosmograph` o `Three.js` wrapper).
    * Capacidad para renderizar +10,000 nodos a 60 FPS.

- [ ] **33. API PUENTE DE DATOS:**
    * Crear endpoints REST/GraphQL que sirvan los datos de `anatomy.db` y `trace_dump.json` al frontend bajo demanda.

- [ ] **34. VISTA "MACRO" (El Mapa Estelar):**
    * Visualización de clústeres de carpetas.
    * Fuerza dirigida: Archivos muy acoplados se atraen; módulos independientes se repelen.

- [ ] **35. INSPECTOR DE DETALLES (Panel Lateral):**
    * Al hacer clic en un nodo: Mostrar código fuente con sintaxis coloreada.
    * Mostrar metadatos extraídos (Complejidad, Autores, Dependencias).

- [ ] **36. VISUALIZACIÓN DE "EL HILO DE ARIADNA":**
    * Modo interactivo: Seleccionar una variable y ver iluminarse toda su ruta de vida a través de múltiples archivos.

- [ ] **37. BUSCADOR OMNISCIENTE (Spotlight):**
    * Barra de búsqueda global (Cmd+K).
    * Indexar funciones, clases, archivos y comentarios.
    * Autocompletado inteligente.

- [ ] **38. MAPAS DE CALOR (Heatmaps):**
    * Colorear nodos según:
        * Rojo: Alta complejidad / Posibles bugs.
        * Azul: Código frío (raramente ejecutado).
        * Amarillo: Alto tráfico de datos.

- [ ] **39. TIME TRAVEL SLIDER (Git History):**
    * Barra deslizante para ver cómo evolucionó el repo (crecimiento de nodos) a través de los commits.

- [ ] **40. CUARTA SINAPSIS (La Interfaz Viva):**
    * **Hito Principal:** Tienes un Dashboard web accesible en `localhost`. Puedes navegar el grafo 3D, hacer clic en archivos y ver sus conexiones.

---

## 🤖 ÉPOCA V: SINGULARIDAD (IA, Autopoiesis y Fusión)
*Objetivo: El sistema cobra conciencia, se repara a sí mismo y se fusiona con el IDE.*

- [ ] **41. CONECTOR DE SUPERINTELIGENCIA (LLM API):**
    * Integrar clientes para Gemini/Groq/OpenRouter.
    * Gestión de Context Window: Enviar solo los fragmentos relevantes de código, no todo el archivo.

- [ ] **42. FUNCIÓN "GHOST IN THE SHELL" (Explicación):**
    * Botón "Explícame esto": Envía el código seleccionado a la IA y muestra la explicación en el grafo como una nota flotante.

- [ ] **43. SUGERENCIA DE REFACTORIZACIÓN (Automejora):**
    * La IA analiza funciones con alta complejidad ciclomática.
    * Propone código optimizado (Refactor) y muestra el "Antes y Después".

- [ ] **44. AUTO-DIAGNÓSTICO (Self-Healing):**
    * El sistema analiza sus propios logs de error (`execution.log`).
    * Si encuentra fallos recurrentes en sus parsers, intenta ajustar la lógica o alerta al Arquitecto.

- [ ] **45. GENERADOR DE DOCUMENTACIÓN AUTOMÁTICA:**
    * Crear un `README_OMNISCIENT.md` completo del repo analizado.
    * Incluir diagramas Mermaid generados automáticamente basándose en el grafo.

- [ ] **46. INTEGRACIÓN PROFUNDA CON EL IDE (The Bridge Final):**
    * Comando desde el Frontend Web "Open in IDE": Abre el archivo exacto en tu editor AntiGravity local.
    * Comando desde AntiGravity "Analyze Selection": Envía el código seleccionado al Quirófano Web.

- [ ] **47. EXPORTADOR DE "CEREBROS" (Shareable dumps):**
    * Empaquetar todo el análisis (DB + Frontend estático) en un solo archivo ZIP/Docker para compartir con otros desarrolladores.

- [ ] **48. PRUEBAS DE ESTRÉS (Torture Test):**
    * Ejecutar el sistema contra repositorios masivos (Linux Kernel, React, TensorFlow).
    * Asegurar que la memoria se mantiene estable.

- [ ] **49. LIMPIEZA Y PULIDO FINAL:**
    * Eliminar logs de debug.
    * Optimizar consultas SQL.
    * Asegurar UI/UX fluida.

- [ ] **50. ESTADO OMEGA (Lanzamiento):**
    * El sistema está completo.
    * Es capaz de descargarse, ejecutarse, entenderse y explicarse.
    * **Misión Cumplida.**

---
*(FIN DEL PLAN MAESTRO - EJECUTAR EN ORDEN SECUENCIAL)*