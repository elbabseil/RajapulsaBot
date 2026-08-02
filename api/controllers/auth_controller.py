from fastapi import APIRouter

from api.schemas.auth_schema import (
    RegisterSchema,
    LoginSchema
)

from api.services.auth_service import (
    hash_password,
    verify_password,
    create_token
)

from app.database.user_repository import user_repository


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    data: RegisterSchema
):

    # cek user sudah ada
    existing = user_repository.get_by_telegram_id(
        data.username
    )

    if existing:

        return {
            "status": "failed",
            "message": "Username sudah digunakan"
        }


    password_hash = hash_password(
        data.password
    )


    conn = user_repository


    from app.database.connection import get_connection


    db = get_connection()


    db.execute(
        """
        INSERT INTO users
        (
            telegram_id,
            username,
            full_name,
            password_hash
        )
        VALUES (?,?,?,?)
        """,
        (
            data.username,
            data.username,
            data.full_name,
            password_hash
        )
    )


    db.commit()
    db.close()


    return {

        "status": "success",

        "message":
        "Akun berhasil dibuat"

    }



@router.post("/login")
def login(
    data: LoginSchema
):


    user = user_repository.get_by_telegram_id(
        data.username
    )


    if not user:

        return {

            "status":"failed",

            "message":
            "User tidak ditemukan"

        }



    if not verify_password(
        data.password,
        user["password_hash"]
    ):

        return {

            "status":"failed",

            "message":
            "Password salah"

        }



    token = create_token(
        data.username
    )


    return {

        "status":"success",

        "username":
        user["username"],

        "full_name":
        user["full_name"],

        "token":
        token

    }