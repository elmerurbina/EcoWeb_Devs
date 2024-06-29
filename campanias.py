from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from db import save_campaign, get_all_campaigns, save_comment

app = Flask(__name__)

@app.route('/campanias')
def campanias():
    form_type = request.args.get('form_type', '')

    campaigns = get_all_campaigns()
    return render_template('campanias.html', form_type=form_type, campaigns=campaigns)


@app.route('/new_campaign', methods=['POST'])
def new_campaign():
    nombre_campania = request.form['nombre_campania']
    descripcion_campania = request.form['descripcion_campania']
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']

    # Check if presupuesto exists in form data
    presupuesto = request.form.get('presupuesto', None)

    try:
        save_campaign(nombre_campania, descripcion_campania, fecha_inicio, fecha_fin, presupuesto)
        flash('Campaña creada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al crear la campaña: {str(e)}', 'error')

    return redirect(url_for('campanias'))

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