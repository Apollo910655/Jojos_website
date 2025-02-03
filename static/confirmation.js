function confirmChoice() {
    const params = new URLSearchParams(window.location.search);
    
    fetch('/confirm-choice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            date: params.get('date'),
            choice: parseInt(params.get('choice'))
        })
    })
    .then(response => response.json())
    .then(data => {
        alert('Thank you! I can\'t wait for our date! ❤️');
        window.location.href = '/';  // Redirect to home page
    })
    .catch(error => console.error('Error:', error));
} 