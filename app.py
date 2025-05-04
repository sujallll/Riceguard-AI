from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
from PIL import Image
import os

app = Flask(__name__)

# Load the trained model
MODEL_PATH = "C:/Users/lenovo/Downloads/Rice-Leaf/backend/my_final_model.h5"
try:
    print(f"Loading model from: {MODEL_PATH}")
    model = tf.keras.models.load_model(MODEL_PATH)


    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    raise

# Define class names
CLASS_NAMES = [
    'Bacterial Leaf Blight',
    'Brown Spot',
    'Healthy Rice Leaf',
    'Leaf Blast',
    'Leaf scald',
    'Narrow Brown Leaf Spot',
    'Neck_Blast',
    'Rice Hispa',
    'Sheath Blight'
]

# Disease information dictionary
DISEASE_INFO = {
    'Bacterial Leaf Blight': {
        'causes': [
            'Bacteria Xanthomonas oryzae',
            'High humidity (>70%)',
            'Temperature range 25-30°C',
            'Stagnant water in field'
        ],
        'stage_detection': {
            'threshold': {
                'early': 0.6,
                'medium': 0.8,
                'severe': 0.9
            },
            'descriptions': {
                'early': 'Early stage - Yellowing of leaves, small lesions. Treatment can be effective.',
                'medium': 'Medium stage - Larger lesions, leaf wilting. Immediate action required.',
                'severe': 'Severe stage - Widespread infection, leaf death. Very difficult to control.'
            }
        }
    },
    'Narrow Brown Leaf Spot': {
        'causes': [
            'Fungus Cercospora janseana',
            'High relative humidity (>89%)',
            'Temperature range 25-35°C',
            'Extended leaf wetness periods',
            'Poor soil fertility',
            'Plant stress conditions'
        ],
        'stage_detection': {
            'threshold': {
                'early': 0.6,
                'medium': 0.75,
                'severe': 0.85
            },
            'descriptions': {
                'early': 'Early stage - Small, narrow brown lesions appear. Control measures highly effective.',
                'medium': 'Medium stage - Lesions enlarge and multiply. Immediate treatment needed.',
                'severe': 'Severe stage - Widespread infection, leaves dying. Yield loss likely.'
            }
        }
    },
    'Brown Spot': {
        'causes': [
            'Fungus Helminthosporium oryzae',
            'Nutrient deficiency (especially potassium)',
            'Soil moisture stress',
            'Poor soil fertility',
            'Unfavorable weather conditions'
        ],
        'stage_detection': {
            'threshold': {
                'early': 0.6,
                'medium': 0.75,
                'severe': 0.85
            },
            'descriptions': {
                'early': 'Early stage - Small brown spots. Can be controlled with proper treatment.',
                'medium': 'Medium stage - Enlarged spots, yellowing. Requires immediate attention.',
                'severe': 'Severe stage - Large dark spots, leaf death. Difficult to manage.'
            }
        }
    },
    'Leaf Blast': {
        'causes': [
            'Fungus Magnaporthe oryzae',
            'High nitrogen fertilization',
            'Long periods of leaf wetness',
            'Temperature range 22-29°C',
            'High relative humidity'
        ],
        'stage_detection': {
            'threshold': {
                'early': 0.6,
                'medium': 0.8,
                'severe': 0.9
            },
            'descriptions': {
                'early': 'Early stage - Small lesions appear. Treatment highly effective.',
                'medium': 'Medium stage - Diamond-shaped lesions. Urgent treatment needed.',
                'severe': 'Severe stage - Large necrotic areas. Significant yield loss likely.'
            }
        }
    },
    'Leaf scald': {
        'causes': [
            'Fungus Rhynchosporium oryzae',
            'Cool temperatures (15-25°C)',
            'High humidity',
            'Poor air circulation',
            'Dense canopy'
        ],
        'stage_detection': {
            'threshold': {
                'early': 0.6,
                'medium': 0.8,
                'severe': 0.9
            },
            'descriptions': {
                'early': 'Early stage - Zonate lesions appear. Good response to treatment.',
                'medium': 'Medium stage - Expanding lesions. Immediate action required.',
                'severe': 'Severe stage - Large necrotic areas. Difficult to control.'
            }
        }
    },
    'Neck_Blast': {
        'causes': [
            'Fungus Magnaporthe oryzae',
            'High nitrogen levels',
            'Drought stress',
            'Susceptible growth stage',
            'Favorable weather conditions'
        ],
        'stage_detection': {
            'threshold': {
                'early': 0.6,
                'medium': 0.8,
                'severe': 0.9
            },
            'descriptions': {
                'early': 'Early stage - Small neck lesions. Treatment very effective.',
                'medium': 'Medium stage - Expanding neck rot. Urgent intervention needed.',
                'severe': 'Severe stage - Complete neck failure. Severe yield loss.'
            }
        }
    },
    'Rice Hispa': {
        'causes': [
            'Insect Dicladispa armigera',
            'High temperature',
            'High humidity',
            'Dense plantation',
            'Early plantation'
        ],
        'stage_detection': {
            'threshold': {
                'early': 0.6,
                'medium': 0.8,
                'severe': 0.9
            },
            'descriptions': {
                'early': 'Early stage - Initial feeding damage. Easy to control.',
                'medium': 'Medium stage - Increased damage. Need immediate action.',
                'severe': 'Severe stage - Extensive damage. Difficult to manage.'
            }
        }
    },
    'Sheath Blight': {
        'causes': [
            'Fungus Rhizoctonia solani',
            'High nitrogen fertilization',
            'Dense planting',
            'High humidity (>95%)',
            'Temperatures 28-32°C'
        ],
        'stage_detection': {
            'threshold': {
                'early': 0.6,
                'medium': 0.8,
                'severe': 0.9
            },
            'descriptions': {
                'early': 'Early stage - Small sheath lesions. Good control possible.',
                'medium': 'Medium stage - Expanding lesions. Immediate treatment needed.',
                'severe': 'Severe stage - Extensive damage. Very difficult to control.'
            }
        }
    },
    'Healthy Rice Leaf': {
        'causes': [
            'Proper nutrient management',
            'Good irrigation practices',
            'Optimal growing conditions',
            'Effective pest management',
            'Regular monitoring'
        ],
        'stage_detection': {
            'threshold': {
                'early': 0.9,
                'medium': 0.95,
                'severe': 1.0
            },
            'descriptions': {
                'early': 'Healthy - Good growing conditions',
                'medium': 'Healthy - Optimal growth',
                'severe': 'Healthy - Excellent condition'
            }
        }
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    print("Received prediction request")  # Debug print
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    try:
        file = request.files['file']
        print(f"Processing file: {file.filename}")  # Debug print
        
        # Process the image
        image = Image.open(file).convert('RGB')  # Ensure RGB format
        image = image.resize((256, 256))  # Adjust size according to your model's requirements
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        
        # Make prediction
        predictions = model.predict(image_array)
        class_idx = np.argmax(predictions[0])
        predicted_class = CLASS_NAMES[class_idx]
        confidence = float(predictions[0][class_idx])
        
        print(f"Predicted class: {predicted_class}, Confidence: {confidence}")  # Debug print
        
        # Get disease info
        disease_info = DISEASE_INFO.get(predicted_class, {
            'causes': ['Information not available'],
            'stage_detection': {
                'threshold': {'early': 0.6, 'medium': 0.8, 'severe': 0.9},
                'descriptions': {
                    'early': 'Early stage',
                    'medium': 'Medium stage',
                    'severe': 'Severe stage'
                }
            }
        })
        
        # Determine disease stage
        stage = 'early'
        if confidence >= disease_info['stage_detection']['threshold']['severe']:
            stage = 'severe'
        elif confidence >= disease_info['stage_detection']['threshold']['medium']:
            stage = 'medium'
        
        response = {
            'predicted_disease': predicted_class,
            'confidence_scores': {
                CLASS_NAMES[i]: float(predictions[0][i]) 
                for i in range(len(CLASS_NAMES))
            },
            'causes': disease_info['causes'],
            'stage': stage,
            'stage_description': disease_info['stage_detection']['descriptions'][stage]
        }
        
        print(f"Sending response: {response}")  # Debug print
        return jsonify(response)
        
    except Exception as e:
        print(f"Error during prediction: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)
