from fastapi import APIRouter

from app.database.product_repository import product_repository


router = APIRouter(
    prefix="/public",
    tags=["Public Website"]
)



@router.get("/products")
def public_products():

    try:

        products = product_repository.get_all()


        result = []


        for p in products:

            result.append({

                "id": p.get("id"),

                "category": p.get("category"),

                "brand": p.get("brand"),

                "name": p.get("product_name")
                or p.get("name"),

                "sku": p.get("sku"),

                "price": p.get("price")

            })


        return {

            "status": "success",

            "total": len(result),

            "products": result

        }



    except Exception as e:

        return {

            "status": "error",

            "message": str(e)

        }



# ==================================
# PUBLIC WEBSITE CATEGORIES
# ==================================

@router.get("/categories")
def public_categories():

    try:

        products = product_repository.get_all()


        categories = []


        for p in products:

            category = p.get("category")


            if category and category not in categories:

                categories.append(category)



        return {

            "status": "success",

            "total": len(categories),

            "categories": sorted(categories)

        }



    except Exception as e:

        return {

            "status": "error",

            "message": str(e)

        }





@router.get("/products/category/{category}")
def products_by_category(category: str):

    try:

        products = product_repository.get_all()

        result = []


        for p in products:

            if p.get("category","").lower() == category.lower():

                result.append({

                    "id": p.get("id"),

                    "brand": p.get("brand"),

                    "name": p.get("product_name")
                    or p.get("name"),

                    "price": p.get("price")

                })


        return {

            "status": "success",

            "category": category,

            "total": len(result),

            "products": result

        }


    except Exception as e:

        return {

            "status":"error",

            "message":str(e)

        }    


# ==================================
# PUBLIC PRODUCT DETAIL
# ==================================

@router.get("/products/detail/{product_id}")
def product_detail(product_id: int):

    try:

        products = product_repository.get_all()


        product = None


        for p in products:

            if p.get("id") == product_id:

                product = p
                break



        if not product:

            return {

                "status": "error",

                "message": "Product tidak ditemukan"

            }



        return {

            "status": "success",

            "product": {

                "id": product.get("id"),

                "category": product.get("category"),

                "brand": product.get("brand"),

                "name": product.get("product_name")
                or product.get("name"),

                "sku": product.get("sku"),

                "price": product.get("price")

            }

        }



    except Exception as e:

        return {

            "status": "error",

            "message": str(e)

        }