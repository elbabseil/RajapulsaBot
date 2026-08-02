# =================================================
# CEK PEMBAYARAN
# =================================================

@router.callback_query(
    F.data.startswith("check:")
)
async def check_payment(
    callback: types.CallbackQuery
):


    ref_id = callback.data.split(":")[1]



    trx = transaction_repository.get_by_trx_id(
        ref_id
    )



    if not trx:

        await callback.answer(
            "Transaksi tidak ditemukan",
            show_alert=True
        )

        return




    if not trx.get("qris_id"):


        await callback.answer(
            "QRIS belum dibuat",
            show_alert=True
        )

        return




    status = xendit.get_qris_status(

        trx["qris_id"]

    )



    if not status:


        await callback.answer(
            "Gagal cek pembayaran",
            show_alert=True
        )

        return





    payment_status = str(

        status.get(
            "status",
            ""
        )

    ).upper()





    print(
        "[QRIS STATUS]",
        payment_status
    )





    if payment_status not in [

        "PAID",
        "COMPLETED",
        "SUCCESS"

    ]:


        await callback.answer(

            "⏳ Pembayaran belum masuk",

            show_alert=True

        )

        return





    # ===============================
    # UPDATE DATABASE
    # ===============================

    transaction_repository.update_status(

        ref_id,

        payment_status="PAID"

    )




    await callback.message.answer(

        """
✅ Pembayaran berhasil diterima.


⏳ Pesanan sedang diproses.


Mohon tunggu...
"""

    )



    await callback.answer()