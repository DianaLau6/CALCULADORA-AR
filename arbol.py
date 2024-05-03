from lexer import tokens  # Importar los tokens definidos en lexer.py
from lexer import lexer     # Asegúrate de importar el lexer si es necesario

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []
        
    
def construir_arbol_sintactico(tokens):
    # Definir la prioridad de los operadores
    prioridad = {
        '(': 3,
        ')': 3,
        '*': 2,
        '/': 2,
        '+': 1,
        '-': 1
    }

    # Función para comparar la prioridad de dos operadores
    def prioridad_mayor(op1, op2):
        return prioridad[op1] >= prioridad[op2]

    # Función para construir el árbol sintáctico
    def construir_arbol(tokens):
        pila_operadores = []
        pila_nodos = []

        for token in tokens:
            if token.value in prioridad:  # Verificar el tipo del token
                while (pila_operadores and pila_operadores[-1] != '(' and 
                       prioridad_mayor(pila_operadores[-1], token.value)):
                    operador = pila_operadores.pop()
                    der = pila_nodos.pop()
                    izq = pila_nodos.pop()
                    nuevo_nodo = Nodo(operador)
                    nuevo_nodo.hijos.append(izq)
                    nuevo_nodo.hijos.append(der)
                    pila_nodos.append(nuevo_nodo)
                pila_operadores.append(token.value)
            elif token.value == '(':
                pila_operadores.append(token.value)
            elif token.value == ')':
                while pila_operadores[-1] != '(':
                    operador = pila_operadores.pop()
                    der = pila_nodos.pop()
                    izq = pila_nodos.pop()
                    nuevo_nodo = Nodo(operador)
                    nuevo_nodo.hijos.append(izq)
                    nuevo_nodo.hijos.append(der)
                    pila_nodos.append(nuevo_nodo)
                pila_operadores.pop()  # Sacar el '('
            else:  # Es un operando
                pila_nodos.append(Nodo(token.value))  # Usar token.value como operando

        while pila_operadores:
            operador = pila_operadores.pop()
            der = pila_nodos.pop()
            izq = pila_nodos.pop()
            nuevo_nodo = Nodo(operador)
            nuevo_nodo.hijos.append(izq)
            nuevo_nodo.hijos.append(der)
            pila_nodos.append(nuevo_nodo)

        return pila_nodos[0]  # El primer nodo en la pila es la raíz del árbol

    # Construir el árbol sintáctico a partir de los tokens
    arbol_sintactico = construir_arbol(tokens)

    return arbol_sintactico

def convertir_arbol_a_vis(raiz):
    nodes = []
    edges = []

    def agregar_nodo(nodo, parent=None):
        nonlocal nodes, edges
        node_id = len(nodes) + 1
        nodes.append({'id': node_id, 'label': str(nodo.valor)})
        if parent is not None:
            edges.append({'from': parent, 'to': node_id})
        for hijo in nodo.hijos:
            agregar_nodo(hijo, parent=node_id)

    agregar_nodo(raiz)
    return {'nodes': nodes, 'edges': edges}