from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database.transaction_repository import transaction_repository
from app.web.auth import require_login


router = APIRouter()


templates = Jinja2Templates(
    directory="app/web/templates"
)



# =====================================
# TRANSACTION LIST
# =====================================

@router.get(
    "/admin/transactions",
    response_class=HTMLResponse
)
async def transactions_page(
    request: Request
):


    redirect = require_login(request)

    if redirect:
        return redirect



    transactions = (
        transaction_repository.get_latest()
        or []
    )


    context = {

        "request": request,

        "transactions": transactions,


        "total_transaction":
            transaction_repository.count_transactions(),


        "pending":
            transaction_repository.count_pending(),


        "success":
            transaction_repository.count_success(),


        "failed":
            transaction_repository.count_failed()

    }



    return templates.TemplateResponse(

        name="transactions.html",

        request=request,

        context=context

    )







# =====================================
# TRANSACTION DETAIL
# =====================================


@router.get(
    "/admin/transactions/{trx_id}",
    response_class=HTMLResponse
)
async def transaction_detail(

    request: Request,

    trx_id:str

):


    redirect = require_login(request)

    if redirect:
        return redirect



    trx = (
        transaction_repository
        .get_by_trx_id(trx_id)
    )



    if not trx:

        return HTMLResponse(

            """

            <h2>
            ❌ Transaction Not Found
            </h2>

            """

        )



    return templates.TemplateResponse(

        name="transaction_detail.html",

        request=request,

        context={

            "trx":trx

        }

    )








# =====================================
# UPDATE TRANSACTION STATUS
# =====================================


@router.get(
    "/admin/transactions/{trx_id}/status/{status}"
)
async def update_transaction_status(

    request:Request,

    trx_id:str,

    status:str

):


    redirect = require_login(request)

    if redirect:
        return redirect



    status = status.upper()



    allowed = [

        "PENDING",

        "PROCESSING",

        "SUCCESS",

        "FAILED"

    ]



    if status not in allowed:


        return HTMLResponse(

            "Invalid Status"

        )




    transaction_repository.update_status(

        trx_id,

        transaction_status=status

    )



    return RedirectResponse(

        "/admin/transactions",

        status_code=302

    )