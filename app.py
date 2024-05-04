from flask import Flask, render_template, request, jsonify
from lexer import lexer
from arbol import construir_arbol_sintactico, convertir_arbol_a_vis

app = Flask(__name__)

datos_arbol = None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener el código fuente ingresado por el usuario
        source_code = request.json.get('source_code')

        try:
            # Llamar al analizador léxico
            lexer.input(source_code)
            lexical_result = [(token.type, token.value) for token in lexer]
            print("Lexical Result:", lexical_result)  # Agregar este print

            # Evaluar la expresión (ejemplo simplificado)
            result = eval(source_code)

            # Construir la lista de tokens para el árbol sintáctico
            lexer.input(source_code)
            tokens = list(lexer)

            # Construir el árbol sintáctico a partir de los tokens
            arbol_sintactico = construir_arbol_sintactico(tokens)

            # Convertir el árbol sintáctico a un formato compatible con Vis.js
            vis_data = convertir_arbol_a_vis(arbol_sintactico)

            # Guardar los datos del árbol para usarlos en la siguiente ruta
            global datos_arbol
            datos_arbol = vis_data

            # Renderizar la plantilla index.html con los resultados léxicos y sintácticos
            return render_template('index.html', lexical_result=lexical_result, result=result)

        except Exception as e:
            return render_template('error.html', message=str(e)), 500

    return render_template('index.html')


@app.route('/arbol', methods=['GET'])
def mostrar_arbol():
    global datos_arbol
    try:
        # Recuperar los datos del árbol guardados previamente
        vis_data = datos_arbol

        if vis_data is None:
            raise Exception("Los datos del árbol sintáctico no están disponibles.")

        # Renderizar la plantilla arbol.html para mostrar el árbol
        return render_template('arbol.html', vis_data=vis_data)

    except Exception as e:
        return render_template('error.html', message=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
