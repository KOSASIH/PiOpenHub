from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from marshmallow import Schema, fields, ValidationError
from sqlalchemy.exc import IntegrityError
from models.transactionModel import TransactionModel
from services.blockchainService import BlockchainService
from utils.logger import logger

transaction_routes = Blueprint('transaction_routes', __name__)

# Schema for validating transaction input
class TransactionSchema(Schema):
    sender = fields.String(required=True)
    receiver = fields.String(required=True)
    amount = fields.Float(required=True)

transaction_schema = TransactionSchema()

@transaction_routes.route('/transactions', methods=['POST'])
@jwt_required()
def create_transaction():
    try:
        # Validate input data
        data = request.get_json()
        validated_data = transaction_schema.load(data)

        # Create a new transaction
        transaction = TransactionModel(
            sender=validated_data['sender'],
            receiver=validated_data['receiver'],
            amount=validated_data['amount']
        )
        
        # Save transaction to the database
        transaction.save()

        # Interact with the blockchain service
        blockchain_service = BlockchainService()
        blockchain_response = blockchain_service.record_transaction(transaction)

        logger.info(f"Transaction recorded: {blockchain_response}")

        return jsonify({
            'message': 'Transaction created successfully',
            'transaction_id': transaction.id,
            'blockchain_response': blockchain_response
        }), 201

    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return jsonify({'error': 'Invalid input', 'messages': err.messages}), 400
    except IntegrityError:
        logger.error("Transaction failed due to integrity error.")
        return jsonify({'error': 'Transaction could not be processed. Please check your data.'}), 409
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500

@transaction_routes.route('/transactions/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction(transaction_id):
    try:
        transaction = TransactionModel.query.get(transaction_id)
        if not transaction:
            logger.warning(f"Transaction {transaction_id} not found.")
            return jsonify({'error': 'Transaction not found'}), 404

        return jsonify({
            'id': transaction.id,
            'sender': transaction.sender,
            'receiver': transaction.receiver,
            'amount': transaction.amount,
            'timestamp': transaction.timestamp
        }), 200

    except Exception as e:
        logger.error(f"Error retrieving transaction: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500

@transaction_routes.route('/transactions', methods=['GET'])
@jwt_required()
def list_transactions():
    try:
        transactions = TransactionModel.query.all()
        transaction_list = [{
            'id': transaction.id,
            'sender': transaction.sender,
            'receiver': transaction.receiver,
            'amount': transaction.amount,
            'timestamp': transaction.timestamp
        } for transaction in transactions]

        return jsonify(transaction_list), 200

    except Exception as e:
        logger.error(f"Error retrieving transactions: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500
