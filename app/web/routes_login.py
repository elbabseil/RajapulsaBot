from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


from app.web.auth import check_login

from app.database.user_repository import user_repository

from api.services.auth_service import verify_password





# =====================================
# ROUTER
# =====================================

router = APIRouter(
    tags=[
        "Admin Authentication"
    ]
)





templates = Jinja2Templates(
    directory="app/web/templates"
)







# =====================================
# LOGIN PAGE
# =====================================

@router.get(
    "/admin/login",
    response_class=HTMLResponse
)
async def login_page(

    request: Request

):


    # =================================
    # JIKA SUDAH LOGIN
    # =================================

    if check_login(request):

        return RedirectResponse(

            url="/admin",

            status_code=302

        )





    return templates.TemplateResponse(

        name="login.html",

        request=request,

        context={

            "error": None

        }

    )









# =====================================
# LOGIN ACTION
# =====================================

@router.post(
    "/admin/login"
)
async def login_process(

    request: Request,

    username: str = Form(...),

    password: str = Form(...)

):


    # =================================
    # CEK USER DATABASE
    # =================================


    user = user_repository.get_by_telegram_id(
        username
    )



    if user and verify_password(

        password,

        user["password_hash"]

    ):



        # =============================
        # CREATE SESSION
        # =============================


        request.session.clear()


        request.session["admin"] = True


        request.session["username"] = user["username"]



        print("==============================")
        print("[ADMIN LOGIN SUCCESS]")
        print("USER :", username)
        print("==============================")





        return RedirectResponse(

            url="/admin",

            status_code=303

        )









    # =================================
    # LOGIN FAILED
    # =================================


    print("==============================")
    print("[ADMIN LOGIN FAILED]")
    print("USER :", username)
    print("==============================")





    return templates.TemplateResponse(

        name="login.html",

        request=request,

        context={

            "error":
            "Username atau password salah"

        },

        status_code=401

    )









# =====================================
# LOGOUT
# =====================================

@router.get(
    "/admin/logout"
)
async def logout(

    request: Request

):


    username = request.session.get(

        "username",

        "-"

    )



    request.session.clear()



    print("==============================")
    print("[ADMIN LOGOUT]")
    print("USER :", username)
    print("==============================")





    return RedirectResponse(

        url="/admin/login",

        status_code=302

    )