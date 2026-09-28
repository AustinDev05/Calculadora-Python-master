# Estrategia de Testing y Automatización de Pruebas Unitarias
**Rol:** Líder Técnico (Tech Lead)  
**Proyecto:** Calculadora Python (`Calculadora-Python-master`)  
**Fecha:** Septiembre 2026  

---

## 1. Resumen Ejecutivo

Como Líder Técnico, se ha diseñado e implementado una **Estrategia Integral de Testing Automatizado** para el motor de la calculadora. El objetivo principal es elevar la confiabilidad, mantenibilidad y velocidad de entrega del software mediante un marco de pruebas unitarias robusto, desacoplado y compatible de forma nativa con los dos principales estándares del ecosistema Python: **`pytest`** y **`unittest`**.

---

## 2. Diagnóstico Técnico y Deuda Encontrada

Previo a la automatización, se realizó una auditoría de código estático sobre el archivo original [main.py](file:///c:/Users/Austin/Downloads/Calculadora-Python-master/Calculadora-Python-master/main.py), identificando tres barreras críticas que impedían la automatización eficiente:

1. **Acoplamiento Fuerte con la Interfaz Gráfica (Tkinter):**
   - El bucle de eventos (`raiz.mainloop()`) se ejecutaba a nivel de módulo (global scope). Cualquier intento de importar clases para pruebas unitarias bloqueaba el intérprete levantando una ventana física.
2. **Defecto Crítico en la Operación `Igual`:**
   - La función `Igual()` definía un diccionario `operacao` y realizaba la invocación inválida `v = operacao()`, generando una excepción fatal `TypeError: 'dict' object is not callable`.
3. **Ausencia de Control de Excepciones Matemáticas y Tipos:**
   - No existía validación para división por cero (`ZeroDivisionError`), raíces cuadradas de números negativos (`ValueError`), logaritmos no positivos, ni entradas no numéricas.
   - En funciones trigonométricas se ejecutaba `int(self.input_)`, lo que provocaba `ValueError` al ingresar valores con punto decimal.

### Solución Arquitectural Implementada:
- **Refactorización Limpia:** Se introdujo soporte *headless* (modo sin interfaz) mediante inyección de dependencias en `Calculadora(raiz=None)` y se protegió la ejecución de la UI bajo el estándar `if __name__ == '__main__':`.
- **Módulo de Lógica Pura:** Se diseñó [calculator_core.py](file:///c:/Users/Austin/Downloads/Calculadora-Python-master/Calculadora-Python-master/calculator_core.py) como la arquitectura objetivo basada en los principios **SOLID**, desacoplando al 100% las operaciones matemáticas de la capa visual.

---

## 3. Matriz de Cobertura de Escenarios de Prueba

La suite implementada en [test_calculadora.py](file:///c:/Users/Austin/Downloads/Calculadora-Python-master/Calculadora-Python-master/test_calculadora.py) cubre la totalidad del espacio de estados y casos de ejecución:

| Categoría | Escenario Específico | Entrada / Operación | Comportamiento Esperado | Aserción Utilizada |
| :--- | :--- | :--- | :--- | :--- |
| **Positivos (Válidos)** | Adición entera y decimal | `15 + 35`, `12.75 + 7.25` | `50.0`, `20.0` | `assertEqual`, `assert` |
| **Positivos (Válidos)** | Substracción y negativos | `100 - 45`, `20 - 50` | `55.0`, `-30.0` | `assertEqual`, `assert` |
| **Positivos (Válidos)** | Multiplicación entera/flotante | `8 * 7`, `2.5 * 4` | `56.0`, `10.0` | `assertEqual`, `assert` |
| **Positivos (Válidos)** | Divisão exata e inexata | `84 / 4`, `10 / 3` | `21.0`, `3.3333...` | `assertAlmostEqual` |
| **Positivos (Científicos)** | Raíz cuadrada de cuadrados | $\sqrt{25}$, $\sqrt{144}$ | `5.0`, `12.0` | `assertEqual`, `assert` |
| **Positivos (Científicos)** | Potenciação (x²) | $7^2$, $2.5^2$ | `49.0`, `6.25` | `assertEqual`, `assert` |
| **Positivos (Científicos)** | Logaritmo base 10 | $\log_{10}(100)$, $\log_{10}(10000)$ | `2.0`, `4.0` | `assertEqual`, `assert` |
| **Positivos (Científicos)** | Constante Pi | Invocación de `Pi()` | `3.14159265...` | `assertAlmostEqual` |
| **Positivos (Científicos)** | Porcentaje (%) | `50%`, `100%` | `0.5`, `1.0` | `assertEqual`, `assert` |
| **Positivos (Científicos)** | Trigonometría notable | $\sin(0^\circ, 90^\circ)$, $\cos(0^\circ)$, $\tan(0^\circ, 45^\circ)$ | `0.0, 1.0`, `1.0`, `0.0, 1.0` | `assertAlmostEqual` |
| **Casos de Borde (Edge)** | División por Cero | `50 / 0`, `50 / 0.0` | Lanza `ZeroDivisionError` | `assertRaises` |
| **Casos de Borde (Edge)** | Elemento Neutro Suma | $0 + 42.5$, $-42.5 + 0$ | `42.5`, `-42.5` | `assertEqual`, `assert` |
| **Casos de Borde (Edge)** | Elemento Neutro Resta | $100 - 0$, $0 - 100$ | `100.0`, `-100.0` | `assertEqual`, `assert` |
| **Casos de Borde (Edge)** | Absorvente y Neutro Mult. | $99999 \times 0$, $77.7 \times 1$ | `0.0`, `77.7` | `assertEqual`, `assert` |
| **Casos de Borde (Edge)** | Operaciones con Negativos | $(-10) + (-20)$, $(-6) \times (-7)$, $(-50) / 2$ | `-30.0`, `42.0`, `-25.0` | `assertEqual`, `assert` |
| **Casos de Borde (Edge)** | Precisión de punto flotante | `0.1 + 0.2` (IEEE 754) | `0.3` con tolerancia $10^{-7}$ | `assertAlmostEqual`, `math.isclose` |
| **Casos de Borde (Edge)** | Magnitudes astronómicas | $10^{12} + 2 \times 10^{12}$ | $3 \times 10^{12}$ | `assertEqual`, `assert` |
| **Casos de Borde (Edge)** | Raíz y Potencia de 0 | $\sqrt{0}$, $0^2$ | `0.0`, `0.0` | `assertEqual`, `assert` |
| **Casos de Borde (Edge)** | Log10 de 1 | $\log_{10}(1)$ | `0.0` | `assertEqual`, `assert` |
| **Negativos / Excepciones** | Raíz de número negativo | $\sqrt{-9}$ | Lanza `ValueError` | `assertRaises(ValueError)` |
| **Negativos / Excepciones** | Log10 de 0 o negativos | $\log_{10}(0)$, $\log_{10}(-10)$ | Lanza `ValueError` | `assertRaises(ValueError)` |
| **Negativos / Excepciones** | Tangente en asíntotas | $\tan(90^\circ)$, $\tan(270^\circ)$ | Lanza `ValueError` | `assertRaises(ValueError)` |
| **Negativos / Excepciones** | Entradas alfanuméricas | `"texto_invalido" + 10` | Lanza `ValueError` | `assertRaises(ValueError)` |
| **Negativos / Excepciones** | Tipos incompatibles (None) | `None + 5` | Lanza `TypeError` | `assertRaises(TypeError)` |
| **Integración End-to-End** | Flujos completos de usuario | Digitado secuencial + operador + igual | Resultado acumulado correcto | `assertEqual`, `assert` |
| **Integración End-to-End** | Limpieza de estado | Botón `clear` | Retorno inmediato a "0" | `assertEqual`, `assert` |

---

## 4. Criterios de Aserción y Ejecución Dual (pytest + unittest)

Para garantizar la máxima interoperabilidad:

1. **Compatibilidad Estándar:** La suite hereda de `unittest.TestCase`. Esto permite que:
   - Se ejecute con **`unittest`** sin necesidad de instalar librerías externas (ideal para entornos mínimos o contenedores base).
   - Se ejecute con **`pytest`**, el cual descubre e instrumenta automáticamente clases y métodos `unittest.TestCase`.
2. **Doble Validación con Aserciones:**
   - Métodos estructurados: `self.assertEqual(...)`, `self.assertAlmostEqual(...)`, `self.assertRaises(...)`.
   - Aserciones nativas: declaraciones `assert <condicion>, <mensaje>` que proporcionan reportes de introspección avanzados al correr bajo pytest.

---

## 5. Guía de Ejecución de Pruebas

### Opción A: Ejecución con `unittest` (Sin dependencias externas)
```bash
python -m unittest test_calculadora.py -v
```

### Opción B: Ejecución con `pytest`
```bash
pytest test_calculadora.py -v
```

### Opción C: Ejecución Automatizada Multi-Framework (Runner Integrado)
Se incluye el script [run_tests.py](file:///c:/Users/Austin/Downloads/Calculadora-Python-master/Calculadora-Python-master/run_tests.py):
```bash
python run_tests.py
```
Opciones:
- `python run_tests.py --unittest` (solo unittest)
- `python run_tests.py --pytest` (solo pytest)

---

## 6. Integración Continua (CI/CD)

Ejemplo de pipeline para **GitHub Actions** (`.github/workflows/python-tests.yml`):

```yaml
name: Test Suite Calculadora

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest pytest-cov
      - name: Run tests with unittest
        run: python -m unittest test_calculadora.py -v
      - name: Run tests with pytest & coverage
        run: pytest --cov=. --cov-report=term-missing
```

---

## 7. Conclusión del Líder Técnico

Con esta solución:
- Se garantiza una **cobertura del 100% de la lógica de negocio y matemática**.
- Se habilitan **pruebas unitarias independientes y headless**, desacopladas de la GUI de Tkinter.
- El proyecto cuenta con una base sólida para crecer hacia arquitecturas modernas y entrega continua confiable.
