from app.db.database import SessionLocal

from app.models.category import Category
from app.models.sub_category import SubCategory
from app.models.brand import brand
from app.models.products import Products
from app.models.product_variant import product_variant
from app.models.collection import Collection
from app.models.collection_subcategory import CollectionSubCategory
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.user import User
from app.models.orders import order
from app.models.order_items import order_items
from app.models.delivery_address import delivery_address

db = SessionLocal()

category_names = [
    "Fruits & Vegetables",
    "Dairy & Breakfast",
    "Snacks",
    "Beverages",
    "Bakery",
    "Personal Care",
    "Cleaning Essentials",
    "Baby Care",
]

for name in category_names:
    existing = db.query(Category).filter(Category.name == name).first()

    if not existing:
        db.add(Category(name=name))

db.commit()

print("Categories seeded successfully!")



subcategory_data = {
    "Fruits & Vegetables": [
        "Fresh Fruits",
        "Fresh Vegetables",
        "Herbs",
    ],

    "Dairy & Breakfast": [
        "Milk",
        "Curd",
        "Butter & Cheese",
    ],

    "Snacks": [
        "Chips",
        "Namkeen",
        "Biscuits",
    ],

    "Beverages": [
        "Soft Drinks",
        "Juices",
        "Tea & Coffee",
    ],

    "Bakery": [
        "Bread",
        "Cakes",
    ],

    "Personal Care": [
        "Soap",
        "Shampoo",
        "Toothpaste",
    ],

    "Cleaning Essentials": [
        "Detergent",
        "Floor Cleaner",
    ],

    "Baby Care": [
        "Diapers",
        "Baby Food",
    ]
}


for category_name, subcategories in subcategory_data.items():

    category = db.query(Category).filter(
        Category.name == category_name
    ).first()

    for subcategory_name in subcategories:

        exists = db.query(SubCategory).filter(
            SubCategory.name == subcategory_name
        ).first()

        if not exists:

            db.add(
                SubCategory(
                    name=subcategory_name,
                    category_id=category.id
                )
            )

db.commit()

print("Subcategories seeded successfully!")



brands = [
    {"name": "Amul", "logo": None, "is_active": True},
    {"name": "Mother Dairy", "logo": None, "is_active": True},
    {"name": "Nestlé", "logo": None, "is_active": True},
    {"name": "Britannia", "logo": None, "is_active": True},
    {"name": "Coca-Cola", "logo": None, "is_active": True},
    {"name": "Pepsi", "logo": None, "is_active": True},
    {"name": "Lay's", "logo": None, "is_active": True},
    {"name": "Haldiram", "logo": None, "is_active": True},
    {"name": "Parle", "logo": None, "is_active": True},
    {"name": "Tata Tea", "logo": None, "is_active": True},
    {"name": "Colgate", "logo": None, "is_active": True},
    {"name": "Dove", "logo": None, "is_active": True},
    {"name": "Surf Excel", "logo": None, "is_active": True},
    {"name": "Harpic", "logo": None, "is_active": False},
    {"name": "Dettol", "logo": None, "is_active": False},
]



for brand_data in brands:

    existing = (
        db.query(brand)
        .filter(brand.name == brand_data["name"])
        .first()
    )

    if existing:
        continue

    db.add(
        brand(
            name=brand_data["name"],
            logo=brand_data["logo"],
            is_active=brand_data["is_active"],
        )
    )

db.commit()

print("Brands seeded successfully!")








