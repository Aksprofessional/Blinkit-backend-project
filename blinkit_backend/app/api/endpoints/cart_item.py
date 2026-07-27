from app.db.database import get_db
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.models.user import User
from uuid import UUID
from app.schemas.cart_item import AddItemResponse,UpdateCartItem,UpdateItemResponse,GetItemCartResponeFinal
from app.services.cart_item import add_product,update_cart_item,get_product_from_cart,delete_cart_item
from app.dependencies.auth import get_current_user



router=APIRouter()

# Add a product to the authenticated user's cart
@router.post('/add-product/{product_variant_id}',response_model=AddItemResponse)
def cart_item_add_product(product_variant_id: UUID, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):


    
    
    # Create a new cart item or update the quantity if it already exists
    cartitem= add_product(db,current_user,product_variant_id)
    return {
            "message": "product added/updated successfully",
            "cart_item": cartitem
        }
    


# Increment or decrement the quantity of a cart item
@router.patch('/{product_variant_id}')
def cart_items_update(product_variant_id: UUID, action: UpdateCartItem, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    # Update the cart item based on the requested action
    cartitem=update_cart_item(db,current_user,product_variant_id,action)

    # Return a response indicating whether the item was removed
    if cartitem.quantity == 0:
        return UpdateItemResponse(
            quantity=0,
            removed=True,
            cart_item_id=cartitem.id,
            message='the product is removed from cart'

        )
    else:
        return UpdateItemResponse(
            quantity=cartitem.quantity,
            removed=False,
            cart_item_id=cartitem.id,
            message='product quantity is updated in cart.'
        )


# Retrieve all cart items for the authenticated user
@router.get('',response_model=GetItemCartResponeFinal)
def cart_items_get_all(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    # Fetch cart items, total price, and unavailable cart item ids
    cart_items_all,total_price,unavailable_cart_item_ids=get_product_from_cart(db,current_user.id)

    return GetItemCartResponeFinal(
        cartitmes=cart_items_all,
        total=len(cart_items_all),
        total_price= total_price,
        unavailable_cart_item_ids=unavailable_cart_item_ids
    )


# Remove a specific cart item from the authenticated user's cart
@router.delete('/delete/{cart_item_id}')
def cart_item_delete(cart_item_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    # Delete the cart item and return its id
    cart_item=delete_cart_item(db,current_user.id,cart_item_id)
    return{
        
        "id":cart_item.id,
        "message":'successfully removed'
    }