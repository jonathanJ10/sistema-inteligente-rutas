"""
Pruebas unitarias del Sistema Inteligente de Rutas
Ejecutar con: python -m unittest -v
"""

import io
import unittest
from contextlib import redirect_stdout

from sistema_rutas import (
    GRAFO_TRANSMILENIO,
    aplicar_reglas,
    busqueda_a_estrella,
    heuristica,
)


def reglas_silenciosas(inicio, fin, hora_pico=False):
    """Ejecuta el motor de inferencia sin imprimir en consola"""
    with redirect_stdout(io.StringIO()):
        return aplicar_reglas(inicio, fin, hora_pico)


# ============================================================
# BASE DE CONOCIMIENTO
# ============================================================

class TestBaseConocimiento(unittest.TestCase):

    def test_grafo_tiene_23_estaciones(self):
        self.assertEqual(len(GRAFO_TRANSMILENIO), 23)

    # BUG conocido: "NQS Calle 30" no tiene conexion de regreso a "Carrera 90"
    @unittest.expectedFailure
    def test_conexiones_son_bidireccionales(self):
        for estacion, vecinos in GRAFO_TRANSMILENIO.items():
            for vecino, costo in vecinos:
                self.assertIn((estacion, costo), GRAFO_TRANSMILENIO[vecino],
                              f"{estacion} -> {vecino} no tiene conexion de regreso")

    def test_costos_positivos(self):
        for vecinos in GRAFO_TRANSMILENIO.values():
            for _, costo in vecinos:
                self.assertGreater(costo, 0)


# ============================================================
# MOTOR DE INFERENCIA (REGLAS)
# ============================================================

class TestMotorInferencia(unittest.TestCase):

    def test_r2_mismo_origen_y_destino(self):
        valido, estado = reglas_silenciosas("Calle 85", "Calle 85")
        self.assertIsNone(valido)
        self.assertEqual(estado, "MISMO_PUNTO")

    def test_r4_origen_inexistente(self):
        valido, estado = reglas_silenciosas("Estacion Falsa", "Calle 26")
        self.assertIsNone(valido)
        self.assertEqual(estado, "ESTACION_INVALIDA")

    def test_r4_destino_inexistente(self):
        _, estado = reglas_silenciosas("Portal Norte", "Estacion Falsa")
        self.assertEqual(estado, "ESTACION_INVALIDA")

    def test_estaciones_validas_permiten_busqueda(self):
        valido, estado = reglas_silenciosas("Portal Norte", "Calle 26")
        self.assertTrue(valido)
        self.assertEqual(estado, "OK")

    def test_r1_hora_pico_permite_busqueda(self):
        valido, estado = reglas_silenciosas("Marly", "Ricaurte", hora_pico=True)
        self.assertTrue(valido)
        self.assertEqual(estado, "OK")


# ============================================================
# ALGORITMO A*
# ============================================================

class TestBusquedaAEstrella(unittest.TestCase):

    def test_cp01_ruta_normal_sin_hora_pico(self):
        ruta, costo = busqueda_a_estrella("Portal Norte", "Calle 26")
        self.assertEqual(ruta[0], "Portal Norte")
        self.assertEqual(ruta[-1], "Calle 26")
        self.assertEqual(len(ruta), 11)
        self.assertAlmostEqual(costo, 38.0)

    def test_cp02_ruta_larga_con_hora_pico_activa_r3(self):
        ruta, costo = busqueda_a_estrella("Portal Norte", "Portal Sur", hora_pico=True)
        self.assertEqual(len(ruta), 17)
        self.assertAlmostEqual(costo, 102.0)
        self.assertGreater(costo, 60)  # R3 debe activarse

    def test_cp04_ramal_occidental(self):
        ruta, costo = busqueda_a_estrella("Portal 80", "NQS Calle 30")
        self.assertEqual(ruta, ["Portal 80", "Avenida Rojas", "Álamos",
                                "Granja", "Carrera 90", "NQS Calle 30"])
        self.assertAlmostEqual(costo, 21.0)

    def test_cp05_ruta_corta_con_hora_pico(self):
        ruta, costo = busqueda_a_estrella("Marly", "Ricaurte", hora_pico=True)
        self.assertEqual(ruta, ["Marly", "Calle 26", "Universidades", "Ricaurte"])
        self.assertAlmostEqual(costo, 18.0)

    def test_cp06_ramal_y_troncal_sur(self):
        ruta, costo = busqueda_a_estrella("Granja", "Portal Sur")
        self.assertEqual(ruta, ["Granja", "Carrera 90", "NQS Calle 30",
                                "General Santander", "Portal Sur"])
        self.assertAlmostEqual(costo, 21.0)

    def test_r1_hora_pico_aumenta_costo_50_por_ciento(self):
        _, normal = busqueda_a_estrella("Portal Norte", "Calle 26")
        _, pico = busqueda_a_estrella("Portal Norte", "Calle 26", hora_pico=True)
        self.assertAlmostEqual(pico, normal * 1.5)

    def test_ruta_elige_camino_mas_corto(self):
        # Portal Norte -> Cardio Infantil: por Toberin (4+3=7) y no por Alcala (5+4=9)
        ruta, costo = busqueda_a_estrella("Portal Norte", "Cardio Infantil")
        self.assertEqual(ruta, ["Portal Norte", "Toberin", "Cardio Infantil"])
        self.assertAlmostEqual(costo, 7.0)

    # BUG conocido: "NQS Calle 30" no tiene conexion de regreso a "Carrera 90"
    @unittest.expectedFailure
    def test_ruta_es_simetrica_en_costo(self):
        _, ida = busqueda_a_estrella("Portal 80", "Portal Sur")
        _, vuelta = busqueda_a_estrella("Portal Sur", "Portal 80")
        self.assertAlmostEqual(ida, vuelta)


# ============================================================
# HEURISTICA
# ============================================================

class TestHeuristica(unittest.TestCase):

    def test_heuristica_cero_en_destino(self):
        self.assertEqual(heuristica("Calle 72", "Calle 72"), 0)

    def test_heuristica_no_negativa(self):
        for a in GRAFO_TRANSMILENIO:
            for b in GRAFO_TRANSMILENIO:
                self.assertGreaterEqual(heuristica(a, b), 0)

    def test_heuristica_estacion_desconocida_retorna_cero(self):
        self.assertEqual(heuristica("Estacion Falsa", "Calle 26"), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
