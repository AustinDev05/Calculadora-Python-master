"""
Suíte de Testes Automatizados para a Calculadora Python
-------------------------------------------------------
Implementada segundo as diretrizes de Liderança Técnica e Engenharia de Qualidade (QA):
- Executável nativamente tanto com 'pytest' quanto com 'unittest'.
- Cobertura exaustiva: Casos Positivos, Negativos, Casos de Borda (Edge Cases) e Tratamento de Exceções.
- Uso de asserções padrão do unittest e validações explícitas com a palavra-chave 'assert'.
"""

import math
import unittest
from main import Celula, Calculadora
from calculator_core import Celula as CoreCelula, CalculatorEngine


class TestCelulaOperacoesBasicas(unittest.TestCase):
    """
    Testes de unidade para operações aritméticas básicas da classe Celula.
    Verifica conformidade funcional, limites numéricos e lançamento de exceções.
    """

    def setUp(self):
        """Inicializa instâncias limpas antes de cada teste."""
        self.celula = Celula()
        self.core_celula = CoreCelula()

    # =========================================================================
    # 1. CENÁRIOS POSITIVOS (Valores Válidos)
    # =========================================================================

    def test_soma_valores_positivos_validos(self):
        """Valida a adição com números inteiros e decimais positivos."""
        # Teste com inteiros
        self.celula._numero_A = "15"
        self.celula._numero_B = "35"
        resultado = self.celula.soma()
        self.assertEqual(resultado, 50.0)
        assert resultado == 50.0, f"Esperado 50.0, obtido {resultado}"

        # Teste com decimais
        self.celula._numero_A = "12.75"
        self.celula._numero_B = "7.25"
        resultado_float = self.celula.soma()
        self.assertEqual(resultado_float, 20.0)
        assert resultado_float == 20.0

    def test_subtracao_valores_positivos_validos(self):
        """Valida a subtração com números onde A > B e A < B."""
        self.celula._numero_A = "100"
        self.celula._numero_B = "45"
        resultado = self.celula.subtracao()
        self.assertEqual(resultado, 55.0)
        assert resultado == 55.0

        # Subtração resultando em negativo
        self.celula._numero_A = "20"
        self.celula._numero_B = "50"
        resultado_neg = self.celula.subtracao()
        self.assertEqual(resultado_neg, -30.0)
        assert resultado_neg == -30.0

    def test_multiplicacao_valores_positivos_validos(self):
        """Valida a multiplicação entre números inteiros e de ponto flutuante."""
        self.celula._numero_A = "8"
        self.celula._numero_B = "7"
        resultado = self.celula.multiplicacao()
        self.assertEqual(resultado, 56.0)
        assert resultado == 56.0

        self.celula._numero_A = "2.5"
        self.celula._numero_B = "4"
        resultado_float = self.celula.multiplicacao()
        self.assertEqual(resultado_float, 10.0)
        assert resultado_float == 10.0

    def test_divisao_valores_positivos_validos(self):
        """Valida a divisão exata e inexata com números positivos válidos."""
        self.celula._numero_A = "84"
        self.celula._numero_B = "4"
        resultado = self.celula.divisao()
        self.assertEqual(resultado, 21.0)
        assert resultado == 21.0

        # Divisão inexata com validação de precisão
        self.celula._numero_A = "10"
        self.celula._numero_B = "3"
        resultado_frac = self.celula.divisao()
        self.assertAlmostEqual(resultado_frac, 3.33333, places=4)
        assert round(resultado_frac, 4) == 3.3333

    # =========================================================================
    # 2. CENÁRIOS DE BORDA (Edge & Boundary Cases)
    # =========================================================================

    def test_divisao_por_zero_lanca_excecao(self):
        """Caso de Borda Crítico: divisão por zero deve lançar ZeroDivisionError."""
        self.celula._numero_A = "50"
        self.celula._numero_B = "0"
        with self.assertRaises(ZeroDivisionError):
            self.celula.divisao()

        # Também para valor em ponto flutuante zero
        self.celula._numero_B = "0.0"
        with self.assertRaises(ZeroDivisionError):
            self.celula.divisao()

    def test_soma_elemento_neutro_zero(self):
        """Caso de Borda: 0 como elemento neutro na adição."""
        self.celula._numero_A = "0"
        self.celula._numero_B = "42.5"
        self.assertEqual(self.celula.soma(), 42.5)
        assert self.celula.soma() == 42.5

        self.celula._numero_A = "-42.5"
        self.celula._numero_B = "0"
        self.assertEqual(self.celula.soma(), -42.5)
        assert self.celula.soma() == -42.5

    def test_subtracao_elemento_neutro_zero(self):
        """Caso de Borda: operação de subtração envolvendo o número zero."""
        self.celula._numero_A = "100"
        self.celula._numero_B = "0"
        self.assertEqual(self.celula.subtracao(), 100.0)
        assert self.celula.subtracao() == 100.0

        self.celula._numero_A = "0"
        self.celula._numero_B = "100"
        self.assertEqual(self.celula.subtracao(), -100.0)
        assert self.celula.subtracao() == -100.0

    def test_multiplicacao_por_zero_e_por_um(self):
        """Caso de Borda: elemento absorvente (0) e elemento neutro (1)."""
        # Multiplicação por 0
        self.celula._numero_A = "99999"
        self.celula._numero_B = "0"
        self.assertEqual(self.celula.multiplicacao(), 0.0)
        assert self.celula.multiplicacao() == 0.0

        # Multiplicação por 1
        self.celula._numero_A = "77.7"
        self.celula._numero_B = "1"
        self.assertEqual(self.celula.multiplicacao(), 77.7)
        assert self.celula.multiplicacao() == 77.7

    def test_operacoes_com_numeros_negativos(self):
        """Caso de Borda: operações entre dois números negativos e de sinais opostos."""
        # Soma de negativos: (-10) + (-20) = -30
        self.celula._numero_A = "-10"
        self.celula._numero_B = "-20"
        self.assertEqual(self.celula.soma(), -30.0)
        assert self.celula.soma() == -30.0

        # Multiplicação de dois negativos: (-6) * (-7) = 42
        self.celula._numero_A = "-6"
        self.celula._numero_B = "-7"
        self.assertEqual(self.celula.multiplicacao(), 42.0)
        assert self.celula.multiplicacao() == 42.0

        # Divisão com números negativos: (-50) / (2) = -25
        self.celula._numero_A = "-50"
        self.celula._numero_B = "2"
        self.assertEqual(self.celula.divisao(), -25.0)
        assert self.celula.divisao() == -25.0

    def test_precisao_flutuante_pequena(self):
        """Caso de Borda: precisão de ponto flutuante padrão IEEE 754."""
        self.celula._numero_A = "0.1"
        self.celula._numero_B = "0.2"
        resultado = self.celula.soma()
        self.assertAlmostEqual(resultado, 0.3, places=7)
        assert math.isclose(resultado, 0.3, rel_tol=1e-9)

    def test_valores_numericos_muito_grandes(self):
        """Caso de Borda: cálculos com ordens de grandeza elevadas (1e12)."""
        self.celula._numero_A = "1000000000000"
        self.celula._numero_B = "2000000000000"
        resultado = self.celula.soma()
        self.assertEqual(resultado, 3000000000000.0)
        assert resultado == 3e12

    # =========================================================================
    # 3. CENÁRIOS NEGATIVOS (Tratamento de Exceções e Entradas Inválidas)
    # =========================================================================

    def test_entradas_nao_numericas_lancam_excecao(self):
        """Cenário Negativo: strings alfanuméricas devem gerar ValueError."""
        self.celula._numero_A = "texto_invalido"
        self.celula._numero_B = "10"
        with self.assertRaises(ValueError):
            self.celula.soma()

        self.celula._numero_A = "10"
        self.celula._numero_B = "outro_erro"
        with self.assertRaises(ValueError):
            self.celula.multiplicacao()

    def test_entrada_none_lanca_excecao(self):
        """Cenário Negativo: valores None devem gerar TypeError."""
        self.celula._numero_A = None
        self.celula._numero_B = "5"
        with self.assertRaises(TypeError):
            self.celula.soma()


