from app.database.user_repository import user_repository



class UserService:


    def __init__(self):

        user_repository.create_table()



    # =====================================
    # REGISTER USER
    # =====================================

    def register(
        self,
        telegram_id,
        username=None,
        full_name=None
    ):

        return user_repository.create_user(

            telegram_id,

            username,

            full_name

        )



    # =====================================
    # GET USER
    # =====================================

    def get_user(
        self,
        telegram_id
    ):

        return user_repository.get_by_telegram_id(

            telegram_id

        )



    # =====================================
    # TOPUP
    # =====================================

    def topup(
        self,
        telegram_id,
        amount
    ):

        return user_repository.add_balance(

            telegram_id,

            amount

        )



    # =====================================
    # PURCHASE
    # =====================================

    def purchase(
        self,
        telegram_id,
        amount
    ):

        return user_repository.subtract_balance(

            telegram_id,

            amount

        )



user_service = UserService()