products = [
    {
        "name": "Amul Gold Milk",
        "brand": "Amul",
        "subcategory": "Milk",
        "description": "Full cream fresh milk",
        "image": "amul_gold_milk.jpg",
        "isdeleted": False,
    },
    {
        "name": "Amul Butter",
        "brand": "Amul",
        "subcategory": "Butter & Cheese",
        "description": "Salted butter",
        "image": "amul_butter.jpg",
        "isdeleted": False,
    },
    {
        "name": "Mother Dairy Toned Milk",
        "brand": "Mother Dairy",
        "subcategory": "Milk",
        "description": "Toned milk",
        "image": "mother_dairy_milk.jpg",
        "isdeleted": False,
    },
    {
        "name": "Lay's Magic Masala",
        "brand": "Lay's",
        "subcategory": "Chips",
        "description": "Potato chips",
        "image": "lays_magic_masala.jpg",
        "isdeleted": False,
    },
    {
        "name": "Haldiram Aloo Bhujia",
        "brand": "Haldiram",
        "subcategory": "Namkeen",
        "description": "Crunchy namkeen",
        "image": "haldiram_aloo_bhujia.jpg",
        "isdeleted": False,
    },
    {
        "name": "Coca-Cola",
        "brand": "Coca-Cola",
        "subcategory": "Soft Drinks",
        "description": "Soft drink",
        "image": "coca_cola.jpg",
        "isdeleted": False,
    },
    {
        "name": "Pepsi",
        "brand": "Pepsi",
        "subcategory": "Soft Drinks",
        "description": "Soft drink",
        "image": "pepsi.jpg",
        "isdeleted": False,
    },
    {
        "name": "Britannia Bread",
        "brand": "Britannia",
        "subcategory": "Bread",
        "description": "Fresh bread",
        "image": "britannia_bread.jpg",
        "isdeleted": False,
    },
    {
        "name": "Tata Tea Premium",
        "brand": "Tata Tea",
        "subcategory": "Tea & Coffee",
        "description": "Premium tea",
        "image": "tata_tea.jpg",
        "isdeleted": False,
    },
    {
        "name": "Colgate Strong Teeth",
        "brand": "Colgate",
        "subcategory": "Toothpaste",
        "description": "Toothpaste",
        "image": "colgate.jpg",
        "isdeleted": False,
    },
]


for product_data in products:

    existing = (
        db.query(Products)
        .filter(Products.name == product_data["name"])
        .first()
    )

    if existing:
        continue

    product_brand = (
        db.query(brand)
        .filter(brand.name == product_data["brand"])
        .first()
    )

    product_subcategory = (
        db.query(SubCategory)
        .filter(SubCategory.name == product_data["subcategory"])
        .first()
    )

    db.add(
        Products(
            name=product_data["name"],
            image=product_data["image"],
            description=product_data["description"],
            brand_id=product_brand.id,
            sub_category_id=product_subcategory.id,
            isdeleted=product_data["isdeleted"],
        )
    )

db.commit()

print("Products seeded successfully!")







variants = [
    {
        "product": "Amul Gold Milk",
        "variant_name": "500 ml",
        "price": 34,
        "stock": 120,
        "sku": "AMUL-GOLD-500",
        "isdeleted": False,
    },
    {
        "product": "Amul Gold Milk",
        "variant_name": "1 L",
        "price": 68,
        "stock": 90,
        "sku": "AMUL-GOLD-1L",
        "isdeleted": False,
    },

    {
        "product": "Amul Butter",
        "variant_name": "100 g",
        "price": 58,
        "stock": 80,
        "sku": "AMUL-BUTTER-100",
        "isdeleted": False,
    },
    {
        "product": "Amul Butter",
        "variant_name": "500 g",
        "price": 255,
        "stock": 35,
        "sku": "AMUL-BUTTER-500",
        "isdeleted": False,
    },

    {
        "product": "Lay's Magic Masala",
        "variant_name": "52 g",
        "price": 20,
        "stock": 150,
        "sku": "LAYS-MM-52",
        "isdeleted": False,
    },
    {
        "product": "Lay's Magic Masala",
        "variant_name": "104 g",
        "price": 38,
        "stock": 100,
        "sku": "LAYS-MM-104",
        "isdeleted": False,
    },

    {
        "product": "Coca-Cola",
        "variant_name": "750 ml",
        "price": 40,
        "stock": 95,
        "sku": "COKE-750",
        "isdeleted": False,
    },
    {
        "product": "Coca-Cola",
        "variant_name": "2 L",
        "price": 99,
        "stock": 40,
        "sku": "COKE-2L",
        "isdeleted": False,
    },

    {
        "product": "Pepsi",
        "variant_name": "750 ml",
        "price": 40,
        "stock": 90,
        "sku": "PEPSI-750",
        "isdeleted": False,
    },
    {
        "product": "Pepsi",
        "variant_name": "2 L",
        "price": 99,
        "stock": 45,
        "sku": "PEPSI-2L",
        "isdeleted": True,
    }
]



