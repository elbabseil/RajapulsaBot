from fastapi import Request
from fastapi.responses import RedirectResponse



# =====================================
# ADMIN ACCOUNT
# =====================================

ADMIN_USERNAME = "admin"

ADMIN_PASSWORD = "flashpay123"





# =====================================
# CHECK LOGIN
# =====================================

def check_login(
    request: Request
):

    return request.session.get(
        "admin",
        False
    ) is True







# =====================================
# REQUIRE LOGIN
# =====================================

def require_login(
    request: Request
):

    if not check_login(request):

        return RedirectResponse(

            url="/admin/login",

            status_code=302

        )


    return None