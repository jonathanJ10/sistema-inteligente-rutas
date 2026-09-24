"""
Sistema Inteligente de Rutas - Transporte Masivo (TransMilenio)
Basado en búsqueda heurística A* y base de conocimiento en reglas lógicas
Curso: Inteligencia Artificial Avanzada
"""

import heapq

# ============================================================
# BASE DE CONOCIMIENTO - Reglas lógicas del sistema de rutas
# ============================================================

# Grafo de estaciones: {estacion: [(vecino, costo_tiempo_minutos)]}
GRAFO_TRANSMILENIO = {
    "Portal Norte":     [("Toberin", 4), ("Alcalá", 5)],
    "Toberin":          [("Portal Norte", 4), ("Cardio Infantil", 3)],
    "Alcalá":           [("Portal Norte", 5), ("Cardio Infantil", 4)],
    "Cardio Infantil":  [("Toberin", 3), ("Alcalá", 4), ("Pepe Sierra", 5)],
    "Pepe Sierra":      [("Cardio Infantil", 5), ("Calle 100", 4)],
    "Calle 100":        [("Pepe Sierra", 4), ("Calle 85", 3)],
    "Calle 85":         [("Calle 100", 3), ("Calle 72", 4)],
    "Calle 72":         [("Calle 85", 4), ("Flores", 3)],
    "Flores":           [("Calle 72", 3), ("Calle 45", 5)],
    "Calle 45":         [("Flores", 5), ("Marly", 3)],
    "Marly":            [("Calle 45", 3), ("Calle 26", 4)],
    "Calle 26":         [("Marly", 4), ("Universidades", 3)],
    "Universidades":    [("Calle 26", 3), ("Ricaurte", 5)],
    "Ricaurte":         [("Universidades", 5), ("Paloquemao", 4)],
    "Paloquemao":       [("Ricaurte", 4), ("NQS Calle 30", 6)],
    "NQS Calle 30":     [("Paloquemao", 6), ("General Santander", 5)],
    "General Santander":[("NQS Calle 30", 5), ("Portal Sur", 7)],
    "Portal Sur":       [("General Santander", 7)],
    "Portal 80":        [("Avenida Rojas", 5)],
    "Avenida Rojas":    [("Portal 80", 5), ("Álamos", 4)],
    "Álamos":           [("Avenida Rojas", 4), ("Granja", 3)],
    "Granja":           [("Álamos", 3), ("Carrera 90", 4)],
    "Carrera 90":       [("Granja", 4), ("NQS Calle 30", 5)],
}

# ============================================================
# REGLAS DE CONOCIMIENTO (Base de reglas lógicas)
# ============================================================

REGLAS = [
    {"id": "R1", "condicion": "hora_pico == True",
     "accion": "aumentar_costo * 1.5",
     "descripcion": "En hora pico los tiempos aumentan 50%"},
    {"id": "R2", "condicion": "estacion_inicio == estacion_fin",
     "accion": "retornar_ruta_vacia",
     "descripcion": "Si inicio == fin, no se necesita ruta"},
    {"id": "R3", "condicion": "costo > 60",
     "accion": "sugerir_ruta_alterna",
     "descripcion": "Si la ruta supera 60 min, sugerir alternativa"},
    {"id": "R4", "condicion": "estacion not in grafo",
     "accion": "retornar_error_estacion",
     "descripcion": "La estación debe existir en el sistema"},
]

def aplicar_reglas(inicio, fin, hora_pico=False):
    """Motor de inferencia: aplica las reglas lógicas antes de buscar"""
    print("\n🔍 MOTOR DE INFERENCIA - Evaluando reglas...")
    for regla in REGLAS:
        if regla["id"] == "R2" and inicio == fin:
            print(f"  ✅ {regla['id']}: {regla['descripcion']}")
            return None, "MISMO_PUNTO"
        if regla["id"] == "R4" and (inicio not in GRAFO_TRANSMILENIO or fin not in GRAFO_TRANSMILENIO):
            print(f"  ✅ {regla['id']}: {regla['descripcion']}")
            return None, "ESTACION_INVALIDA"
        if regla["id"] == "R1" and hora_pico:
            print(f"  ✅ {regla['id']}: {regla['descripcion']}")
    print("  ✅ Todas las reglas evaluadas. Iniciando búsqueda A*...\n")
    return True, "OK"


# ============================================================
# ALGORITMO DE BÚSQUEDA HEURÍSTICA A*
# ============================================================

def heuristica(estacion, destino):
    """
    Heurística admisible: estimación basada en índice de posición
    en la línea troncal (simplificación para el modelo de conocimiento)
    """
    estaciones_linea = list(GRAFO_TRANSMILENIO.keys())
    try:
        pos_actual = estaciones_linea.index(estacion)
        pos_destino = estaciones_linea.index(destino)
        return abs(pos_actual - pos_destino) * 2
    except ValueError:
        return 0


def busqueda_a_estrella(inicio, fin, hora_pico=False):
    """
    Búsqueda A* con base de conocimiento para encontrar
    la ruta óptima entre dos estaciones.
    """
    factor = 1.5 if hora_pico else 1.0

    # Cola de prioridad: (costo_total_estimado, costo_real, estacion, ruta)
    cola = [(0 + heuristica(inicio, fin), 0, inicio, [inicio])]
    visitados = set()

    while cola:
        f, g, actual, ruta = heapq.heappop(cola)

        if actual in visitados:
            continue
        visitados.add(actual)

        # Meta alcanzada
        if actual == fin:
            return ruta, g

        # Expandir vecinos
        for vecino, costo in GRAFO_TRANSMILENIO.get(actual, []):
            if vecino not in visitados:
                nuevo_g = g + (costo * factor)
                nuevo_f = nuevo_g + heuristica(vecino, fin)
                heapq.heappush(cola, (nuevo_f, nuevo_g, vecino, ruta + [vecino]))

    return None, float('inf')  # No se encontró ruta


