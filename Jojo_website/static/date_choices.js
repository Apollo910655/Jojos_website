function selectDateOption(optionNumber) {
    const date = new URLSearchParams(window.location.search).get('date');
    window.location.href = `/confirmation?date=${date}&choice=${optionNumber}`;
} 