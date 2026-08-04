from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database.user_repository import user_repository
from app.database.product_repository import product_repository
from app.database.transaction_repository import transaction_repository

from app.web.auth import require_login


router = APIRouter(
    tags=["FlashPay Admin"]
)

templates = Jinja2Templates(
    directory="app/web/templates"
)


@router.get(
    "/admin",
    response_class=HTMLResponse
)
async def dashboard(request: Request):

    redirect = require_login(request)

    if redirect:
        return redirect

    try:

        print("========== DASHBOARD ==========")

        print("1. Count User")
        total_user = user_repository.count_users() or 0

        print("2. Produk")
        products = product_repository.get_all() or []
        total_produk = len(products)

        print("3. Total Transaksi")
        total_transaksi = transaction_repository.count_transactions() or 0

        print("4. Pending")
        pending = transaction_repository.count_pending() or 0

        print("5. Success")
        berhasil = transaction_repository.count_success() or 0

        print("6. Failed")
        gagal = transaction_repository.count_failed() or 0

        print("7. Omzet")
        omzet = transaction_repository.total_revenue() or 0

        print("8. Latest")
        transaksi = transaction_repository.get_latest() or []

        dashboard_data = {
            "total_user": total_user,
            "total_produk": total_produk,
            "total_transaksi": total_transaksi,
            "pending": pending,
            "berhasil": berhasil,
            "gagal": gagal,
            "omzet": omzet,
            "transaksi": transaksi,
            "chart": {
                "total": total_transaksi,
                "pending": pending,
                "success": berhasil,
                "failed": gagal,
            },
        }

        print("9. Render Template")

        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "data": dashboard_data,
                "admin_name": request.session.get(
                    "username",
                    "Administrator"
                ),
            },
        )

    except Exception as e:

        print("==============================")
        print("DASHBOARD ERROR")
        print(type(e).__name__)
        print(e)
        print("==============================")

        import traceback
        traceback.print_exc()

        return HTMLResponse(
            f"""
            <html>
            <body style="font-family:Arial;padding:40px">
                <h2>Dashboard Error</h2>
                <hr>
                <pre>{type(e).__name__}: {e}</pre>
            </body>
            </html>
            """,
            status_code=500,
        )