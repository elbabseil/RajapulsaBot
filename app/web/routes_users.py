from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database.user_repository import user_repository
from app.web.auth import require_login


router = APIRouter()

templates = Jinja2Templates(
    directory="app/web/templates"
)


# =====================================
# USER MANAGEMENT
# =====================================

@router.get(
    "/admin/users",
    response_class=HTMLResponse
)
async def users_dashboard(
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
        # LOAD DATA
        # =====================================

        users = user_repository.get_all() or []

        total_user = len(users)

        total_balance = user_repository.total_balance() or 0

        active_user = sum(
            1 for user in users
            if user.get("status") == "ACTIVE"
        )

        inactive_user = total_user - active_user

        # =====================================
        # TEMPLATE DATA
        # =====================================

        context = {
            "request": request,
            "title": "User Management",
            "users": users,
            "total_user": total_user,
            "total_balance": total_balance,
            "active_user": active_user,
            "inactive_user": inactive_user,
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
            name="users.html",
            context=context
        )

    except Exception as e:

        print("==============================")
        print("[USER DASHBOARD ERROR]")
        print(type(e).__name__)
        print(e)
        print("==============================")

        return HTMLResponse(
            content=f"""
<!DOCTYPE html>
<html lang="id">

<head>
<meta charset="utf-8">
<title>User Dashboard Error</title>
</head>

<body style="font-family:Arial;padding:40px">

<h2>❌ User Dashboard Error</h2>

<hr>

<p>Terjadi kesalahan saat membuka halaman User Management.</p>

<pre>{type(e).__name__}: {e}</pre>

</body>

</html>
""",
            status_code=500
        )