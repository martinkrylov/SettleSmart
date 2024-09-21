from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Main route to render the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Example API route to handle city search
@app.route('/search', methods=['POST'])
def search():
    user_input = request.json.get('condition')
    # Here you would add your logic for searching cities based on input
    response_data = {"city": "Austin", "cost": 2000, "hospitals": 5}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7754, debug=True)
