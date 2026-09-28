from tkinter import *
import itertools
import math

class Calculadora():
    def __init__(self, raiz=None):
        self.raiz = raiz
        self.input_ = "0" 
        self.soma = Celula()
        
        if raiz is not None:
            caixa_texto = Texto(raiz, self.input_) 

            def novo_botao(text, row, column, function):
                return Botao(raiz, text, row, column, function)

            def input_numero(numero):
                return lambda : self.Numero(numero)
            
            buttons = {}

            numbers_positions = list(itertools.product([3, 4, 5], [2, 3, 4]))
            for numero in range(1, 10):
                buttons.update({str(numero) : (*numbers_positions[numero-1], input_numero(numero))})
            
            buttons.update({"0": (5, 5, input_numero(0))})

            buttons.update({
                "pi()": (2, 1, self.Pi),
                "x²": (2, 2, self.Pow),
                "log10()": (2, 3, self.Log10),
                "%": (2, 4, self.Percentual),
                "raiz()": (2, 5, self.Raiz_Quadrada),
                "clear": (2, 6, self.clear_),
                "sen()": (3, 1, self.Seno),
                "cos()": (4, 1, self.Cosseno),
                "tg()": (5, 1, self.Tangente)
            })
            
            for button in buttons.keys():
                novo_botao(button, *buttons[button])

    def _render_display(self, valor):
        if self.raiz is not None:
            Texto(self.raiz, valor)

    def clear_(self):
        self.input_ = "0"
        self._render_display(self.input_)
        return self.input_

    def Raiz_Quadrada(self):
        val = float(self.input_)
        if val < 0:
            raise ValueError("math domain error: raiz quadrada de número negativo não permitida")
        temporario = math.sqrt(val)
        self.input_ = str(temporario)
        self._render_display(self.input_)
        return temporario

    def Seno(self):
        temporario = ((float(self.input_)) * 2 * math.pi) / 360
        res = math.sin(temporario)
        self.input_ = str(res)
        self._render_display(self.input_)
        return res
        
    def Cosseno(self):
        temporario = ((float(self.input_)) * 2 * math.pi) / 360
        res = math.cos(temporario)
        self.input_ = str(res)
        self._render_display(self.input_)
        return res

    def Tangente(self):
        angulo = float(self.input_)
        if (angulo - 90) % 180 == 0:
            raise ValueError(f"Tangente indefinida para {angulo} graus")
        temporario = (angulo * 2 * math.pi) / 360
        res = math.tan(temporario)
        self.input_ = str(res)
        self._render_display(self.input_)
        return res

    def Log10(self):
        val = float(self.input_)
        if val <= 0:
            raise ValueError("math domain error: logaritmo de número não positivo não permitido")
        temporario = math.log10(val)
        self.input_ = str(temporario)
        self._render_display(self.input_)
        return temporario

    def Pi(self):
        self.input_ = str(math.pi)
        self._render_display(self.input_)
        return math.pi
        
    def Pow(self):
        temporario = math.pow(float(self.input_), 2)
        self.input_ = str(temporario)
        self._render_display(self.input_)
        return temporario

    def Percentual(self):
        temporario = float(self.input_) / 100
        self.input_ = str(temporario)
        self._render_display(self.input_)
        return temporario

    def Igual(self):
        self.soma._numero_B = self.input_
        soma = self.soma
        operacao = {"soma": soma.soma,
                    "subtracao": soma.subtracao,
                    "multiplicacao": soma.multiplicacao,
                    "divisao": soma.divisao}
        if soma._sinal in operacao:
            v = operacao[soma._sinal]()
        else:
            v = float(self.input_)
        self.input_ = str(v)
        self._render_display(v)
        return v

    def Soma(self):
        self.soma._numero_A = self.input_
        self.soma._sinal = "soma"
        self.input_ = "0"

    def Multiplicacao(self):
        self.soma._numero_A = self.input_
        self.soma._sinal = "multiplicacao"
        self.input_ = "0"

    def Divisao(self):
        self.soma._numero_A = self.input_
        self.soma._sinal = "divisao"
        self.input_ = "0"

    def Subtracao(self):
        self.soma._numero_A = self.input_
        self.soma._sinal = "subtracao"
        self.input_ = "0"

    def Numero(self, numero):
        if self.input_ == "0":
            self.input_ = str(numero)
        else:
            self.input_ += str(numero)
        self._render_display(self.input_)
        return self.input_


class Botao():
    def __init__(self, frame, text_botao, linha, coluna, comando):
        self.button = Button(frame, text = text_botao, fg="black", bg="grey", command = comando, font = ("Arial", "20", "bold"))
        self.button["width"] = 5
        self.button["height"] = 1
        self.button.grid(row = linha, column = coluna)

class Celula():
    def __init__(self):
        self._numero_A = None
        self._numero_B = None
        self._sinal = None

    def soma(self):
        return float(self._numero_A) + float(self._numero_B)

    def subtracao(self):
        return float(self._numero_A) - float(self._numero_B)

    def multiplicacao(self):
        return float(self._numero_A) * float(self._numero_B)
    
    def divisao(self):
        divisor = float(self._numero_B)
        if divisor == 0.0:
            raise ZeroDivisionError("Divisão por zero não permitida")
        return float(self._numero_A) / divisor

class Texto():
    def __init__(self, raiz, texto):
        self.texto = Label(raiz, text = round(float(texto), 5), font = ("Arial", "72", "bold"))
        self.texto["height"] = 2 
        self.texto["width"] = 2
        self.texto.grid(row=1, column=1, columnspan=6, sticky=W+E+N+S)


if __name__ == "__main__":
    raiz = Tk()
    raiz.title("Calculadora")
    raiz.geometry("570x452")
    m = Calculadora(raiz)
    raiz.mainloop()
