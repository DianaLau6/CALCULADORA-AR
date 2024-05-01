# app.py
from flask import Flask, render_template, request, jsonify
from lexer import lexer 

app = Flask(__name__)

# Ruta para la página principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener el código fuente ingresado por el usuario
        source_code = request.json.get('source_code')

        # Llamar al analizador léxico
        lexical_result = []
        lexer.input(source_code)
        for token in lexer:
            lexical_result.append((token.type, token.value))

        # Evaluar la expresión (ejemplo simplificado)
        try:
            result = eval(source_code)
        except Exception as e:
            result = str(e)

        # Devolver los resultados
        return jsonify(lexical_result=lexical_result, result=result)

    return render_template('index.html')

# Ruta para el árbol
@app.route('/arbol')
def arbol():
    return render_template('arbol.html')


if __name__ == '__main__':
    app.run(debug=True)
