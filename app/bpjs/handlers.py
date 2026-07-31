from app.bpjs.bpjs_service import validate_va


def process_bpjs_order(data):

    if not validate_va(data.get("va_number")):
        return {
            "status": "FAILED",
            "message": "Nomor VA BPJS tidak valid"
        }

    return {
        "status": "READY",
        "message": "Data BPJS siap diproses"
    }