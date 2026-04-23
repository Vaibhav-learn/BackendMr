"""
Order Management Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Order
from app.schemas import OrderCreate, OrderApprove, OrderResponse
from datetime import datetime
from typing import List

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order: OrderCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create a new order"""
    db_order = Order(
        mr_id=user_id,
        product_details=order.product_details,
        quantity=order.quantity,
        order_notes=order.order_notes,
        status="pending"
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return db_order


@router.get("", response_model=List[OrderResponse])
def get_my_orders(user_id: int, db: Session = Depends(get_db)):
    """Get all orders for current user"""
    orders = db.query(Order).filter(
        Order.mr_id == user_id
    ).order_by(Order.created_at.desc()).all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get order details"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order


@router.post("/{order_id}/approve", response_model=OrderResponse)
def approve_order(
    order_id: int,
    approval: OrderApprove,
    admin_id: int,
    db: Session = Depends(get_db)
):
    """Approve or reject order (Admin only)"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    order.status = "approved" if approval.approved else "rejected"
    order.approved_by = admin_id
    order.approval_date = datetime.utcnow()
    
    db.commit()
    db.refresh(order)
    
    return order
