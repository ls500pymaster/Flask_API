import os

import requests
from flasgger import Swagger, swag_from
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
swagger = Swagger(app)
API_KEY = os.environ.get("API_KEY")

@app.route('/forecast', methods=['GET'])
@swag_from({
    'parameters': [
        {
            "name": "lat",
            "in": "query",
            "type": "number",
            "description": "Latitude",
            "required": True,
        },
        {
            "name": "lon",
            "in": "query",
            "type": "number",
            "description": "Longitude",
            "required": True,
        },
        {
            "name": "lang",
            "in": "query",
            "type": "string",
            "description": "Language",
            "required": False,
        },
    ],
    'responses': {
        200: {
            'description': 'Weather forecast data',
        },
        500: {
            'description': 'Error message',
        }
    },
})

def forecast():
	latitude = request.args.get("lat", default=0, type=float)
	longitude = request.args.get("lon", default=0, type=float)
	lang = request.args.get("lang", default="en", type=str)

	url = f"https://api.weatherapi.com/v1/current.json?q={latitude}%2C%20{longitude}&lang={lang}&key={API_KEY}"

	response = requests.get(url)

	if response.status_code:
		data = response.json()
		return jsonify(data), 200
	else:
		return jsonify({"message": "Unable to fetch forecast"}), 500


@app.route('/about')
def about():
	return render_template("about.html")


if __name__ == '__main__':
	app.run(debug=True)
