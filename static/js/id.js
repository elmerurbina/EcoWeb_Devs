async function saveComment(campaignId, userId, commentText) {
    const url = '/add_comment';
    const data = {
        campaign_id: campaignId,
        user_id: userId,
        comment_text: commentText
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('Error saving comment');
        }

        const responseData = await response.json();
        console.log('Comment saved successfully:', responseData);
    } catch (error) {
        console.error('Failed to save comment:', error.message);
    }
}
