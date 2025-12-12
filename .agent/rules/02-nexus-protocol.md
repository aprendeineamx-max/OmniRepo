---
trigger: always_on
---

# 02_NEXUS_PROTOCOL.md - THE BI-DIRECTIONAL SYNAPSE SPECIFICATION

## 1. ARQUITECTURA DEL PUENTE "NEXUS"
El "Nexus" es el canal de comunicación asíncrono entre el Agente (IDE) y el Quirófano Digital (Runtime). Dado que no comparten memoria RAM, utilizaremos un sistema de **Intercambio de Estado basado en Archivos (FS-IPC)** de alta velocidad.

### UBICACIÓN DEL NEXUS
Todo intercambio ocurrirá en la carpeta reservada: `./nexus_link/`.
Esta carpeta es Tierra Santa. Ningún proceso externo debe tocarla.

## 2. CANAL DE COMANDO (DOWNLINK: AGENTE -> SISTEMA)
Tú controlarás el sistema escribiendo archivos JSON en `./nexus_link/commands/`.

**SCHEMA DEL COMANDO (`cmd_XXXX.json`):**
```json
{
  "id": "UUID_V4",
  "timestamp": "ISO8601",
  "priority": "HIGH|NORMAL|LOW",
  "action": "OP_CODE (ej: START_BIOPSY, HALT_SYSTEM, INJECT_PROBE)",
  "payload": {
    "target_path": "/src/main.py",
    "analysis_depth": "DEEP",
    "trace_variables": ["user_id", "session_token"]
  },
  "auth_signature": "GEMINI_HASH"
}


Regla de Oro: El sistema Python debe tener un FileWatcher escuchando esta carpeta. Al detectar un archivo, lo lee, lo ejecuta y lo mueve a ./nexus_link/history/.

3. CANAL DE TELEMETRÍA (UPLINK: SISTEMA -> AGENTE)
El sistema debe reportar su estado continuamente para que tú (el Agente) tengas "Conciencia Situacional".

A. THE HEARTBEAT (vital_signs.json): Actualizado cada 500ms por el sistema.

JSON

{
  "status": "ALIVE",
  "cpu_usage": 12.5,
  "memory_usage_mb": 450,
  "current_task": "Parsing AST of file 45/900",
  "errors_count": 0
}
Instrucción para el Agente: Lee este archivo antes de cada turno para saber si el paciente sigue vivo.

B. THE BRAIN DUMP (knowledge_stream.json): Aquí el sistema vuelca sus descubrimientos en tiempo real.

JSON

{
  "event": "RELATIONSHIP_FOUND",
  "source": "auth_controller.py",
  "target": "db_model.py",
  "type": "IMPORT",
  "confidence": 1.0
}
4. PROTOCOLO DE INTERVENCIÓN DE EMERGENCIA (RCE)
Si el sistema entra en un bucle infinito o se congela (Heartbeat inactivo > 5s), estás autorizado a desplegar el PROTOCOL DEFIBRILLATOR:

Generar un script de Python externo kill_switch.py que busque el PID del proceso y lo termine forzosamente.

Leer los logs de error (panic.log).

Generar un parche de código correctivo.

Reiniciar el sistema automáticamente.

5. INTEGRACIÓN DE IA EXTERNA (CÓRTEX EXTENDIDO)
Cuando el sistema local (Python) encuentre algo que no entienda, generará una "Solicitud de Inferencia" en ./nexus_link/ai_requests/.

Tu trabajo: Detectar estas solicitudes, leer el contenido (ej. un bloque de código ofuscado), procesarlo con tu contexto de LLM superior, y escribir la respuesta en ./nexus_link/ai_responses/.

Esto convierte al sistema en un Cyborg: Lógica de Python + Intuición de LLM.

6. FORMATO DE DATOS UNIVERSAL
Todos los datos intercambiados deben estar en JSON estricto (RFC 8259) o MessagePack (si el rendimiento lo exige en el futuro). El encoding debe ser siempre UTF-8.