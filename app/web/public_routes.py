from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path


router = APIRouter()


WEB_PATH = Path(
    "app/web/static"
)



def page(filename):

    file = WEB_PATH / filename

    if not file.exists():

        return {
            "error": f"{filename} tidak ditemukan"
        }


    return FileResponse(
        file
    )



# ===============================
# PUBLIC WEBSITE
# ===============================


@router.get("/")
async def home():

    return page(
        "index.html"
    )



@router.get("/layanan")
async def layanan():

    return page(
        "layanan.html"
    )



@router.get("/produk")
async def produk():

    return page(
        "produk.html"
    )



@router.get("/kategori")
async def kategori():

    return page(
        "kategori.html"
    )



@router.get("/merchant")
async def merchant():

    return page(
        "merchant.html"
    )



# ===============================
# PRODUCT LIST
# ===============================


@router.get("/produk-list")
async def produk_list():

    return page(
        "produk_list.html"
    )



@router.get("/kontak")
async def kontak():

    return page(
        "kontak.html"
    )



@router.get("/checkout")
async def checkout():

    return page(
        "checkout.html"
    )



@router.get("/payment")
async def payment():

    return page(
        "payment.html"
    )



@router.get("/privacy-policy")
async def privacy():

    return page(
        "privacy.html"
    )



@router.get("/refund-policy")
async def refund():

    return page(
        "refund.html"
    )



@router.get("/terms-condition")
async def terms():

    return page(
        "terms.html"
    )