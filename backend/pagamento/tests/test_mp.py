from unittest import TestCase
import mercadopago
import json


class TestMercadoPago(TestCase):
    def setUp(self) -> None:
        self.sdk = mercadopago.SDK(
            ""
        )
        self.id_pagamento = "1321314427"

    def test_create_preference(self):
        preference_data = {
            "items": [{"title": "My Item", "quantity": 1, "unit_price": 75.76}]
        }
        preference_response = self.sdk.preference().create(preference_data)
        preference = preference_response["response"]

        print(json.dumps(preference, indent=4))

    def test_status_payment(self):
        status = self.sdk.payment().get(self.id_pagamento)
        status = status["response"]

        print(json.dumps(status, indent=4))

        tipo_pagamento = status["payment_type_id"]
        status_pagamento = status["status"]
        status_mp = status["status_detail"]

        print(tipo_pagamento, status_pagamento, status_mp)