for variant_data in variants:

    existing = (
        db.query(product_variant)
        .filter(product_variant.sku == variant_data["sku"])
        .first()
    )

    if existing:
        continue

    product = (
        db.query(Products)
        .filter(Products.name == variant_data["product"])
        .first()
    )

    db.add(
        product_variant(
            product_id=product.id,
            sku=variant_data["sku"],
            price=variant_data["price"],
            stock_quantity=variant_data["stock"],
            variant_name=variant_data["variant_name"],
            isdeleted=variant_data["isdeleted"],
        )
    )

db.commit()

print("Product variants seeded successfully!")








collections = [
    {"name": "Best Sellers", "display_order": 1, "is_active": True},
    {"name": "Daily Essentials", "display_order": 2, "is_active": True},
    {"name": "Breakfast Favorites", "display_order": 3, "is_active": True},
    {"name": "Healthy Choices", "display_order": 4, "is_active": True},
    {"name": "Cold Drinks", "display_order": 5, "is_active": True},
    {"name": "Snacking Time", "display_order": 6, "is_active": True},
    {"name": "Home Cleaning", "display_order": 7, "is_active": True},
    {"name": "Old Collections", "display_order": 8, "is_active": False},
]

for collection_data in collections:

    existing = (
        db.query(Collection)
        .filter(Collection.name == collection_data["name"])
        .first()
    )

    if existing:
        continue

    db.add(
        Collection(
            name=collection_data["name"],
            display_order=collection_data["display_order"],
            is_active=collection_data["is_active"],
        )
    )

db.commit()

print("Collections seeded successfully!")







collection_mapping = {

    "Best Sellers": [
        "Milk",
        "Soft Drinks",
        "Chips",
        "Bread",
    ],

    "Daily Essentials": [
        "Milk",
        "Bread",
        "Soap",
        "Toothpaste",
    ],

    "Breakfast Favorites": [
        "Milk",
        "Butter & Cheese",
        "Bread",
        "Tea & Coffee",
    ],

    "Healthy Choices": [
        "Fresh Fruits",
        "Fresh Vegetables",
        "Herbs",
        "Juices",
    ],

    "Cold Drinks": [
        "Soft Drinks",
        "Juices",
    ],

    "Snacking Time": [
        "Chips",
        "Namkeen",
        "Biscuits",
    ],

    "Home Cleaning": [
        "Detergent",
        "Floor Cleaner",
    ],
}

for collection_name, subcategories in collection_mapping.items():

    collection = (
        db.query(Collection)
        .filter(Collection.name == collection_name)
        .first()
    )

    for subcategory_name in subcategories:

        subcategory = (
            db.query(SubCategory)
            .filter(SubCategory.name == subcategory_name)
            .first()
        )

        existing = (
            db.query(CollectionSubCategory)
            .filter(
                CollectionSubCategory.collection_id == collection.id,
                CollectionSubCategory.subcategory_id == subcategory.id,
            )
            .first()
        )

        if existing:
            continue

        db.add(
            CollectionSubCategory(
                collection_id=collection.id,
                subcategory_id=subcategory.id,
                display_order=1,
            )
        )

db.commit()

print("Collection mappings seeded successfully!")



























db.close()
