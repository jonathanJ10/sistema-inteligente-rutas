# 🧠 Sistema Inteligente de Rutas — Transporte Masivo

**Curso:** Inteligencia Artificial Avanzada  
**Universidad:** Iberoamericana — 2026  
**Referencia:** Benítez, R. (2014). *Inteligencia artificial avanzada*. Editorial UOC (caps. 2, 3 y 9)

## 📌 Descripción
Sistema inteligente basado en **reglas lógicas** y **búsqueda heurística A\*** que encuentra la mejor ruta entre dos estaciones del sistema de transporte masivo (TransMilenio, Bogotá).

## 🧩 Componentes del sistema
- **Base de conocimiento:** Grafo de 23 estaciones con costos en minutos
- **Motor de inferencia:** 4 reglas lógicas que validan y ajustan la búsqueda
- **Algoritmo de búsqueda:** A* (A-estrella) con función `f(n) = g(n) + h(n)`
- **Factor hora pico:** Ajuste automático del 50% en horas de alta demanda

## 📁 Estructura del repositorio
| Archivo | Contenido |
|---------|-----------|
| `sistema_rutas.py` | Código fuente del sistema (base de conocimiento, reglas, A*, interfaz) |
| `test_sistema_rutas.py` | Pruebas unitarias con `unittest` |
| `README.md` | Instrucciones de ejecución |

## ▶️ Cómo ejecutar

### Requisitos
- Python 3.8 o superior
- No requiere librerías externas (solo `heapq` y `unittest` de la librería estándar)

### Instalación y ejecución
```bash
# Clonar el repositorio
git clone https://github.com/jonathanJ10/sistema-inteligente-rutas.git
cd sistema-inteligente-rutas

# Ejecutar el sistema
python sistema_rutas.py
```

### Opciones al ejecutar
```
1 → Sistema interactivo: ingresa origen y destino manualmente
2 → Casos de prueba automáticos (6 escenarios predefinidos)
```

> Los nombres de las estaciones deben escribirse exactamente como aparecen en la lista (con tildes y mayúsculas), por ejemplo `Alcalá` o `Álamos`.

### Ejemplo de sesión interactiva
```
Opción (1/2): 1
👉 Ingrese estación de ORIGEN:  Portal Norte
👉 Ingrese estación de DESTINO: Calle 26
👉 ¿Es hora pico? (s/n):        n
```

### Ejecutar las pruebas unitarias
```bash
python -m unittest -v
```

## 🧪 Casos de prueba automáticos
| ID | Origen | Destino | Hora pico | Tiempo | Paradas | Resultado |
|----|--------|---------|-----------|--------|---------|-----------|
| CP-01 | Portal Norte | Calle 26 | No | 38.0 min | 11 | Ruta encontrada |
| CP-02 | Portal Norte | Portal Sur | Sí | 102.0 min | 17 | Ruta encontrada + R3 activada |
| CP-03 | Calle 85 | Calle 85 | No | — | — | R2: mismo punto |
| CP-04 | Portal 80 | NQS Calle 30 | No | 21.0 min | 6 | Ruta encontrada |
| CP-05 | Marly | Ricaurte | Sí | 18.0 min | 4 | Ruta encontrada |
| CP-06 | Granja | Portal Sur | No | 21.0 min | 5 | Ruta encontrada |

## 🗺️ Estaciones disponibles
Portal Norte, Toberin, Alcalá, Cardio Infantil, Pepe Sierra, Calle 100,
Calle 85, Calle 72, Flores, Calle 45, Marly, Calle 26, Universidades,
Ricaurte, Paloquemao, NQS Calle 30, General Santander, Portal Sur,
Portal 80, Avenida Rojas, Álamos, Granja, Carrera 90

## 📋 Reglas lógicas implementadas
| ID | Condición | Acción |
|----|-----------|--------|
| R1 | Hora pico activa | Aumentar costo ×1.5 |
| R2 | Origen == Destino | Retornar ruta vacía |
| R3 | Costo > 60 min | Sugerir ruta alternativa |
| R4 | Estación no existe | Retornar error |
