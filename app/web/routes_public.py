from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path


router = APIRouter()



STATIC_DIR = Path(
    "app/web/static"
)



def load_page(filename):

    file = STATIC_DIR / filename

    if not file.exists():

        return HTMLResponse(

            content=f"""
            <h1>404</h1>
            <p>Halaman {filename} tidak ditemukan</p>
            """,

            status_code=404

        )


    return HTMLResponse(

        content=file.read_text(
            encoding="utf-8"
        )

    )





# =====================================
# WEBSITE PUBLIC
# =====================================


@router.get(
    "/",
    response_class=HTMLResponse
)
def home():

    return load_page(
        "index.html"
    )




@router.get(
    "/layanan",
    response_class=HTMLResponse
)
def layanan():

    return load_page(
        "layanan.html"
    )





@router.get(
    "/produk",
    response_class=HTMLResponse
)
def produk():

    return load_page(
        "produk.html"
    )





@router.get(
    "/kontak",
    response_class=HTMLResponse
)
def kontak():

    return load_page(
        "kontak.html"
    )





@router.get(
    "/privacy-policy",
    response_class=HTMLResponse
)
def privacy():

    return load_page(
        "privacy.html"
    )





@router.get(
    "/terms-condition",
    response_class=HTMLResponse
)
def terms():

    return load_page(
        "terms.html"
    )