# Riceguard-AI
🌾 RiceGuard AI
RiceGuard AI is a web-based rice leaf disease detection system. Built using simple HTML, CSS, and a Python-powered machine learning backend, this tool allows users to upload an image of a rice leaf and receive an instant diagnosis along with recommended precautionary measures.

✅ Features

📷 Upload rice leaf images for disease detection

🧠 Backend-powered ML model (e.g., using TensorFlow/Keras)

🛡️ Provides precautionary steps for each detected disease

💻 Clean and simple web interface using vanilla HTML and CSS

📱 Fully responsive and mobile-friendly

🖥️ Technologies Used
Layer	Tools
Frontend	HTML5, CSS3
Backend	Python (Flask / FastAPI)
ML Framework	TensorFlow / Keras

📂 Project Structure

Rice-Leaf/
├── index.html              # Main webpage
├── style.css               # Styling for the frontend
├── app.py                  # Flask or FastAPI backend (ML logic)
├── model/                  # Trained model (.h5 or similar)
├── static/                 # Static assets (images, CSS if any)
└── README.md               # Project documentation

🚀 Getting Started
📦 Prerequisites
Python 3.9+

Required packages in requirements.txt (Flask, TensorFlow, etc.)

🔧 Setup Instructions
Clone or extract the project:


unzip Rice-Leaf.zip
cd Rice-Leaf
Install Python dependencies:


pip install -r requirements.txt
Run the backend server:

python app.py
Open index.html in your browser, or host it using Flask static routing.

🧠 How It Works
User uploads a rice leaf image.

The backend receives the image and runs it through the trained model.

The model classifies the disease (e.g., Brown Spot, Bacterial Leaf Blight).

The page displays the result and shows prevention tips.

🛡️ Example Output
Disease Detected: Bacterial Leaf Blight
Suggested Actions:

Avoid overhead irrigation

Apply copper-based bactericides

Use resistant seed varieties

📬 Contact

Sujal Gaikwad
sujalgaikwad0210@gmail.com

