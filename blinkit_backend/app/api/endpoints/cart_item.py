from app.db.database import get_db
from fastapi import HTTPException,APIRouter,Depends,status,Request,Body
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories import cart
from uuid import UUID
from app.repositories.product_variant import get_product_variant
from app.repositories import cart_item
from app.schemas.cart_item import AddItemResponse,UpdateCartItem,UpdateItemResponse,GetItemCartResponeFinal
from app.dependencies.permissions import check_user_is_deleted
from app.services.cart_item import add_product,update_cart_item,get_product_from_cart,delete_cart_item
from app.dependencies.auth import get_current_user



router=APIRouter()

#adding a product to user cart
@router.post('/add-product/{product_variant_id}',response_model=AddItemResponse)
def cart_item_add_product(product_variant_id: UUID, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):


    
    
    cartitem= add_product(db,current_user,product_variant_id)
    return {
            "message": "product added/updated successfully",
            "cart_item": cartitem
        }
    


@router.patch('/{product_variant_id}')
def cart_items_update(product_variant_id: UUID, action: UpdateCartItem, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    cartitem=update_cart_item(db,current_user,product_variant_id,action)
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


@router.get('',response_model=GetItemCartResponeFinal)
def cart_items_get_all(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart_items_all,total_price,unavailable_cart_item_ids=get_product_from_cart(db,current_user.id)

    return GetItemCartResponeFinal(
        cartitmes=cart_items_all,
        total=len(cart_items_all),
        total_price= total_price,
        unavailable_cart_item_ids=unavailable_cart_item_ids
    )


@router.delete('/delete/{cart_item_id}')
def cart_items_get_all(cart_item_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart_item=delete_cart_item(db,current_user.id,cart_item_id)
    return{
        
        "id":cart_item.id,
        "message":'successfully removed'
    }





    
        



            



    
    


