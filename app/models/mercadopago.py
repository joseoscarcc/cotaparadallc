
# SDK de Mercado Pago
import mercadopago
# Agrega credenciales
sdk = mercadopago.SDK("PROD_ACCESS_TOKEN")

# Crea un ítem en la preferencia
preference_data = {
    "items": [
        {
            "title": "Preventa Libro Quiero Viajar Más",
            "quantity": 1,
            "unit_price": 200,
        }
    ]
}

preference_response = sdk.preference().create(preference_data)
preference = preference_response["response"]