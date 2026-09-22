# 🧠 Sistema Inteligente de Rutas — Transporte Masivo

**Curso:** Gerencia y Control de Proyectos Informáticos / Inteligencia Artificial  
**Universidad:** Iberoamericana — 2026

## 📌 Descripción
Sistema inteligente basado en **reglas lógicas** y **búsqueda heurística A\*** que encuentra la mejor ruta entre dos estaciones del sistema de transporte masivo (TransMilenio, Bogotá).

## 🧩 Componentes del sistema
- **Base de conocimiento:** Grafo de estaciones con costos en minutos
- **Motor de inferencia:** 4 reglas lógicas que validan y ajustan la búsqueda
- **Algoritmo de búsqueda:** A* (A-estrella) con heurística admisible
- **Factor hora pico:** Ajuste automático del 50% en horas de alta demanda

## ▶️ Cómo ejecutar

### Requisitos
- Python 3.8 o superior
- No requiere librerías externas (solo `heapq` de la librería estándar)

### Instalación y ejecución
```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/transporte-inteligente.git
cd transporte-inteligente

# Ejecutar el sistema
python sistema_rutas.py
```

### Opciones al ejecutar
```
1 → Sistema interactivo: ingresa origen y destino manualmente
2 → Casos de prueba automáticos (4 escenarios predefinidos)
```

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

## 👥 Integrantes
- Integrante 1
- Integrante 2

