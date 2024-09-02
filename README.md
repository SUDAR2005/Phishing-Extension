<!DOCTYPE html>
<html>
<body>
  <h1>Phishing-Extension</h1>

  <h2>Overview</h2>

  <p>This project combines Python backend services with a browser extension built using JavaScript. The backend processes data and serves it to the frontend, while the extension interacts with the browser and finnaly detects the pishing website.</p>

  <h2>Features</h2>

  <ul>
    <li><strong>Backend:</strong> Powered by Python, includes a pre-trained model and a server for API handling.</li>
    <li><strong>Browser Extension:</strong> Includes background scripts, content scripts, and a popup interface.</li>
  </ul>

  <h2>Prerequisites</h2>

  <p>Before you begin, ensure you have met the following requirements:</p>

  <ul>
    <li>Python 3.x installed on your machine.</li>
  </ul>

  <h2>Installation</h2>

  <h3>1. Clone the Repository</h3>

  <p>Clone this repository to your local machine using:</p>

  <pre>
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
  </pre>

  <h3>2. Set Up Python Environment</h3>

  <p>Navigate to the project directory and create a virtual environment:</p>

  <pre>
    python -m venv myenv
  </pre>

  <p>Activate the environment:</p>

  <ul>
    <li><strong>On macOS/Linux:</strong></li>

    <pre>
      source myenv/bin/activate
    </pre>

    <li><strong>On Windows:</strong></li>

    <pre>
      myenv\Scripts\activate
    </pre>
  </ul>

  <h3>3. Install Python Dependencies</h3>

  <p>Install the necessary Python packages using requirements.txt:</p>

  <pre>
    pip install -r requirements.txt
  </pre>

  <h3>4. Run the Backend Server</h3>

  <p>After setting up the environment, start the backend server:</p>

  <pre>
    python server/app.py
  </pre>

  <p>This will start the Flask server, ready to handle requests from the extension.</p>

  <h3>5. Load the Extension in Chrome</h3>

  <p>To test or use the extension:</p>

  <ol>
    <li>Open Chrome and navigate to chrome://extensions/.</li>
    <li>Enable "Developer mode" in the top-right corner.</li>
    <li>Click "Load unpacked" and select the project directory containing manifest.json.</li>
  </ol>

  <h2>Project Structure</h2>

  <pre>
    .
    ├── _metadata/
    ├── image/
    │   └── icon16.png
    ├── myenv/
    │   └── ... (virtual environment files)
    ├── scripts/
    │   ├── background.js
    │   ├── content.js
    │   └── popup.js
    ├── server/
    │   ├── ann_model.pkl
    │   └── app.py
    ├── .gitignore
    ├── blocked.html
    ├── manifest.json
    ├── popup.html
    ├── requirements.txt
    └── rules.json
  </pre>

  <ul>
    <li><strong>_metadata/:</strong> Contains additional project metadata.</li>
    <li><strong>image/:</strong> Stores image assets used in the extension.</li>
    <li><strong>myenv/:</strong> Virtual environment directory.</li>
    <li><strong>scripts/:</strong> JavaScript files for the browser extension.</li>
    <li><strong>server/:</strong> Backend server files, including a pre-trained model.</li>
    <li><strong>.gitignore:</strong> Specifies files to be ignored by Git.</li>
    <li><strong>blocked.html:</strong> HTML page for blocked content.</li>
    <li><strong>manifest.json:</strong> Manifest file for the browser extension.</li>
    <li><strong>popup.html:</strong> HTML for the extension's popup interface.</li>
    <li><strong>requirements.txt:</strong> Python dependencies.</li>
    <li><strong>rules.json:</strong> JSON file for defining extension rules.</li>
  </ul>
  </ol>
</html>
