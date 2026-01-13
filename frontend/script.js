// Configuration - Update this with your backend URL
const API_URL = 'http://localhost:8000';  // Change to your Render URL after deployment

const form = document.getElementById('obesityForm');
const resultDiv = document.getElementById('result');
const errorDiv = document.getElementById('error');
const submitBtn = document.getElementById('submitBtn');
const btnText = document.getElementById('btnText');
const loader = document.getElementById('loader');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Hide previous results/errors
    resultDiv.style.display = 'none';
    errorDiv.style.display = 'none';
    
    // Show loading state
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    loader.style.display = 'block';
    
    // Collect form data
    const formData = {
        weight: parseFloat(document.getElementById('weight').value),
        height: parseFloat(document.getElementById('height').value),
        age: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        main_meals: parseInt(document.getElementById('mainMeals').value),
        high_caloric_food: document.getElementById('highCaloricFood').value,
        vegetable_intake: parseInt(document.getElementById('vegetableIntake').value),
        alcohol_intake: document.getElementById('alcoholIntake').value
    };
    
    try {
        // Make API request
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display results
        document.getElementById('predictionText').textContent = data.prediction;
        
        if (data.confidence !== null && data.confidence !== undefined) {
            document.getElementById('confidenceText').textContent = 
                `${(data.confidence * 100).toFixed(1)}%`;
            document.getElementById('confidenceDiv').style.display = 'block';
        } else {
            document.getElementById('confidenceDiv').style.display = 'none';
        }
        
        resultDiv.style.display = 'block';
        
        // Scroll to result
        resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('errorText').textContent = 
            `Failed to get prediction. Please make sure the backend is running. Error: ${error.message}`;
        errorDiv.style.display = 'block';
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        loader.style.display = 'none';
    }
});

// Add input validation feedback
const inputs = document.querySelectorAll('input, select');
inputs.forEach(input => {
    input.addEventListener('invalid', (e) => {
        e.preventDefault();
        input.style.borderColor = '#f44';
    });
    
    input.addEventListener('input', () => {
        input.style.borderColor = '#e0e0e0';
    });
});
