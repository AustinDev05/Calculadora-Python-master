"""
Script Automatizador de Ejecución de Pruebas Unitarias
------------------------------------------------------
Permite ejecutar la suite completa de pruebas con:
1. unittest (Biblioteca estándar de Python)
2. pytest (Framework moderno de testing, si está instalado)

Uso:
    python run_tests.py            # Ejecuta con unittest y pytest si está disponible
    python run_tests.py --unittest # Ejecuta exclusivamente con unittest
    python run_tests.py --pytest   # Ejecuta exclusivamente con pytest
"""

import sys
import time
import unittest


def ejecutar_con_unittest() -> bool:
    """Ejecuta los tests usando el runner de unittest estándar."""
    print("=" * 70)
    print("EJECUTANDO SUITE CON UNITTEST (Standard Library)")
    print("=" * 70)
    
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=".", pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    
    inicio = time.time()
    resultado = runner.run(suite)
    duracion = time.time() - inicio
    
    print("-" * 70)
    print(f"Resumen unittest:")
    print(f"  - Pruebas ejecutadas: {resultado.testsRun}")
    print(f"  - Exitosas:           {resultado.testsRun - len(resultado.failures) - len(resultado.errors)}")
    print(f"  - Fallos:             {len(resultado.failures)}")
    print(f"  - Errores:            {len(resultado.errors)}")
    print(f"  - Tiempo total:       {duracion:.4f} segundos")
    print("=" * 70)
    
    return resultado.wasSuccessful()


def ejecutar_con_pytest() -> bool:
    """Ejecuta los tests usando pytest si se encuentra instalado."""
    print("\n" + "=" * 70)
    print("EJECUTANDO SUITE CON PYTEST")
    print("=" * 70)
    
    try:
        import pytest
        inicio = time.time()
        codigo_salida = pytest.main(["-v", "test_calculadora.py"])
        duracion = time.time() - inicio
        print("-" * 70)
        print(f"Resumen pytest:")
        print(f"  - Código de salida: {codigo_salida}")
        print(f"  - Tiempo total:     {duracion:.4f} segundos")
        print("=" * 70)
        return codigo_salida == 0
    except ImportError:
        print("[AVISO] 'pytest' no está instalado en este entorno de Python.")
        print("Para instalarlo ejecute: pip install pytest")
        print("La suite se ejecuta 100% compatible mediante unittest.")
        print("=" * 70)
        return True


def main():
    args = sys.argv[1:]
    unittest_ok = True
    pytest_ok = True
    
    if "--pytest" in args:
        pytest_ok = ejecutar_con_pytest()
        sys.exit(0 if pytest_ok else 1)
    elif "--unittest" in args:
        unittest_ok = ejecutar_con_unittest()
        sys.exit(0 if unittest_ok else 1)
    else:
        unittest_ok = ejecutar_con_unittest()
        pytest_ok = ejecutar_con_pytest()
        sys.exit(0 if (unittest_ok and pytest_ok) else 1)


if __name__ == "__main__":
    main()
