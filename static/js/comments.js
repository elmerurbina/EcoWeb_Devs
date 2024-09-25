async function loadLoginAndComment(campaignId) {
    try {
        const response = await fetch('/login'); // Replace with your actual login route
        if (response.ok) {
            const responseData = await response.json();
            if (responseData.success) {
              
                toggleCommentForm(campaignId);
            } else {
                // Handle login failure or redirect to login page
                alert('Login failed. Please try again.');
            }
        } else {
            throw new Error('Failed to load login page.');
        }
    } catch (error) {
        console.error('Error loading login page:', error.message);
    }
}

function toggleCommentForm(campaignId) {
    const commentForm = document.getElementById(`commentForm${campaignId}`);
    if (commentForm) {
        commentForm.style.display = commentForm.style.display === 'none' ? 'block' : 'none';
    }
}
