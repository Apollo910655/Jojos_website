let currentDate = new Date();
let selectedDate = null;

function renderCalendar() {
    const monthYear = document.getElementById('monthYear');
    const daysContainer = document.getElementById('days');
    
    const firstDay = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
    const lastDay = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
    
    monthYear.textContent = currentDate.toLocaleString('default', { 
        month: 'long', 
        year: 'numeric' 
    });
    
    daysContainer.innerHTML = '';
    
    for (let i = 0; i < firstDay.getDay(); i++) {
        const emptyDay = document.createElement('div');
        daysContainer.appendChild(emptyDay);
    }
    
    for (let day = 1; day <= lastDay.getDate(); day++) {
        const dayElement = document.createElement('div');
        dayElement.classList.add('day');
        dayElement.textContent = day;
        
        const dateString = `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${day}`;
        if (selectedDate === dateString) {
            dayElement.classList.add('selected');
        }
        
        dayElement.addEventListener('click', () => selectDate(day));
        daysContainer.appendChild(dayElement);
    }
}

async function selectDate(day) {
    const dateString = `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${day}`;
    selectedDate = dateString;
    
    document.querySelectorAll('.day').forEach(el => el.classList.remove('selected'));
    document.querySelector(`.day:nth-child(${day + firstDayOfMonth()})`).classList.add('selected');
    
    document.getElementById('selected-date').textContent = 
        `Selected date: ${new Date(currentDate.getFullYear(), currentDate.getMonth(), day).toLocaleDateString()}`;
    
    // Enable the next button
    document.getElementById('nextButton').disabled = false;

    // Send date to backend
    try {
        const response = await fetch('/save-date', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ selected_date: dateString })
        });
        
        if (response.ok) {
            alert('Date saved successfully! I will email you the details ❤️');
        }
    } catch (error) {
        console.error('Error saving date:', error);
    }
}

function firstDayOfMonth() {
    return new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay();
}

document.getElementById('prevMonth').addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
});

document.getElementById('nextMonth').addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
});

function goToDateChoices() {
    if (selectedDate) {
        window.location.href = `/date-choices?date=${selectedDate}`;
    }
}

renderCalendar(); 