# Archivo para manejar la logica de las campanias

# Metodos y librerias
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from db import save_campaign, get_all_campaigns, save_comment
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Definicion de la ruta ruta principal
@app.route('/campanias')
def campanias():
    form_type = request.args.get('form_type', '')

# Obtener todas las campanias disponibles en la base de datos
    campaigns = get_all_campaigns()
    return render_template('campanias.html', form_type=form_type, campaigns=campaigns)

# Ruta para crear una nueva campania
@app.route('/new_campaign', methods=['POST'])
def new_campaign():
    nombre_campania = request.form['nombre_campania']
    descripcion_campania = request.form['descripcion_campania']
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']

    # Presupuesto es opcional, aqui se comprueba si ese campo esta vacio o no
    presupuesto = request.form.get('presupuesto', None)

    try:
        # Guardar la informacion en la base de datos
        save_campaign(nombre_campania, descripcion_campania, fecha_inicio, fecha_fin, presupuesto)
        flash('Campaña creada exitosamente', 'success') #  Mostrar mensaje de validacion
    except Exception as e:
        # Si ocurre un error mostrar mensaje
        flash(f'Error al crear la campaña: {str(e)}', 'error')

# Luego de crear la campania redirigir a la interfaz principal
    return redirect(url_for('campanias'))

# Ruta para agregar comentarios
@app.route('/add_comment', methods=['POST'])
def add_comment():
    if request.method == 'POST':
        if request.is_json:
            data = request.json
            campaign_id = data.get('campaign_id')
            comment_text = data.get('comment_text')

            try:
                save_comment(campaign_id, comment_text)
                return jsonify({'message': 'Comment added successfully'}), 200
            except Exception as e:
                return jsonify({'error': f'Failed to add comment: {str(e)}'}), 500
        else:
            return jsonify({'error': 'Unsupported Media Type'}), 415

if __name__ == '__main__':
    app.run(debug=True)