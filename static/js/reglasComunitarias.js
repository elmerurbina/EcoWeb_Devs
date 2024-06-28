document.addEventListener('DOMContentLoaded', function () {
    const rules = `
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reglas Comunitarias</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    padding: 20px;
                    line-height: 1.6;
                }
                h1 {
                    color: #007bff;
                }
            </style>
        </head>
        <body>
            <h1>Reglas Comunitarias</h1>
            <p>Para asegurar un ambiente seguro y respetuoso, pedimos que todos los miembros de la comunidad sigan estas reglas:</p>
            <ul>
                <li> <strong>Respeto mutuo: </strong> Tratar a todos los miembros con respeto, sin importar sus opiniones o creencias.</li>
                <li> <strong>No al lenguaje ofensivo: </strong> Evitar el uso de lenguaje ofensivo, insultos o ataques personales.</li>
                <li> <strong>Publicaciones relevantes: </strong> Asegurarse de que todas las publicaciones y debates sean relevantes y constructivos.</li>
                <li> <strong>Privacidad:</strong> No compartir información personal de otros miembros sin su consentimiento.</li>
                <li> <strong>Fuentes verificadas:</strong> Compartir información de fuentes verificadas para evitar la propagación de desinformación.</li>
                <li> <strong>Moderación:</strong> Seguir las instrucciones de los moderadores y respetar sus decisiones.</li>
                <li> <strong>No spam:</strong> Evitar el envío de mensajes repetitivos, publicidad no autorizada o contenido irrelevante.</li>
            </ul>
            <p>El incumplimiento de estas reglas puede resultar en la eliminación de publicaciones y la expulsión de la comunidad.</p>
        </body>
        </html>
    `;

    document.querySelectorAll('.view-rules-link').forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const rulesWindow = window.open('', 'Rules', 'width=600,height=400');
            rulesWindow.document.write(rules);
            rulesWindow.document.close();
        });
    });
});