# ============================================================
# INTERFAZ DEL SISTEMA INTELIGENTE
# ============================================================

def mostrar_resultado(ruta, costo, hora_pico):
    """Presenta los resultados de forma clara"""
    print("=" * 60)
    print("   🚌 SISTEMA INTELIGENTE DE RUTAS - TRANSMILENIO")
    print("=" * 60)

    if ruta is None:
        print("❌ No se encontró una ruta entre las estaciones indicadas.")
        return

    print(f"\n📍 Ruta óptima encontrada ({len(ruta)} estaciones):\n")
    for i, estacion in enumerate(ruta):
        if i == 0:
            print(f"  🟢 INICIO → {estacion}")
        elif i == len(ruta) - 1:
            print(f"  🔴 DESTINO → {estacion}")
        else:
            print(f"  🔵 Paso {i}  → {estacion}")

    print(f"\n⏱️  Tiempo estimado: {costo:.1f} minutos")
    if hora_pico:
        print("⚠️  (Incluye factor hora pico +50%)")
    print(f"🔢 Total de transbordos: {len(ruta) - 1}")

    if costo > 60:
        print("\n💡 REGLA R3 activada: La ruta supera 60 min.")
        print("   Considera tomar un bus alimentador o combinar con SITP.")
    print("=" * 60)


def sistema_inteligente():
    """Función principal del sistema"""
    print("\n" + "=" * 60)
    print("   🧠 SISTEMA INTELIGENTE DE TRANSPORTE MASIVO")
    print("   Basado en reglas lógicas y búsqueda heurística A*")
    print("=" * 60)

    print("\n📋 Estaciones disponibles:")
    estaciones = list(GRAFO_TRANSMILENIO.keys())
    for i, est in enumerate(estaciones, 1):
        print(f"  {i:2}. {est}")

    print("\n")
    inicio = input("👉 Ingrese estación de ORIGEN:  ").strip()
    fin    = input("👉 Ingrese estación de DESTINO: ").strip()
    pico   = input("👉 ¿Es hora pico? (s/n):        ").strip().lower() == "s"

    # Aplicar motor de inferencia (reglas)
    valido, estado = aplicar_reglas(inicio, fin, pico)

    if estado == "MISMO_PUNTO":
        print("\n✅ Ya estás en tu destino. No necesitas tomar ninguna ruta.")
        return
    if estado == "ESTACION_INVALIDA":
        print(f"\n❌ Una de las estaciones no existe en el sistema.")
        print("   Verifica el nombre exacto de la estación.")
        return

    # Ejecutar búsqueda A*
    print("🔄 Ejecutando búsqueda A*...")
    ruta, costo = busqueda_a_estrella(inicio, fin, pico)
    mostrar_resultado(ruta, costo, pico)


# ============================================================
# CASOS DE PRUEBA AUTOMÁTICOS
# ============================================================

def ejecutar_pruebas():
    print("\n" + "=" * 60)
    print("   🧪 CASOS DE PRUEBA DEL SISTEMA")
    print("=" * 60)

    casos = [
        ("Portal Norte", "Calle 26",    False, "Ruta normal sin hora pico"),
        ("Portal Norte", "Portal Sur",  True,  "Ruta larga en hora pico"),
        ("Calle 85",     "Calle 85",    False, "Mismo origen y destino"),
        ("Portal 80",    "NQS Calle 30",False, "Ruta por ramal occidental"),
        ("Marly",        "Ricaurte",    True,  "Ruta corta centro con hora pico"),
        ("Granja",       "Portal Sur",  False, "Ruta ramal occidental y troncal sur"),
    ]

    for inicio, fin, pico, descripcion in casos:
        print(f"\n📌 Prueba: {descripcion}")
        print(f"   De: {inicio}  →  A: {fin}  | Hora pico: {'Sí' if pico else 'No'}")
        valido, estado = aplicar_reglas(inicio, fin, pico)
        if estado == "MISMO_PUNTO":
            print("   ✅ Resultado: Mismo punto, sin ruta necesaria.")
        elif estado == "ESTACION_INVALIDA":
            print("   ❌ Resultado: Estación no válida.")
        else:
            ruta, costo = busqueda_a_estrella(inicio, fin, pico)
            if ruta:
                print(f"   ✅ Ruta: {' → '.join(ruta)}")
                print(f"   ⏱️  Tiempo: {costo:.1f} min | Paradas: {len(ruta)}")
                if costo > 60:
                    print("   💡 REGLA R3 activada: La ruta supera 60 min. Se sugiere ruta alterna.")
            else:
                print("   ❌ No se encontró ruta.")


# ============================================================
# PUNTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    print("\n¿Qué deseas ejecutar?")
    print("  1. Sistema interactivo (ingresar origen y destino)")
    print("  2. Ejecutar casos de prueba automáticos")
    opcion = input("Opción (1/2): ").strip()

    if opcion == "1":
        sistema_inteligente()
    elif opcion == "2":
        ejecutar_pruebas()
    else:
        print("Opción no válida.")
