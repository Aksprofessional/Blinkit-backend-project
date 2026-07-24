from fastapi import HTTPException,status
from sqlalchemy.orm import Session,joinedload
from uuid import UUID
from app.models.cart_item import CartItem
from app.models.cart import Cart
from app.models.product_variant import product_variant
from app.models.products import Products

def add_product_cart_item(db: Session, productvariantid: UUID, cartid: UUID, quantity: int = 1):

    cart_item=CartItem(product_variant_id=productvariantid, cart_id=cartid, quantity=quantity)
    db.add(cart_item)
    return cart_item


def get_product_from_cart(db: Session, cartid: UUID, productvariantid: UUID):
    cart_item=db.query(CartItem).filter(CartItem.cart_id==cartid, CartItem.product_variant_id==productvariantid).first()
    return cart_item

def get_cart_items(db: Session, current_user_id: UUID):
    cart_item_all = (
        db.query(
            CartItem.id.label("cart_item_id"),
            CartItem.quantity.label("cart_item_quantity"),

            product_variant.id.label("product_variant_id"),
            product_variant.price.label("product_variant_price"),
            product_variant.variant_name.label("variant_name"),
            product_variant.stock_quantity.label("product_variant_stock_quantity"),
            product_variant.isdeleted.label("product_variant_deleted"),

            Products.name.label("product_name"),
            Products.image.label("product_image"),
            Products.isdeleted.label("product_deleted"),
        ).join(CartItem.cart)
        .join(CartItem.product_variants)
        .join(product_variant.product)
        .filter(Cart.user_id == current_user_id).order_by(CartItem.created_at.desc(),CartItem.id.desc())
        .all()
    )

    return cart_item_all

def get_cart_items_for_order(db: Session, cart_id: UUID):
    cart_item_all=db.query(
        CartItem.id.label('cart_item_id'),
        CartItem.quantity.label('cart_item_quantity'),
        product_variant.id.label('product_variant_id'),
        product_variant.variant_name.label("product_variant_name"),
        product_variant.price.label('product_variant_price'),
        product_variant.stock_quantity.label('product_variant_quantity'),
        product_variant.isdeleted.label('product_variant_deleted'),
        Products.isdeleted.label('product_deleted'),
        Products.name.label("product_name"),
        Products.image.label("product_image")

    
        ).join(CartItem.product_variants).join(product_variant.product).filter(CartItem.cart_id == cart_id).all()
    return cart_item_all


def delete_cart_items_list(db: Session, cart_ids: set[UUID]):

        
    db.query(CartItem).filter(CartItem.id.in_(cart_ids)).delete(synchronize_session=False)
    return


def get_cart_items_reorder(db: Session, cart_id: UUID):
    user_cart_items=db.query(CartItem).options(joinedload(CartItem.product_variants).joinedload(product_variant.product)).filter(CartItem.cart_id==cart_id).all()
    return user_cart_items



def get_cart_item_by_cart_item_id(db: Session, current_user_id: UUID, cart_item_id: UUID):
    cart_item = (
        db.query(CartItem).join(CartItem.cart)
        .filter(
            CartItem.id == cart_item_id,
            Cart.user_id == current_user_id
        )
        .first()
    )

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found."
        )
    db.delete(cart_item)
    return cart_item


def get_cart_item_by_product_variant_id(db: Session, current_user_id: UUID, product_variant_id: UUID):
    cart_item = (
        db.query(CartItem)
        .join(CartItem.cart)
        .filter(
            CartItem.product_variant_id == product_variant_id,
            Cart.user_id == current_user_id
        )
        .first()
    )

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found."
        )
    return cart_item
