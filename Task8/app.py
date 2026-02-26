from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = "244b6048b80cdf0875391f41023330cc"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')

    if not city:
        return jsonify({"error": "City required"})

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return jsonify({"error": "City not found"})

    return jsonify({
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"]
    })

if __name__ == '__main__':
    app.run(debug=True)