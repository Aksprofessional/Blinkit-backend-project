from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories import cart_item
from fastapi import HTTPException,status
from app.utils.db import commit_or_500
from app.services.products import check_product_variant_exist
from app.services.cart import cart_create_or_get
from uuid import UUID
from app.repositories.cart_item import get_cart_items,get_cart_item_by_cart_item_id,get_cart_item_by_product_variant_id
from app.schemas.cart_item import CartItemAction,GetCartItemResponse
from app.models.products import PrductStockType



# Check whether a specific product variant exists in the user's cart
def cart_item_exist(db: Session,cart_id: UUID, product_variant_id: UUID):

    # Retrieve the cart item
    cartitem=cart_item.get_product_from_cart(db,cart_id,product_variant_id)

    # Raise an exception if the product is not present in the cart
    if cartitem is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='no such product in cart.'
        )
    return cartitem


# Add a product variant to the authenticated user's cart
def add_product(db: Session, current_user: User, product_variant_id: UUID):

    

    # Verify that the product variant exists
    product_variant=check_product_variant_exist(db,product_variant_id)

    # Prevent adding products that are out of stock
    if product_variant.stock_quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The product is out of stock."
        )

    # Retrieve the user's cart or create one if it does not exist
    user_cart,created =cart_create_or_get(db,current_user.id)

    # Check whether the product already exists in the cart
    if not created:
        cartitem=cart_item.get_product_from_cart(db,user_cart.id,product_variant_id)
        if cartitem:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='product already exists in cart.'
            )

    # Add the product to the cart
    cartitem=cart_item.add_product_cart_item(db,product_variant_id,user_cart.id)

    # Commit the transaction
    message_error='product could not be added to the cart'
    commit_or_500(db,message_error)

    
    
    return cartitem
            


# Update the quantity of a cart item
def update_cart_item(db: Session, current_user: User, product_variant_id: int, action: CartItemAction):

    # Verify that the product variant exists
    product_variant=check_product_variant_exist(db,product_variant_id)

    # Retrieve the cart item
    cartitem=get_cart_item_by_product_variant_id(db,current_user.id,product_variant_id)

    # Increase the quantity if sufficient stock is available
    if action.action == CartItemAction.INCREMENT:
        if product_variant.stock_quantity>=cartitem.quantity+1:
            cartitem.quantity += 1
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Insufficient stock."
            )

    # Decrease the quantity or remove the item if it reaches zero
    elif action.action == CartItemAction.DECREMENT:
        if cartitem.quantity == 1:
            cartitem.quantity = 0
            db.delete(cartitem)
        elif cartitem.quantity < 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='the product quantity is already 0'
            )
        else:
            cartitem.quantity -= 1

    # Reject unsupported actions
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="you cannot do the provided action."
        )

    
    # Commit the transaction
    message_error='product could not be updated to the cart'
    commit_or_500(db,message_error)

    return cartitem


# Retrieve all cart items for a user
def get_product_from_cart(db: Session, current_user_id: UUID):

    # Fetch all cart items
    rows = get_cart_items(db, current_user_id)

    # Store ids of unavailable cart items
    unavailable_cart_item_ids=set()

    # Ensure the cart is not empty
    if not rows:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no products in cart"
        )

    all_items = []
    total_price = 0

    # Process each cart item
    for row in rows:
        row_data = dict(row._mapping)

        

        # Product has been deleted
        if row_data["product_deleted"]:
            row_data["is_available"] = False
            row_data["unavailable_reason"] = PrductStockType.PRODCUT_DELETED.value
            unavailable_cart_item_ids.add(row_data["cart_item_id"])

        # Product variant has been deleted
        elif row_data["product_variant_deleted"]:
            row_data["is_available"] = False
            row_data["unavailable_reason"] = PrductStockType.PRODUCT_VARIANT_DELETED.value
            unavailable_cart_item_ids.add(row_data["cart_item_id"])

        # Product variant is out of stock
        elif row_data["product_variant_stock_quantity"] == 0:
            row_data["is_available"] = False
            row_data["unavailable_reason"] = PrductStockType.OUT_OF_STOCK.value
            unavailable_cart_item_ids.add(row_data["cart_item_id"])

        # Requested quantity exceeds available stock
        elif row_data["cart_item_quantity"] > row_data["product_variant_stock_quantity"]:
            row_data["is_available"] = False
            row_data["unavailable_reason"] = PrductStockType.INSUFFICIENT_STOCK.value



        else:
            
            # Calculate the total price for the cart item
            row_data["item_total"]=(row_data["product_variant_price"]* row_data["cart_item_quantity"])

            # Add the item total to the overall cart total
            total_price += row_data["item_total"]

            # Mark the item as available
            row_data["is_available"] = True
            row_data["unavailable_reason"] = None

        # Convert the row into the response schema
        all_items.append(GetCartItemResponse.model_validate(row_data))

    return all_items, total_price, unavailable_cart_item_ids



# Delete a cart item
def delete_cart_item(db: Session, current_user_id: UUID,cart_item_id: UUID):

    # Retrieve and delete the specified cart item
    cart_item=get_cart_item_by_cart_item_id(db,current_user_id,cart_item_id)

    # Commit the transaction
    commit_or_500(db,'cart item could not be deleted')

    return cart_item