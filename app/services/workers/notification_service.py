from app.loader import bot



class NotificationService:


    async def send_success(

        self,

        chat_id,

        order

    ):


        message = f"""
✅ TRANSAKSI BERHASIL

Produk:
{order['product_name']}

Nomor:
{order['customer_no']}

SN:
{order['sn']}

Ref ID:
{order['ref_id']}
"""


        await bot.send_message(

            chat_id,

            message

        )





    async def send_failed(

        self,

        chat_id,

        order

    ):


        message = f"""
❌ TRANSAKSI GAGAL

Produk:
{order['product_name']}

Nomor:
{order['customer_no']}

Ref ID:
{order['ref_id']}

Silakan hubungi admin.
"""


        await bot.send_message(

            chat_id,

            message

        )





notification_service = NotificationService()