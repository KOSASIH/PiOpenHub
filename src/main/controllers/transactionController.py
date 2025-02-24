# transactionController.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import logging
from typing import List
from .models import TransactionModel
from .services.blockchainService import BlockchainService
from .database import get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic model for transaction input
class TransactionCreate(BaseModel):
    sender: str = Field(..., example="0xSenderAddress")
    receiver: str = Field(..., example="0xReceiverAddress")
    amount: float = Field(..., example=0.01)
    currency: str = Field(..., example="BTC")

class TransactionResponse(BaseModel):
    transaction_id: str
    status: str

@router.post("/transactions/", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """
    Create a new transaction and interact with the blockchain.
    """
    logger.info("Creating transaction: %s", transaction)

    # Validate transaction data
    if transaction.amount <= 0:
        logger.error("Invalid transaction amount: %s", transaction.amount)
        raise HTTPException(status_code=400, detail="Transaction amount must be greater than zero.")

    # Interact with the blockchain service
    blockchain_service = BlockchainService()
    try:
        transaction_id = await blockchain_service.create_transaction(
            sender=transaction.sender,
            receiver=transaction.receiver,
            amount=transaction.amount,
            currency=transaction.currency
        )
    except Exception as e:
        logger.exception("Failed to create transaction on blockchain: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to create transaction on blockchain.")

    # Save transaction to the database
    db_transaction = TransactionModel(
        transaction_id=transaction_id,
        sender=transaction.sender,
        receiver=transaction.receiver,
        amount=transaction.amount,
        currency=transaction.currency,
        status="Pending"
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    logger.info("Transaction created successfully: %s", db_transaction)
    return TransactionResponse(transaction_id=db_transaction.transaction_id, status=db_transaction.status)

@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a transaction by its ID.
    """
    logger.info("Retrieving transaction with ID: %s", transaction_id)
    transaction = db.query(TransactionModel).filter(TransactionModel.transaction_id == transaction_id).first()

    if not transaction:
        logger.error("Transaction not found: %s", transaction_id)
        raise HTTPException(status_code=404, detail="Transaction not found.")

    logger.info("Transaction retrieved successfully: %s", transaction)
    return TransactionResponse(transaction_id=transaction.transaction_id, status=transaction.status)

@router.delete("/transactions/{transaction_id}", response_model=dict)
async def delete_transaction(transaction_id: str, db: Session = Depends(get_db)):
    """
    Delete a transaction by its ID.
    """
    logger.info("Deleting transaction with ID: %s", transaction_id)
    transaction = db.query(TransactionModel).filter(TransactionModel.transaction_id == transaction_id).first()

    if not transaction:
        logger.error("Transaction not found: %s", transaction_id)
        raise HTTPException(status_code=404, detail="Transaction not found.")

    db.delete(transaction)
    db.commit()
    logger.info("Transaction deleted successfully: %s", transaction_id)
    return {"detail": "Transaction deleted successfully."}
