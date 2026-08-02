from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database.product_repository import product_repository
from app.web.auth import require_login


router = APIRouter()

templates = Jinja2Templates(
    directory="app/web/templates"
)


# =====================================
# PRODUCT MANAGEMENT
# =====================================

@router.get(
    "/admin/products",
    response_class=HTMLResponse
)
async def products_dashboard(
    request: Request
):

    # =====================================
    # LOGIN CHECK
    # =====================================

    redirect = require_login(request)

    if redirect:
        return redirect

    try:

        # =====================================
        # LOAD PRODUCTS
        # =====================================

        products = product_repository.get_all() or []

        total_product = len(products)

        # =====================================
        # TEMPLATE DATA
        # =====================================

        context = {
            "request": request,
            "title": "Product Management",
            "products": products,
            "total_product": total_product,
            "admin_name": request.session.get(
                "username",
                "Administrator"
            )
        }

        # =====================================
        # RENDER TEMPLATE
        # =====================================

        return templates.TemplateResponse(
            request=request,
            name="products.html",
            context=context
        )

    except Exception as e:

        print("==============================")
        print("[PRODUCT DASHBOARD ERROR]")
        print(type(e).__name__)
        print(e)
        print("==============================")

        return HTMLResponse(
            content=f"""
<!DOCTYPE html>
<html lang="id">

<head>
<meta charset="utf-8">
<title>Product Dashboard Error</title>
</head>

<body style="font-family:Arial;padding:40px;">

<h2>❌ Product Dashboard Error</h2>

<hr>

<p>Terjadi kesalahan saat membuka halaman Product Management.</p>

<pre>{type(e).__name__}: {e}</pre>

</body>

</html>
""",
            status_code=500
        )