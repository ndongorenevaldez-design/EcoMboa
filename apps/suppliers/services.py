import uuid
from io import BytesIO

import qrcode
from django.core.files.base import ContentFile


def simulate_mobile_money_payment(operator: str, amount) -> tuple[str, str]:
    # Deterministic simulation for dev workflows.
    reference = f"SIM-{operator.upper()}-{uuid.uuid4().hex[:10].upper()}"
    return "paid", reference


def generate_transaction_qr(transaction) -> None:
    code = transaction.lot_qr_code or f"LOT-{uuid.uuid4().hex[:12].upper()}"
    transaction.lot_qr_code = code

    qr_payload = (
        f"transaction_id={transaction.pk};"
        f"lot={code};"
        f"supplier={transaction.supplier_id};"
        f"material={transaction.material_type};"
        f"weight={transaction.weight_kg};"
        f"amount={transaction.total_amount}"
    )
    img = qrcode.make(qr_payload)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    filename = f"{code}.png"
    transaction.qr_code_image.save(filename, ContentFile(buffer.getvalue()), save=False)

