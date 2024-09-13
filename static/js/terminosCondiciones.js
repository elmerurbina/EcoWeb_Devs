document.addEventListener('DOMContentLoaded', function () {
    // Funcion para abrir los terminos y condiciones
    function openTermsConditions(event) {
        event.preventDefault();
        
        const termsWindow = window.open('', 'TermsConditions', 'width=600,height=900');
        termsWindow.document.write(`
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Términos y Condiciones</title>
                <style>
                    body {
                        font-family: 'Arial', sans-serif;
                        padding: 20px;
                        line-height: 1.6;
                    }
                    h1 {
                        color: #007bff;
                    }
                    h2 {
                        margin-top: 20px;
                        color: #007bff;
                    }
                    p {
                        margin-bottom: 15px;
                    }
                </style>
            </head>
            <body>
                <h1>Términos y Condiciones</h1>
                <p>Los siguientes términos y condiciones regulan el uso del sitio web desarrollado por EcoWeb Devs (en adelante, "VerdeNica").</p>
                
                <h2>1. Aceptación de los Términos</h2>
                <p>Al acceder y utilizar este Sitio, usted acepta cumplir con estos términos y condiciones. Si no está de acuerdo con alguna parte de estos términos, no utilice el Sitio o Contactenos.</p>
                
                <h2>2. Uso del Sitio</h2>
                <p>El contenido del Sitio es solo para fines informativos y educativos. No se permite su reproducción o distribución sin autorización.</p>
                
                <h2>3. Privacidad</h2>
                <p>Nuestra política de privacidad describe cómo recopilamos, almacenamos y utilizamos la información que usted proporciona. Al usar el Sitio, usted acepta los términos de nuestra política de privacidad detallada a continuación:</p>
                
                <h3>Política de Privacidad</h3>
                <p>En VerdeNica, valoramos y respetamos su privacidad. Esta política de privacidad describe cómo recopilamos, usamos y protegemos la información personal que usted proporciona a través de nuestro sitio web.</p>
                
                <h4>Información Recopilada</h4>
                <p>Podemos recopilar información personal identificable como su nombre, dirección de correo electrónico, dirección postal, etc., solo cuando usted voluntariamente nos la proporciona al registrarse, suscribirse a nuestro boletín, participar en encuestas, o interactuar de otras formas con nuestro sitio.</p>
                
                <h4>Uso de la Información</h4>
                <p>Utilizamos la información recopilada para mejorar nuestro sitio web, personalizar su experiencia, enviarle información relevante, procesar transacciones y proporcionar soporte al cliente. No vendemos, comercializamos ni transferimos su información personal a terceros sin su consentimiento, excepto según lo requiera la ley.</p>
                
                <h4>Seguridad de la Información</h4>
                <p>Implementamos medidas de seguridad razonables para proteger su información personal contra accesos no autorizados, uso indebido o divulgación.</p>
                
                <h4>Acceso y Control de su Información</h4>
                <p>Puede acceder, corregir, actualizar o eliminar la información personal que nos ha proporcionado en cualquier momento. Si tiene alguna pregunta sobre nuestra política de privacidad o desea ejercer sus derechos de privacidad, no dude en contactarnos.</p>
                
                <h2>4. Derechos de Propiedad Intelectual</h2>
                <p>El contenido del Sitio, incluidos textos, gráficos, logotipos, imágenes, etc., están protegidos por leyes de derechos de autor y otras leyes de propiedad intelectual. No se permite la reproducción, distribución o modificación del contenido sin autorización.</p>
                
                <h2>5. Limitación de Responsabilidad</h2>
                <p>No nos hacemos responsables por cualquier daño directo, indirecto, incidental, especial, consecuente o punitivo que surja del uso o la imposibilidad de usar el Sitio. Esto incluye pérdidas de datos, interrupciones del servicio, errores, omisiones, defectos, virus u otros problemas tecnológicos.</p>
                
                <h2>6. Modificaciones</h2>
                <p>Nos reservamos el derecho de modificar estos términos y condiciones en cualquier momento. Es su responsabilidad revisar periódicamente los cambios. El uso continuado del Sitio después de la publicación de los cambios constituirá su aceptación de los mismos.</p>
                
                <p>Al utilizar este Sitio, usted acepta estar sujeto a estos términos y condiciones. Si tiene alguna pregunta o inquietud, contáctenos.</p>
            </body>
            </html>
        `);
        termsWindow.document.close();
    }
    
    // Attach event listener to elements with class 'view-terms-link'
    document.querySelectorAll('.view-terms-link').forEach(link => {
        link.addEventListener('click', openTermsConditions);
    });
});
