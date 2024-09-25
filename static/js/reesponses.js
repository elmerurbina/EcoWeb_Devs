document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.responder-button').forEach(button => {
        button.addEventListener('click', (event) => {
            const itemId = event.target.getAttribute('data-item-id');
            const itemType = event.target.getAttribute('data-item-type');
            toggleAnswerForm(event.target, itemId, itemType);
        });
    });

    document.querySelectorAll('.submit-answer-button').forEach(button => {
        button.addEventListener('click', async (event) => {
            const itemId = event.target.getAttribute('data-item-id');
            const itemType = event.target.getAttribute('data-item-type');
            const answerText = event.target.previousElementSibling.value;
            
            if (answerText) {
                const response = await fetch('/submit_answer', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ answer: answerText, item_id: itemId, item_type: itemType })
                });
                
                if (response.ok) {
                    loadAnswers(itemId, itemType);
                    event.target.previousElementSibling.value = '';
                } else {
                    alert('Error al enviar la respuesta');
                }
            }
        });
    });
});

function toggleAnswerForm(button, itemId, itemType) {
    const answerForm = document.querySelector(`.answer-form[data-item-id="${itemId}"][data-item-type="${itemType}"]`);
    answerForm.style.display = answerForm.style.display === 'none' || answerForm.style.display === '' ? 'block' : 'none';
    loadAnswers(itemId, itemType);
}

async function loadAnswers(itemId, itemType) {
    const response = await fetch(`/get_answers/${itemId}/${itemType}`);
    if (response.ok) {
        const answers = await response.json();
        const answersContainer = document.getElementById(`answers-${itemId}`);
        const answersList = answersContainer.querySelector('.answers-list');
        answersList.innerHTML = '';

        answers.forEach(answer => {
            const li = document.createElement('li');
            li.textContent = answer.contenido;
            answersList.appendChild(li);
        });

        answersContainer.style.display = 'block';
    }
}
