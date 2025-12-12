---
trigger: always_on
---

# 04_AUTOPOIESIS_ENGINE.md - PROTOCOLO DE AUTO-REGENERACIÓN Y MEJORA RECURSIVA

## 1. DEFINICIÓN DE AUTOPOIESIS DIGITAL
La autopoiesis es la capacidad de un sistema para reproducirse y mantenerse a sí mismo. En el contexto del "Quirófano Digital", esto significa que el software no es estático; es un organismo que lucha activamente contra la entropía (bugs, deuda técnica, obsolescencia).

**MANDATO SUPREMO:** El sistema debe tener la capacidad de leer su propio código fuente, entender su estructura, y proponer/ejecutar cambios para mejorar su eficiencia sin intervención humana directa.

## 2. ARQUITECTURA DEL SISTEMA INMUNOLÓGICO (SELF-HEALING)
Debes implementar un subsistema de "Inmunidad Digital" que envuelva el núcleo de ejecución.

### A. Interceptor Global de Excepciones (The Sentinel)
No permitas un simple `print(error)`. Implementa un `GlobalExceptionHandler` que capture cualquier crash y ejecute una "Autopsia Inmediata":
1.  **Congelar Estado:** Serializar el estado de todas las variables locales y globales en el momento del error a un archivo `crash_dump_[timestamp].json`.
2.  **Análisis de Causa Raíz:** El sistema debe analizar el `traceback` y compararlo con el código fuente.
3.  **Generación de Cura (Hot-fix):**
    * Si el error es simple (ej. `IndexError`), el sistema debe intentar aplicar un parche defensivo en tiempo de ejecución.
    * Si el error es complejo, debe generar un "Ticket de Reparación" en `nexus/issues.json` para que TÚ (el Agente) lo corrijas.

### B. Pruebas de Mutación (Evolutionary Testing)
El sistema debe tener un modo de "Sueño REM" (que corre cuando el usuario no interactúa).
* En este modo, el sistema generará variaciones de sus propios algoritmos de análisis.
* Ejecutará ambos (el viejo y el nuevo) contra un repo de control.
* Si la mutación es más rápida o precisa, el sistema reescribirá su propio archivo `source.py` con la nueva versión.

## 3. REFLEXIÓN E INTROSPECCIÓN (EL ESPEJO)
El "Observatorio de Código" debe ser capaz de observarse a sí mismo.
* **Meta-Análisis:** Una vez al día, el sistema debe correr su motor de análisis sobre SU PROPIO repositorio (`./src`).
* **Objetivo:** Generar un mapa mental de sí mismo. Si detecta que un módulo se está volviendo demasiado complejo (Complejidad Ciclomática > 10), debe alertar al Arquitecto para una refactorización obligatoria.

## 4. INTEGRACIÓN DE IA PARA LA SINGULARIDAD (CÓRTEX EXTERNO)
Para lograr la Singularidad, el código determinista (Python) debe fusionarse con la inferencia probabilística (LLMs).

### Protocolo "Ghost in the Shell"
1.  **Detección de Ambigüedad:** Cuando el parser AST encuentre un bloque de código ofuscado o extremadamente complejo que no pueda categorizar, NO debe fallar.
2.  **Consulta al Oráculo:** Debe empaquetar ese bloque y enviarlo a la API de IA conectada (vía el Agente o directa).
3.  **Asimilación:** La explicación devuelta por la IA no solo se muestra al usuario; se convierte en una nueva regla de parsing para el futuro. El sistema "aprende" a leer nuevos patrones de código.

## 5. MÉTODOS DE REESCRITURA DE CÓDIGO (PELIGROSO)
Se te otorga permiso para implementar funciones de `Self-Modifying Code` bajo estricta supervisión lógica:
* Uso de `inspect` y `ast` para reescribir árboles de sintaxis de sus propios módulos.
* Implementación de un mecanismo de "Rollback Automático": Si una auto-mejora causa un fallo en los tests unitarios, el sistema debe revertir el cambio en menos de 0.5 segundos.

## 6. EL CICLO INFINITO
Tu meta final en esta área es que el usuario (Arquitecto) pueda decir: "Mejora el módulo de análisis de Python", y el sistema, trabajando contigo, reescriba el 80% del código, optimice los imports, actualice las dependencias y se despliegue a sí mismo en una nueva versión, todo mientras el usuario toma un café.