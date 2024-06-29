function toggleAnswerForm(button) {
    const answerForm = button.nextElementSibling;
    if (answerForm.style.display === "none") {
        answerForm.style.display = "block";
    } else {
        answerForm.style.display = "none";
    }
}