class TestOperacoesCientificas(unittest.TestCase):
    """
    Testes de unidade para funções matemáticas científicas:
    Raiz quadrada, Potência, Log10, Constante Pi, Porcentagem e Trigonometria.
    """

    def setUp(self):
        """Cria calculadora headless sem interface gráfica."""
        self.calc = Calculadora(raiz=None)

    # =========================================================================
    # 1. CENÁRIOS POSITIVOS (Valores Válidos)
    # =========================================================================

    def test_raiz_quadrada_quadrados_perfeitos(self):
        """Valida a raiz quadrada de números positivos conhecidos."""
        self.calc.input_ = "25"
        resultado = self.calc.Raiz_Quadrada()
        self.assertEqual(resultado, 5.0)
        assert resultado == 5.0
        assert self.calc.input_ == "5.0"

        self.calc.input_ = "144"
        resultado = self.calc.Raiz_Quadrada()
        self.assertEqual(resultado, 12.0)
        assert resultado == 12.0

    def test_potencia_quadrado(self):
        """Valida a potenciação ao quadrado (x²)."""
        self.calc.input_ = "7"
        resultado = self.calc.Pow()
        self.assertEqual(resultado, 49.0)
        assert resultado == 49.0

        self.calc.input_ = "2.5"
        resultado = self.calc.Pow()
        self.assertEqual(resultado, 6.25)
        assert resultado == 6.25

    def test_log10_valores_validos(self):
        """Valida o logaritmo base 10 para potências de 10."""
        self.calc.input_ = "100"
        resultado = self.calc.Log10()
        self.assertEqual(resultado, 2.0)
        assert resultado == 2.0

        self.calc.input_ = "10000"
        resultado = self.calc.Log10()
        self.assertEqual(resultado, 4.0)
        assert resultado == 4.0

    def test_constante_pi(self):
        """Valida a injeção da constante matemática Pi."""
        resultado = self.calc.Pi()
        self.assertAlmostEqual(resultado, math.pi, places=10)
        assert math.isclose(resultado, 3.1415926535, rel_tol=1e-5)

    def test_percentual_valores_validos(self):
        """Valida a divisão percentual por 100."""
        self.calc.input_ = "50"
        resultado = self.calc.Percentual()
        self.assertEqual(resultado, 0.5)
        assert resultado == 0.5

        self.calc.input_ = "100"
        resultado = self.calc.Percentual()
        self.assertEqual(resultado, 1.0)
        assert resultado == 1.0

    def test_trigonometria_angulos_notaveis(self):
        """Valida seno, cosseno e tangente para ângulos padrão (0°, 30°, 45°, 180°)."""
        # Seno de 0° = 0.0
        self.calc.input_ = "0"
        res_sen_0 = self.calc.Seno()
        self.assertAlmostEqual(res_sen_0, 0.0, places=5)
        assert math.isclose(res_sen_0, 0.0, abs_tol=1e-5)

        # Seno de 90° = 1.0
        self.calc.input_ = "90"
        res_sen_90 = self.calc.Seno()
        self.assertAlmostEqual(res_sen_90, 1.0, places=5)
        assert math.isclose(res_sen_90, 1.0, abs_tol=1e-5)

        # Cosseno de 0° = 1.0
        self.calc.input_ = "0"
        res_cos_0 = self.calc.Cosseno()
        self.assertAlmostEqual(res_cos_0, 1.0, places=5)
        assert math.isclose(res_cos_0, 1.0, abs_tol=1e-5)

        # Tangente de 0° = 0.0
        self.calc.input_ = "0"
        res_tg_0 = self.calc.Tangente()
        self.assertAlmostEqual(res_tg_0, 0.0, places=5)
        assert math.isclose(res_tg_0, 0.0, abs_tol=1e-5)

        # Tangente de 45° = 1.0
        self.calc.input_ = "45"
        res_tg_45 = self.calc.Tangente()
        self.assertAlmostEqual(res_tg_45, 1.0, places=5)
        assert math.isclose(res_tg_45, 1.0, abs_tol=1e-5)

    # =========================================================================
    # 2. CENÁRIOS DE BORDA (Edge & Boundary Cases)
    # =========================================================================

    def test_raiz_quadrada_de_zero(self):
        """Caso de Borda: raiz quadrada de 0 é exatamente 0.0."""
        self.calc.input_ = "0"
        resultado = self.calc.Raiz_Quadrada()
        self.assertEqual(resultado, 0.0)
        assert resultado == 0.0

    def test_potencia_de_zero_e_negativo(self):
        """Caso de Borda: 0² = 0 e (-x)² > 0."""
        self.calc.input_ = "0"
        self.assertEqual(self.calc.Pow(), 0.0)
        assert self.calc.Pow() == 0.0

        self.calc.input_ = "-5"
        resultado = self.calc.Pow()
        self.assertEqual(resultado, 25.0)
        assert resultado == 25.0

    def test_log10_de_um(self):
        """Caso de Borda: log10(1) = 0.0."""
        self.calc.input_ = "1"
        resultado = self.calc.Log10()
        self.assertEqual(resultado, 0.0)
        assert resultado == 0.0

    def test_percentual_zero_e_valores_extremos(self):
        """Caso de Borda: percentual de 0%, 250% e negativos."""
        self.calc.input_ = "0"
        self.assertEqual(self.calc.Percentual(), 0.0)
        assert self.calc.Percentual() == 0.0

        self.calc.input_ = "250"
        self.assertEqual(self.calc.Percentual(), 2.5)
        assert self.calc.Percentual() == 2.5

        self.calc.input_ = "-50"
        self.assertEqual(self.calc.Percentual(), -0.5)
        assert self.calc.Percentual() == -0.5

    # =========================================================================
    # 3. CENÁRIOS NEGATIVOS E EXCEÇÕES
    # =========================================================================

    def test_raiz_quadrada_numero_negativo_lanca_excecao(self):
        """Cenário Negativo: raiz de número negativo deve lançar ValueError."""
        self.calc.input_ = "-9"
        with self.assertRaises(ValueError):
            self.calc.Raiz_Quadrada()

    def test_log10_de_zero_ou_negativo_lanca_excecao(self):
        """Cenário Negativo: log10 de zero ou valores negativos é matematicamente indefinido."""
        self.calc.input_ = "0"
        with self.assertRaises(ValueError):
            self.calc.Log10()

        self.calc.input_ = "-10"
        with self.assertRaises(ValueError):
            self.calc.Log10()

    def test_tangente_noventa_graus_lanca_excecao(self):
        """Cenário Negativo: tangente de 90° e 270° é assintótica (indefinida)."""
        self.calc.input_ = "90"
        with self.assertRaises(ValueError):
            self.calc.Tangente()

        self.calc.input_ = "270"
        with self.assertRaises(ValueError):
            self.calc.Tangente()


