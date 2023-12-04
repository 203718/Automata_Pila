from PyQt5 import QtWidgets, uic
import re

gr_var = {
    "LR": r"[a-z][a-z0-9]*",
    "A": r"=",
    "CA": r'"[^"]*"',
    "IN": r"[0-9]+",
}

gr_if = {
    "PR": r"if",
    "PI": r"\(",
    "LR": r"[a-z][a-z]*",
    "DR": r"[0-9][0-9]*",
    "OP": r"<|>|==|!=",
    "PF": r"\)",
    "PA": r"\{\}",
}

gr_for = {
    "PR": r"for",
    "PI": r"\(",
    "VA": r"[a-z][a-z]*",
    "CM": r",",
    "VI": r"[0-9][0-9]*",
    "VF": r"[0-9][0-9]*",
    "PF": r"\)",
    "PA": r"\{\}",
}

gr_func = {
    "N": r"[a-z][a-z]*",
    "PI": r"\(",
    "PR": r"[a-z | 0-9][a-z | 0-9]*",
    "PF": r"\)",
    "PA": r"\{\}",
}

gr_main = {
    "PR": r"main",
    "P": r"\(\)",
    "PA": r"\{\}",
}



def validar_var(cadena):
    pila = [gr_var["LR"], gr_var["A"], (gr_var["IN"], gr_var["CA"])]
    pila_pasos = []
    bloques = cadena.split()

    while pila:
        cont = 0
        x = pila[cont]
        a = bloques[cont]

        if isinstance(x, tuple): 
            for option in x:
                if re.match(option, a):
                    pila.pop(0)
                    if a:
                        bloques = bloques[1:]
                    pila_pasos.append(next(key for key, value in gr_var.items() if value == option)) 
                    break 
        else:
            if re.match(x, a):
                pila.pop(0)
                if a:
                    bloques = bloques[1:]
                pila_pasos.append([key for key, value in gr_var.items() if value == x][0])
            else:
                return False, pila_pasos

    return True, pila_pasos

def validar_if(cadena):
    pila = [gr_if["PR"], gr_if["PI"], (gr_if["LR"], gr_if["DR"]), gr_if["OP"], (gr_if["LR"], gr_if["DR"]), gr_if["PF"], gr_if["PA"]]
    pila_pasos = []
    bloques = cadena.split()

    while pila:
        cont = 0
        x = pila[cont]
        a = bloques[cont]

        if isinstance(x, tuple):
            for option in x:
                if re.match(option, a):
                    pila.pop(0)
                    if a:
                        bloques = bloques[1:]
                    pila_pasos.append(next(key for key, value in gr_if.items() if value == option))
                    break
        else:
            if re.match(x, a):
                pila.pop(0)
                if a:
                    bloques = bloques[1:]
                pila_pasos.append([key for key, value in gr_if.items() if value == x][0])
            else:
                return False, pila_pasos
    return True, pila_pasos

def validar_for(cadena):
    pila = [gr_for["PR"], gr_for["PI"], gr_for["VA"], gr_for["CM"], gr_for["VI"], gr_for["CM"], gr_for["VF"], gr_for["PF"], gr_for["PA"]]
    pila_pasos = []
    bloques = cadena.split()

    while pila:
        cont = 0
        x = pila[cont]
        a = bloques[cont]

        if isinstance(x, tuple):
            for option in x:
                if re.match(option, a):
                    pila.pop(0)
                    if a:
                        bloques = bloques[1:]
                    pila_pasos.append(next(key for key, value in gr_for.items() if value == option))
                    break
        else:
            if re.match(x, a):
                pila.pop(0)
                if a:
                    bloques = bloques[1:]
                pila_pasos.append([key for key, value in gr_for.items() if value == x][0])
            else:
                return False, pila_pasos
    return True, pila_pasos


def validar_func(cadena):
    pila = [gr_func["N"], gr_func["PI"], gr_func["PR"], gr_func["PF"], gr_func["PA"]]
    pila_pasos = []
    bloques = cadena.split()

    while pila:
        cont = 0
        x = pila[cont]
        a = bloques[cont]

        if isinstance(x, tuple):
            for option in x:
                if re.match(option, a):
                    pila.pop(0)
                    if a:
                        bloques = bloques[1:]
                    pila_pasos.append(next(key for key, value in gr_func.items() if value == option))
                    break
        else:
            if re.match(x, a):
                pila.pop(0)
                if a:
                    bloques = bloques[1:]
                pila_pasos.append([key for key, value in gr_func.items() if value == x][0])
            else:
                return False, pila_pasos
    return True, pila_pasos


def validar_main(cadena):
    pila = [gr_main["PR"], gr_main["P"], gr_main["PA"]]
    pila_pasos = []
    bloques = cadena.split()

    while pila:
        cont = 0
        x = pila[cont]
        a = bloques[cont]

        if isinstance(x, tuple):
            match_found = False
            for option in x:
                if re.match(option, a):
                    match_found = True
                    pila.pop(0)
                    if a:
                        bloques = bloques[1:]
                    pila_pasos.append(next(key for key, value in gr_main.items() if value == option))
                    break
            if not match_found:
                return False, []  # Cadena inválida
        else:
            if re.match(x, a):
                pila.pop(0)
                if a:
                    bloques = bloques[1:]
                pila_pasos.append([key for key, value in gr_main.items() if value == x][0])
            else:
                return False, pila_pasos
            
    return True, pila_pasos

def determinar_tipo_cadena(cadena):
    if cadena.startswith("if"):
        return "if"
    elif cadena.startswith("for"):
        return "for"
    elif cadena.startswith("main"):
        return "main"
    elif re.match(r"[a-z][a-z0-9]*", cadena):
        if "(" in cadena:
            return "funcion"
        else:
            return "variable"
    else:
        return "desconocido"
    
def validar_cadena(cadena):
    tipo = determinar_tipo_cadena(cadena)
    if tipo == "variable":
        return validar_var(cadena)
    elif tipo == "if":
        return validar_if(cadena)
    elif tipo == "for":
        return validar_for(cadena)
    elif tipo == "funcion":
        return validar_func(cadena)
    elif tipo == "main":
        return validar_main(cadena)
    else:
        return False, []

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("interface.ui", self)

        self.pushButton.clicked.connect(self.validar_cadena)

    def validar_cadena(self):
        cadena = self.plainTextEdit.toPlainText()
        resultado, pasos = validar_cadena(cadena)
        
        if resultado:
            self.resultadoTextEdit.setPlainText("La cadena es válida.")
        else:
            self.resultadoTextEdit.setPlainText("La cadena es inválida.")

        pasos_str = "\n".join(pasos)
        self.pasosTextEdit.setPlainText(pasos_str)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
