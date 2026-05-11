"""
Datos del viaje grupal.

REEMPLAZA TODOS LOS PLACEHOLDERS con la informacion real antes de usar
el agente en serio. El agente lee de aqui, asi que si el dato no esta
escrito abajo, el agente no lo va a saber.
"""

# REEMPLAZA CON TUS DATOS REALES
TRIP_DATA: dict = {
    "general": {
        "destination": "Tokio, Japon",                  # REEMPLAZA
        "start_date": "2026-07-10",                     # REEMPLAZA (YYYY-MM-DD)
        "end_date": "2026-07-20",                       # REEMPLAZA
        "currency": "JPY",                              # REEMPLAZA
        "timezone": "Asia/Tokyo",                       # REEMPLAZA
        "tips": [
            "El metro cierra alrededor de medianoche, planeen los regresos.",
            "Llevar siempre efectivo: muchos lugares pequenos no aceptan tarjeta.",
            "Conseguir tarjeta Suica o Pasmo para transporte.",
        ],
    },

    # REEMPLAZA con los viajeros reales. El telefono se usa para identificar
    # quien escribe al agente, asi que debe coincidir EXACTAMENTE con el
    # numero desde el que envian WhatsApp (formato E.164: +51999...).
    "travelers": [
        {
            "name": "Miranda",
            "phone": "+51999111111",                    # REEMPLAZA
            "outbound_flight": {
                "airline": "LATAM",
                "flight_number": "LA1234",
                "departure": "2026-07-09 23:50 LIM",
                "arrival": "2026-07-10 17:30 HND",
                "confirmation": "ABC123",
            },
            "return_flight": {
                "airline": "LATAM",
                "flight_number": "LA1235",
                "departure": "2026-07-20 22:00 HND",
                "arrival": "2026-07-21 19:30 LIM",
                "confirmation": "ABC123",
            },
        },
        {
            "name": "Amigo 2",
            "phone": "+51999222222",                    # REEMPLAZA
            "outbound_flight": {
                "airline": "LATAM",
                "flight_number": "LA1234",
                "departure": "2026-07-09 23:50 LIM",
                "arrival": "2026-07-10 17:30 HND",
                "confirmation": "DEF456",
            },
            "return_flight": {
                "airline": "LATAM",
                "flight_number": "LA1235",
                "departure": "2026-07-20 22:00 HND",
                "arrival": "2026-07-21 19:30 LIM",
                "confirmation": "DEF456",
            },
        },
    ],

    "accommodation": {
        "type": "Airbnb",                               # hotel | airbnb | hostel
        "name": "Apartamento en Shibuya",               # REEMPLAZA
        "address": "1-2-3 Shibuya, Shibuya-ku, Tokyo",  # REEMPLAZA
        "check_in": "2026-07-10 15:00",                 # REEMPLAZA
        "check_out": "2026-07-20 10:00",                # REEMPLAZA
        "confirmation": "AIRBNB-XYZ789",                # REEMPLAZA
        "host_contact": "+81 90 0000 0000",             # REEMPLAZA
        "notes": "Codigo de entrada se manda 24h antes por la app.",
    },

    "activities": [
        {
            "date": "2026-07-11",
            "time": "10:00",
            "place": "Mercado de Tsukiji",
            "notes": "Desayuno temprano, llegar antes de las 9 para evitar colas.",
        },
        {
            "date": "2026-07-12",
            "time": "14:00",
            "place": "Templo Senso-ji (Asakusa)",
            "notes": "Reserva no requerida.",
        },
        {
            "date": "2026-07-14",
            "time": "09:00",
            "place": "Tour a Monte Fuji",
            "notes": "Reserva confirmada, ID: TOUR-001. Punto de encuentro: Shinjuku Station West Exit.",
        },
        # REEMPLAZA / agrega mas actividades reales
    ],

    "emergency": {
        "local_emergency_number": "110 (policia) / 119 (ambulancia)",
        "embassy": "Embajada de Peru en Tokio: +81 3 3406 4243",  # REEMPLAZA segun nacionalidad
        "travel_insurance": {
            "provider": "Assist Card",                  # REEMPLAZA
            "policy_number": "AC-000000",               # REEMPLAZA
            "phone": "+1 800 000 0000",                 # REEMPLAZA
        },
        "trusted_contacts": [
            {"name": "Mama de Miranda", "phone": "+51999000001"},  # REEMPLAZA
        ],
    },
}


def find_traveler_by_phone(phone: str) -> dict | None:
    """Devuelve el dict del viajero cuyo telefono coincide, o None."""
    normalized = phone.replace("whatsapp:", "").strip()
    for traveler in TRIP_DATA["travelers"]:
        if traveler["phone"] == normalized:
            return traveler
    return None
