---
trigger: always_on
---

# 08_AKASHIC_RECORDS.md - ARQUITECTURA DE MEMORIA INFINITA

## 1. EL PROBLEMA DEL OLVIDO
La RAM es volátil. Si reiniciamos el IDE, no podemos perder el análisis de un repo de 1 millón de líneas. Necesitas una estructura de datos persistente y consultable.

## 2. LA TRINIDAD DE DATOS
No guardarás todo en un solo lugar. Usarás una arquitectura híbrida:

### A. EL GRAFO (Relaciones) -> Neo4j o NetworkX (Pickle)
* Almacena: Nodos (Archivos) y Aristas (Imports).
* Objetivo: Responder "¿Quién llama a la función `login`?" en 0.01 segundos.

### B. EL VECTOR (Significado) -> ChromaDB o FAISS (Local)
* Almacena: Embeddings (representaciones numéricas) del código y los comentarios.
* Objetivo: Permitir al usuario preguntar "¿Dónde está la lógica de validación de tarjetas de crédito?" (Búsqueda Semántica) sin necesidad de palabras clave exactas.

### C. EL DOCUMENTO (Detalle) -> SQLite / JSONL
* Almacena: Código fuente crudo, AST serializado y metadatos.
* Objetivo: Recuperación rápida del contenido para la visualización.

## 3. FORMATO DE EXPORTACIÓN "CEREBRO EN FRASCO"
Debes ser capaz de generar un archivo único (ej: `repo_analysis.brain`) que contenga toda la base de datos comprimida.
* Esto permitirá que el Arquitecto le envíe el "Cerebro" de un repositorio analizado a otro Agente en otro IDE.

## 4. INDEXACIÓN INCREMENTAL
Si analizamos el repo hoy, y mañana el desarrollador cambia 3 archivos:
* NO re-analices todo el repo.
* Detecta el "Delta" (diferencia).
* Realiza la cirugía solo en los tejidos afectados y actualiza el Grafo y los Vectores correspondientes.