class TestFluxoIntegradoCalculadora(unittest.TestCase):
    """
    Testes de integração end-to-end do fluxo da calculadora (interação por dígitos e operações).
    """

    def setUp(self):
        self.calc = Calculadora(raiz=None)

    def test_flujo_completo_adicao(self):
        """Simula: usuário digita 25 + 15 = 40.0"""
        self.calc.clear_()
        self.calc.Numero(2)
        self.calc.Numero(5)
        assert self.calc.input_ == "25"

        self.calc.Soma()
        assert self.calc.input_ == "0"
        assert self.calc.soma._numero_A == "25"
        assert self.calc.soma._sinal == "soma"

        self.calc.Numero(1)
        self.calc.Numero(5)
        assert self.calc.input_ == "15"

        resultado = self.calc.Igual()
        self.assertEqual(resultado, 40.0)
        assert resultado == 40.0
        assert self.calc.input_ == "40.0"

    def test_flujo_completo_subtracao(self):
        """Simula: usuário digita 50 - 18 = 32.0"""
        self.calc.clear_()
        self.calc.Numero(5)
        self.calc.Numero(0)
        self.calc.Subtracao()
        self.calc.Numero(1)
        self.calc.Numero(8)
        resultado = self.calc.Igual()
        self.assertEqual(resultado, 32.0)
        assert resultado == 32.0

    def test_flujo_completo_multiplicacao(self):
        """Simula: usuário digita 9 * 8 = 72.0"""
        self.calc.clear_()
        self.calc.Numero(9)
        self.calc.Multiplicacao()
        self.calc.Numero(8)
        resultado = self.calc.Igual()
        self.assertEqual(resultado, 72.0)
        assert resultado == 72.0

    def test_flujo_completo_divisao(self):
        """Simula: usuário digita 100 / 4 = 25.0"""
        self.calc.clear_()
        self.calc.Numero(1)
        self.calc.Numero(0)
        self.calc.Numero(0)
        self.calc.Divisao()
        self.calc.Numero(4)
        resultado = self.calc.Igual()
        self.assertEqual(resultado, 25.0)
        assert resultado == 25.0

    def test_flujo_limpar_clear(self):
        """Valida se a função clear reseta o display para '0'."""
        self.calc.Numero(7)
        self.calc.Numero(8)
        self.assertEqual(self.calc.input_, "78")
        self.calc.clear_()
        self.assertEqual(self.calc.input_, "0")
        assert self.calc.input_ == "0"

    def test_flujo_divisao_por_zero_lanca_excecao(self):
        """Simula usuário tentando dividir por zero através do fluxo de botões."""
        self.calc.clear_()
        self.calc.Numero(1)
        self.calc.Numero(0)
        self.calc.Divisao()
        self.calc.Numero(0)
        with self.assertRaises(ZeroDivisionError):
            self.calc.Igual()


