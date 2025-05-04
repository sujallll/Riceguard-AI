const precautionsData = {
    'Bacterial Leaf Blight': [
        "Use disease-resistant rice varieties",
        "Ensure proper field drainage",
        "Apply balanced fertilization",
        "Avoid excessive nitrogen application",
        "Treatment: Use copper-based bactericides if severe"
    ],
    'Brown Spot': [
        "Maintain proper soil fertility",
        "Use certified disease-free seeds",
        "Proper spacing between plants",
        "Avoid water stress",
        "Treatment: Apply fungicides if necessary"
    ],
    'Healthy Rice Leaf': [
        "Continue good agricultural practices",
        "Maintain proper irrigation",
        "Regular monitoring",
        "Balanced fertilizer application",
        "Maintain field hygiene"
    ],
    'Leaf Blast': [
        "Use blast-resistant varieties",
        "Avoid excessive nitrogen",
        "Maintain good drainage",
        "Early planting",
        "Treatment: Apply systemic fungicides"
    ],
    'Leaf scald': [
        "Use resistant varieties",
        "Avoid dense planting",
        "Proper water management",
        "Remove weed hosts",
        "Treatment: Apply fungicides"
    ],
    'Narrow Brown Leaf Spot': [
        "Plant resistant varieties",
        "Balanced soil fertility",
        "Proper spacing",
        "Remove infected debris",
        "Treatment: Apply fungicides"
    ],
    'Neck_Blast': [
        "Use resistant varieties",
        "Apply silicon fertilizers",
        "Avoid excess nitrogen",
        "Proper timing of planting",
        "Treatment: Systemic fungicides"
    ],
    'Rice Hispa': [
        "Regular monitoring",
        "Remove alternate hosts",
        "Avoid over fertilization",
        "Encourage natural enemies",
        "Treatment: Apply insecticides"
    ],
    'Sheath Blight': [
        "Use tolerant varieties",
        "Avoid dense planting",
        "Proper nitrogen management",
        "Good drainage",
        "Treatment: Apply fungicides"
    ]
};

// Handle drag and drop
const dropZone = document.getElementById('dropZone');
const imageInput = document.getElementById('imageInput');
const previewContainer = document.getElementById('previewContainer');
const loading = document.getElementById('loading');
const resultSection = document.getElementById('resultSection');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    dropZone.classList.add('highlight');
}

function unhighlight(e) {
    dropZone.classList.remove('highlight');
}

dropZone.addEventListener('drop', handleDrop, false);
imageInput.addEventListener('change', handleFileSelect, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

function handleFileSelect(e) {
    const files = e.target.files;
    handleFiles(files);
}

function handleFiles(files) {
    const file = files[0];
    if (file && file.type.startsWith('image/')) {
        const preview = document.getElementById('imagePreview');
        preview.src = URL.createObjectURL(file);
        previewContainer.style.display = 'block';
        
        document.getElementById('loading').style.display = 'block';
        document.getElementById('resultSection').style.display = 'none';
        
        const formData = new FormData();
        formData.append('file', file);

        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('resultSection').style.display = 'block';
            
            const confidence = (data.confidence_scores[data.predicted_disease] * 100).toFixed(2);
            const confidenceClass = confidence > 80 ? 'confidence-high' : 
                                  confidence > 50 ? 'confidence-medium' : 
                                  'confidence-low';
            
            // Create stage indicator class
            const stageClass = data.stage === 'severe' ? 'stage-severe' : 
                             data.stage === 'medium' ? 'stage-medium' : 
                             'stage-early';
            
            document.getElementById('predictionResult').innerHTML = `
                <div class="prediction-result">
                    <h3>Disease Detection</h3>
                    <p class="disease-name"><strong>Detected Disease:</strong> ${data.predicted_disease}</p>
                    <p class="confidence ${confidenceClass}">Confidence: ${confidence}%</p>
                    
                    <div class="disease-stage ${stageClass}">
                        <h4>Disease Stage</h4>
                        <p>${data.stage_description}</p>
                    </div>
                    
                    <div class="disease-causes">
                        <h4>Causes</h4>
                        <ul>
                            ${data.causes.map(cause => `<li>${cause}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            `;

            // Display precautions
            const precautions = precautionsData[data.predicted_disease];
            document.getElementById('precautionsContent').innerHTML = `
                <ul class="precautions-list">
                    ${precautions.map(p => `<li>${p}</li>`).join('')}
                </ul>
            `;
        })
        .catch(error => {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('resultSection').style.display = 'block';
            document.getElementById('predictionResult').innerHTML = `
                <p class="error">Error: ${error.message}</p>
            `;
        });
    } else {
        alert('Please upload an image file (JPG, JPEG, or PNG)');
    }
}

function resetUpload() {
    const imageInput = document.getElementById('imageInput');
    const previewContainer = document.getElementById('previewContainer');
    const resultSection = document.getElementById('resultSection');
    
    imageInput.value = '';
    previewContainer.style.display = 'none';
    resultSection.style.display = 'none';
}
