from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.web.auth import check_login
from app.database.user_repository import user_repository
from api.services.auth_service import verify_password



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


    if check_login(request):

        return RedirectResponse(
            "/admin",
            status_code=302
        )



    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": None
        }
    )






# =====================================
# LOGIN PROCESS
# =====================================

@router.post(
    "/admin/login"
)
async def login_process(

    request: Request,

    username: str = Form(...),

    password: str = Form(...)

):


    print("==============================")
    print("[ADMIN LOGIN TRY]")
    print("USERNAME :", username)
    print("==============================")



    # cari user berdasarkan username

    user = user_repository.get_by_username(
        username
  )



    if not user:


        print("[USER NOT FOUND]")


        return templates.TemplateResponse(

            "login.html",

            {
                "request": request,
                "error":
                "Username tidak ditemukan"
            },

            status_code=401

        )





    # cek password


    if not verify_password(

        password,

        user["password_hash"]

    ):


        print("[PASSWORD WRONG]")


        return templates.TemplateResponse(

            "login.html",

            {
                "request": request,
                "error":
                "Password salah"
            },

            status_code=401

        )






    # ==========================
    # CREATE SESSION
    # ==========================


    request.session.clear()


    request.session["admin"] = True


    request.session["username"] = user["username"]



    print("==============================")
    print("[ADMIN LOGIN SUCCESS]")
    print("USER :", user["username"])
    print("==============================")





    return RedirectResponse(

        "/admin",

        status_code=303

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

        "/admin/login",

        status_code=302

    )