from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Initialize a DataFrame to store carbon credits
carbon_credits = pd.DataFrame(columns=['id', 'owner', 'amount', 'type'])

# Initialize a DataFrame to store emission records
emission_records = pd.DataFrame(columns=['id', 'owner', 'amount', 'type'])

@app.route('/create_credit', methods=['POST'])
def create_credit():
    data = request.json
    credit_id = len(carbon_credits) + 1
    owner = data.get('owner')
    amount = data.get('amount')
    credit_type = data.get('type')

    # Create a new carbon credit
    new_credit = pd.DataFrame({'id': [credit_id], 'owner': [owner], 'amount': [amount], 'type': [credit_type]})
    global carbon_credits
    carbon_credits = pd.concat([carbon_credits, new_credit], ignore_index=True)

    return jsonify({'status': 'Credit created', 'credit_id': credit_id})

@app.route('/track_emission', methods=['POST'])
def track_emission():
    data = request.json
    emission_id = len(emission_records) + 1
    owner = data.get('owner')
    amount = data.get('amount')
    emission_type = data.get('type')

    # Create a new emission record
    new_emission = pd.DataFrame({'id': [emission_id], 'owner': [owner], 'amount': [amount], 'type': [emission_type]})
    global emission_records
    emission_records = pd.concat([emission_records, new_emission], ignore_index=True)

    return jsonify({'status': 'Emission tracked', 'emission_id': emission_id})

@app.route('/get_credits', methods=['GET'])
def get_credits():
    return jsonify(carbon_credits.to_dict(orient='records'))

@app.route('/get_emissions', methods=['GET'])
def get_emissions():
    return jsonify(emission_records.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
