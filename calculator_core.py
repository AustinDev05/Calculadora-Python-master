"""
Módulo Core da Calculadora - Lógica de Negócio Desacoplada da Interface Gráfica.

Este módulo implementa o motor de cálculo da aplicação, isolando as operações
matemáticas de qualquer dependência visual (Tkinter). Esta separação segue os
princípios de Clean Architecture e Single Responsibility Principle (SRP),
permitindo a execução de testes unitários rápidos, confiáveis e adequados para
ambientes de Integração Contínua (CI/CD).
"""

import math
from typing import Union, Optional

NumberType = Union[int, float, str]


def _to_float(value: NumberType) -> float:
    """
    Converte um valor de entrada para float com validação rigorosa de tipo.
    
    Lança:
        TypeError: se o valor for None ou de tipo não suportado.
        ValueError: se a string não puder ser convertida para float.
    """
    if value is None:
        raise TypeError("O valor de entrada não pode ser None")
    try:
        return float(value)
    except (TypeError, ValueError) as err:
        raise type(err)(f"Valor numérico inválido: '{value}'") from err


class Celula:
    """
    Entidade responsável por armazenar operandos e executar operações aritméticas básicas.
    """
    def __init__(self):
        self._numero_A: Optional[NumberType] = None
        self._numero_B: Optional[NumberType] = None
        self._sinal: Optional[str] = None

    def soma(self) -> float:
        """Executa a adição entre _numero_A e _numero_B."""
        a = _to_float(self._numero_A)
        b = _to_float(self._numero_B)
        return a + b

    def subtracao(self) -> float:
        """Executa a subtração (_numero_A - _numero_B)."""
        a = _to_float(self._numero_A)
        b = _to_float(self._numero_B)
        return a - b

    def multiplicacao(self) -> float:
        """Executa a multiplicação entre _numero_A e _numero_B."""
        a = _to_float(self._numero_A)
        b = _to_float(self._numero_B)
        return a * b

    def divisao(self) -> float:
        """
        Executa a divisão (_numero_A / _numero_B).
        
        Lança:
            ZeroDivisionError: Se o divisor (_numero_B) for igual a zero.
        """
        a = _to_float(self._numero_A)
        b = _to_float(self._numero_B)
        if b == 0.0:
            raise ZeroDivisionError("Divisão por zero não permitida")
        return a / b


class CalculatorEngine:
    """
    Motor matemático que concentra as operações científicas e de estado da calculadora.
    """

    @staticmethod
    def raiz_quadrada(valor: NumberType) -> float:
        """
        Calcula a raiz quadrada de um número.
        
        Lança:
            ValueError: Se o valor for negativo (fora do domínio real).
        """
        num = _to_float(valor)
        if num < 0:
            raise ValueError("math domain error: raiz quadrada de número negativo não permitida")
        return math.sqrt(num)

    @staticmethod
    def seno(graus: NumberType) -> float:
        """Calcula o seno de um ângulo fornecido em graus."""
        deg = _to_float(graus)
        rad = math.radians(deg)
        return math.sin(rad)

    @staticmethod
    def cosseno(graus: NumberType) -> float:
        """Calcula o cosseno de um ângulo fornecido em graus."""
        deg = _to_float(graus)
        rad = math.radians(deg)
        return math.cos(rad)

    @staticmethod
    def tangente(graus: NumberType) -> float:
        """
        Calcula a tangente de um ângulo fornecido em graus.
        
        Lança:
            ValueError: Se o ângulo for um múltiplo ímpar de 90° (onde a tangente é indefinida).
        """
        deg = _to_float(graus)
        # Asíntotas: 90, 270, -90, -270 (+- 180*k)
        if abs((deg - 90) % 180) < 1e-9 or abs((deg + 90) % 180) < 1e-9:
            raise ValueError(f"Tangente indefinida para {deg}°")
        rad = math.radians(deg)
        return math.tan(rad)

    @staticmethod
    def log10(valor: NumberType) -> float:
        """
        Calcula o logaritmo na base 10.
        
        Lança:
            ValueError: Se o valor for menor ou igual a zero.
        """
        num = _to_float(valor)
        if num <= 0:
            raise ValueError("math domain error: logaritmo de número não positivo não permitido")
        return math.log10(num)

    @staticmethod
    def pi() -> float:
        """Retorna o valor da constante matemática Pi."""
        return math.pi

    @staticmethod
    def potencia(valor: NumberType, expoente: NumberType = 2) -> float:
        """Calcula a potência (valor ^ expoente). Padrão: expoente 2 (x²)."""
        base = _to_float(valor)
        exp = _to_float(expoente)
        return math.pow(base, exp)

    @staticmethod
    def percentual(valor: NumberType) -> float:
        """Calcula o percentual (valor / 100)."""
        num = _to_float(valor)
        return num / 100.0
