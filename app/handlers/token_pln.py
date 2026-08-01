from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from app.states.token_pln_state import TokenPLNState


router = Router()


@router.message(F.text == "Token PLN")
async def token_pln_menu(
    message: types.Message
):

    await message.answer(
        """
⚡ Token PLN

Silakan pilih nominal:

20.000
50.000
100.000
200.000
"""
    )


@router.message(
    F.text.in_([
        "20.000",
        "50.000",
        "100.000",
        "200.000",
        "20000",
        "50000",
        "100000",
        "200000"
    ])
)
async def token_pln_nominal(
    message: types.Message,
    state: FSMContext
):

    await state.update_data(
        nominal=message.text
    )

    await state.set_state(
        TokenPLNState.waiting_meter
    )

    await message.answer(
        f"""
⚡ Token PLN

Nominal dipilih:

Rp {message.text}

Silakan masukkan nomor meter PLN.
"""
    )


@router.message(
    TokenPLNState.waiting_meter
)
async def token_pln_meter(
    message: types.Message,
    state: FSMContext
):

    data = await state.get_data()

    nominal = data.get(
        "nominal"
    )

    nomor_meter = message.text


    await message.answer(
        f"""
✅ Data Token PLN

Nominal:
Rp {nominal}

Nomor Meter:
{nomor_meter}

Sedang diproses...
"""
    )


    await state.clear()