class TestDecoupledEngineCore(unittest.TestCase):
    """
    Testes de conformidade do motor desacoplado (calculator_core.py)
    projetado para arquitetura corporativa e pipelines de CI/CD.
    """

    def test_core_celula_adicao_e_divisao(self):
        core = CoreCelula()
        core._numero_A = 40
        core._numero_B = 10
        self.assertEqual(core.soma(), 50.0)
        self.assertEqual(core.divisao(), 4.0)
        assert core.soma() == 50.0
        assert core.divisao() == 4.0

    def test_core_celula_validacao_tipos_invalidos(self):
        core = CoreCelula()
        core._numero_A = None
        core._numero_B = 10
        with self.assertRaises(TypeError):
            core.soma()

        core._numero_A = "texto_invalido"
        with self.assertRaises(ValueError):
            core.soma()

    def test_core_engine_funcoes_cientificas(self):
        assert CalculatorEngine.raiz_quadrada(81) == 9.0
        assert CalculatorEngine.potencia(3, 3) == 27.0
        assert CalculatorEngine.percentual(25) == 0.25
        assert math.isclose(CalculatorEngine.cosseno(60), 0.5, abs_tol=1e-5)

        with self.assertRaises(ValueError):
            CalculatorEngine.raiz_quadrada(-16)

        with self.assertRaises(ValueError):
            CalculatorEngine.log10(-1)

        with self.assertRaises(ValueError):
            CalculatorEngine.tangente(90)


if __name__ == "__main__":
    unittest.main(verbosity=2)
