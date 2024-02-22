from unittest import TestCase
import mercadopago
import json

from backend.pagamento.models import Pagamento
from backend.loja.models import Pedido


class TestMercadoPago(TestCase):
    def setUp(self) -> None:
        self.sdk = mercadopago.SDK(
            ""
        )
        self.pedido = Pedido.objects.get(pk="1b67eed0-2471-4bb3-9cf3-b6fac9a7889c")
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

    def test_save_payment(self):
        status = self.sdk.payment().get(self.id_pagamento)
        status = status["response"]

        tipo_pagamento = status["payment_type_id"]
        status_pagamento = status["status"]
        status_mp = status["status_detail"]
        Pagamento(
            pedido=self.pedido,
            status=status_pagamento,
            status_mp=status_mp,
            tipo_pagamento=tipo_pagamento      
        ).save()
        self.pedido.status_pagamento=status_pagamento
        self.pedido.cod_pagamento=self.id_pagamento
        self.pedido.save()

        print(tipo_pagamento, status_pagamento, status_mp)