from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from app.database.user_repository import user_repository
from app.database.product_repository import product_repository
from app.database.transaction_repository import transaction_repository

from app.web.auth import require_login






router = APIRouter(
    prefix="",
    tags=[
        "FlashPay Admin"
    ]
)





templates = Jinja2Templates(
    directory="app/web/templates"
)









# =====================================
# ADMIN DASHBOARD
# =====================================


@router.get(
    "/admin",
    response_class=HTMLResponse
)
async def dashboard(

    request: Request

):


    # =====================================
    # LOGIN PROTECTION
    # =====================================


    redirect = require_login(request)


    if redirect:

        return redirect





    try:


        # =====================================
        # DATABASE STATISTICS
        # =====================================


        total_user = (

            user_repository.count_users()

            or 0

        )




        products = (

            product_repository.get_all()

            or []

        )



        total_produk = len(products)





        total_transaksi = (

            transaction_repository.count_transactions()

            or 0

        )





        pending = (

            transaction_repository.count_pending()

            or 0

        )





        berhasil = (

            transaction_repository.count_success()

            or 0

        )





        gagal = (

            transaction_repository.count_failed()

            or 0

        )





        omzet = (

            transaction_repository.total_revenue()

            or 0

        )





        transaksi = (

            transaction_repository.get_latest()

            or []

        )









        # =====================================
        # CHART DATA
        # =====================================


        chart = {


            "total":

            total_transaksi,



            "pending":

            pending,



            "success":

            berhasil,



            "failed":

            gagal


        }









        # =====================================
        # DASHBOARD DATA
        # =====================================


        dashboard_data = {


            "total_user":

            total_user,



            "total_produk":

            total_produk,



            "total_transaksi":

            total_transaksi,



            "pending":

            pending,



            "berhasil":

            berhasil,



            "gagal":

            gagal,



            "omzet":

            omzet,



            "transaksi":

            transaksi,



            "chart":

            chart


        }









        # =====================================
        # RENDER DASHBOARD
        # =====================================


        return templates.TemplateResponse(


            name="dashboard.html",


            request=request,


            context={


                "data":

                dashboard_data,



                "admin_name":

                request.session.get(

                    "username",

                    "Administrator"

                )


            }


        )








    except Exception as e:



        print("==============================")

        print("[DASHBOARD ERROR]")

        print(type(e).__name__)

        print(e)

        print("==============================")





        return HTMLResponse(


            content=f"""

<html>

<head>

<title>
Dashboard Error
</title>

</head>


<body style="font-family:Arial;padding:40px">


<h2>
❌ Dashboard Error
</h2>


<hr>


<pre>
{type(e).__name__}: {e}
</pre>


</body>

</html>

""",


            status_code=500


        )