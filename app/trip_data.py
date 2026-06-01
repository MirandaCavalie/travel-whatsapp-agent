"""
Datos del viaje grupal: San Diego + Yosemite, junio 2026.

Fuente de verdad de TODO lo que el agente sabe. Si un dato no esta aqui,
el agente no lo sabra. Los campos marcados "PENDIENTE" todavia no se
recopilaron y conviene completarlos antes de viajar.
"""

TRIP_DATA: dict = {
    "general": {
        "destination": "San Diego, California, USA (con escapada a Yosemite, CA)",
        "start_date": "2026-06-05",
        "end_date": "2026-06-25",
        "currency": "USD",
        "timezone": "America/Los_Angeles (Pacific Time, UTC-7)",
        "weather_note": (
            "June Gloom: nublado por las mananas, despeja en la tarde. "
            "18-24°C (65-75°F). Llevar capas ligeras."
        ),
        "tips": [
            "El barrio Ocean Beach (base del viaje) esta junto a la playa, ambiente relajado.",
            "Uber/Lyft funcionan bien en San Diego. El trolley cubre algunas zonas.",
            "Para Yosemite y Universal Studios Hollywood necesitan auto (rental o propio).",
            "Voltaje 110V, enchufes tipo A/B (USA).",
            "Propina estandar 18-20% en restaurantes.",
        ],
    },

    "travelers": [
        {
            "name": "Miranda Cavalie",
            "phone": "+51950969085",
            "email": "mirandacavalie@gmail.com",
            "role": "Organizadora del viaje",
            "current_residence": "San Francisco, CA",
            "outbound_flight": {
                "summary": "SFO -> SAN (Frontier Airlines)",
                "date": "2026-06-05",  # viernes
                "airline": "Frontier Airlines",
                "flight_number": "F94306",
                "departure": "22:01 SFO",
                "arrival": "23:44 SAN",
                "seat": "19A",
                "confirmation": "NCWZKV",
                "baggage": "Carry-on incluido (Economy Bundle).",
            },
            "return_flight": {
                "summary": "SAN -> SFO (Frontier Airlines)",
                "date": "2026-06-25",  # jueves
                "airline": "Frontier Airlines",
                "departure": "19:35 SAN",
                "arrival": "21:30 SFO",
                "seat": "27A",
                "confirmation": "NCWZKV",
                "baggage": "Carry-on incluido (Economy Bundle).",
            },
        },
        {
            "name": "Fernanda Jara",
            "phone": "+51993345051",
            "email": "fernandajarameza@gmail.com",
            "current_residence": "Lima, Peru",
            "outbound_flight": {
                "summary": "Lima -> San Diego (via Panama, Copa Airlines)",
                "date": "2026-06-07",  # domingo
                "booking_ref": "BLFV4P",
                "ticket": "2302154298412",
                "frequent_flyer": "Copa 119177868CM",
                "layover": "Panama 3h 16m",
                "segments": [
                    {
                        "airline": "Copa Airlines",
                        "flight_number": "CM462",
                        "from": "Lima (LIM)",
                        "to": "Panama (PTY)",
                        "departure": "07:00",
                        "arrival": "10:45",
                    },
                    {
                        "airline": "Copa Airlines",
                        "flight_number": "CM847",
                        "from": "Panama (PTY)",
                        "to": "San Diego (SAN)",
                        "departure": "14:01",
                        "arrival": "18:40",
                    },
                ],
            },
            "return_flight": {
                "summary": "LAX -> Lima (via San Salvador, Avianca). Vuelo de regreso a Peru.",
                "date": "2026-06-24",  # martes (aterriza en Lima 25 jun 03:30)
                "booking_ref": "AKLPU6",
                "ticket": "202 2489374457",
                "departure_terminal": "Terminal B en LAX",
                "fare": "LIGHT - NON REFUNDABLE / CHANGES RESTRICTED",
                "baggage": (
                    "0 maletas facturadas incluidas. Carry-on 1 pieza de 10kg gratis. "
                    "1ra maleta facturada extra: $130 USD."
                ),
                "segments": [
                    {
                        "airline": "Avianca",
                        "flight_number": "AV525",
                        "from": "Los Angeles (LAX)",
                        "to": "San Salvador (SAL)",
                        "departure": "15:05 (24 jun)",
                        "arrival": "21:05 (24 jun)",
                    },
                    {
                        "airline": "Avianca",
                        "flight_number": "AV429",
                        "from": "San Salvador (SAL)",
                        "to": "Lima (LIM)",
                        "departure": "22:15 (24 jun)",
                        "arrival": "03:30 (25 jun)",
                    },
                ],
            },
        },
        {
            "name": "Zarela Meza",
            "phone": "+51989240894",
            "email": "fernandajarameza@gmail.com",  # email de contacto compartido con Fernanda
            "current_residence": "Lima, Peru",
            "outbound_flight": {
                "summary": "Lima -> San Diego (via Panama, Copa Airlines). Mismo vuelo que Fernanda.",
                "date": "2026-06-07",
                "booking_ref": "BLFV4P",
                "ticket": "2302154298413",
                "layover": "Panama 3h 16m",
                "segments": [
                    {
                        "airline": "Copa Airlines",
                        "flight_number": "CM462",
                        "from": "Lima (LIM)",
                        "to": "Panama (PTY)",
                        "departure": "07:00",
                        "arrival": "10:45",
                    },
                    {
                        "airline": "Copa Airlines",
                        "flight_number": "CM847",
                        "from": "Panama (PTY)",
                        "to": "San Diego (SAN)",
                        "departure": "14:01",
                        "arrival": "18:40",
                    },
                ],
            },
            "return_flight": {
                "summary": "LAX -> Lima (via San Salvador, Avianca). Mismo vuelo que Fernanda.",
                "date": "2026-06-24",
                "booking_ref": "AKLPU6",
                "ticket": "202 2489374458",
                "departure_terminal": "Terminal B en LAX",
                "fare": "LIGHT - NON REFUNDABLE / CHANGES RESTRICTED",
                "baggage": (
                    "0 maletas facturadas incluidas. Carry-on 1 pieza de 10kg gratis. "
                    "1ra maleta facturada extra: $130 USD."
                ),
                "segments": [
                    {
                        "airline": "Avianca",
                        "flight_number": "AV525",
                        "from": "Los Angeles (LAX)",
                        "to": "San Salvador (SAL)",
                        "departure": "15:05 (24 jun)",
                        "arrival": "21:05 (24 jun)",
                    },
                    {
                        "airline": "Avianca",
                        "flight_number": "AV429",
                        "from": "San Salvador (SAL)",
                        "to": "Lima (LIM)",
                        "departure": "22:15 (24 jun)",
                        "arrival": "03:30 (25 jun)",
                    },
                ],
            },
        },
        {
            "name": "Ariana",
            "phone": "+16198973324",
            "email": "arianaym1029@gmail.com",
            "current_residence": "San Diego, CA",
            "outbound_flight": None,
            "return_flight": None,
            "notes": (
                "Local en San Diego, no necesita vuelos. "
                "Es quien compro el Annual Pass de parques nacionales (esta a su nombre)."
            ),
        },
    ],

    "accommodations": [
        {
            "label": "Base San Diego",
            "address": "4605 Voltaire Street, San Diego, CA",
            "neighborhood": "Ocean Beach",
            "period": "Aprox 7-18 jun 2026 y 21-24 jun 2026 (al regresar de Yosemite)",
            "notes": (
                "Casa/base donde se queda el grupo durante la parte de San Diego. "
                "A ~10-15 min en auto del aeropuerto SAN."
            ),
            "wifi": "PENDIENTE - agregar SSID y password",
            "host_contact": "PENDIENTE",
        },
        {
            "label": "Hotel Yosemite",
            "name": "Yosemite Southgate Hotel & Suites",
            "stars": 3,
            "address": "40644 Highway 41, Oakhurst, CA 93644",
            "phone": "+1 559 683 3555",
            "booking_confirmation": "Booking.com #6299380000",
            "pin": "9818",
            "check_in": "2026-06-18 desde las 16:00",  # jueves
            "check_out": "2026-06-21 hasta las 12:00",  # domingo
            "guest_name": "Miranda Cavalie",
            "room": "Family Suite (Private Suite) - 4 adultos, 1 habitacion, 3 noches",
            "breakfast_included": True,
            "smoking": False,
            "amenities": [
                "Bano privado", "A/C", "Caja fuerte", "Banera/ducha",
                "Escritorio", "Sala de estar", "TV pantalla plana",
                "Refrigerador", "Telefono", "Canales satelitales",
                "Cafetera", "Plancha", "Microondas", "Calefaccion",
                "Secador de pelo", "Armario", "Reloj despertador",
            ],
            "cancellation": (
                "Gratis hasta 45 dias antes (limite ~2026-05-04). "
                "Dentro de los 45 dias se cobra el total."
            ),
            "discount": "Genius -18% aplicado antes de impuestos.",
            "distance_to_yosemite_south_entrance": "30 min en auto",
        },
        {
            "label": "Motel escapada Universal (LA)",
            "name": "La Casa Motel, Los Angeles - Burbank Airport",
            "address": "8065 San Fernando Road, Sun Valley, CA 91352, United States",
            "phone": "+1 818-962-3269",
            "booking_confirmation": "5502895308",
            "guest_name": "Fernanda Jara",  # reserva a nombre de Fernanda
            "check_in": "2026-06-13 desde las 14:00",  # sabado
            "check_out": "2026-06-14 hasta las 10:00",  # domingo
            "nights": 1,
            "occupants": ["Miranda Cavalie", "Fernanda Jara"],
            "notes": (
                "Hospedaje para la escapada a Universal Studios Hollywood (13-14 jun). "
                "SOLO Miranda y Fernanda; Zarela y Ariana se quedan en San Diego. "
                "A ~2-2.5 h en auto de la base de San Diego (4605 Voltaire St)."
            ),
        },
    ],

    "parks_pass": {
        "name": "America the Beautiful Annual Pass",
        "year": "2026 Digital Resident Annual Pass",
        "order_number": "0844932983",
        "purchased_at": "recreation.gov",
        "purchased_by": "Ariana",
        "email_associated": "arianaym1029@gmail.com",
        "valid_from": "2026-05-11",
        "valid_until": "2027-05-31",
        "cost_usd": 80.00,
        "covers": "Entrada de vehiculo a parques nacionales (Yosemite, Sequoia, etc.)",
        "logistics_note": (
            "Lo tiene Ariana. Si ella no va a Yosemite/Sequoia, coordinar que "
            "entregue el pase antes del road trip."
        ),
    },

    "itinerary": [
        {"date": "2026-06-05", "weekday": "viernes",   "summary": "Miranda vuela SFO -> SAN (llega 23:44)."},
        {"date": "2026-06-06", "weekday": "sabado",    "summary": "San Diego, turismo libre (Miranda ya en SD)."},
        {"date": "2026-06-07", "weekday": "domingo",   "summary": "Fernanda y Zarela llegan a SAN desde Lima via Panama (18:40)."},
        {"date": "2026-06-08", "weekday": "lunes",     "summary": "San Diego, turismo libre."},
        {"date": "2026-06-09", "weekday": "martes",    "summary": "San Diego, turismo libre."},
        {"date": "2026-06-10", "weekday": "miercoles", "summary": "San Diego, turismo libre."},
        {"date": "2026-06-11", "weekday": "jueves",    "summary": "San Diego, turismo libre."},
        {"date": "2026-06-12", "weekday": "viernes",   "summary": "San Diego, turismo libre."},
        {"date": "2026-06-13", "weekday": "sabado",    "summary": "Miranda y Fernanda: drive SD -> LA. Universal Studios Hollywood (dia 1). Noche en La Casa Motel (Burbank). Zarela y Ariana se quedan en San Diego."},
        {"date": "2026-06-14", "weekday": "domingo",   "summary": "Miranda y Fernanda: Universal Studios Hollywood (dia 2). Check-out motel antes de 10:00 y regreso a San Diego. Zarela y Ariana en San Diego."},
        {"date": "2026-06-15", "weekday": "lunes",     "summary": "San Diego, turismo libre."},
        {"date": "2026-06-16", "weekday": "martes",    "summary": "San Diego, turismo libre."},
        {"date": "2026-06-17", "weekday": "miercoles", "summary": "San Diego, preparar road trip a Yosemite."},
        {"date": "2026-06-18", "weekday": "jueves",    "summary": "Road trip SD -> Oakhurst. Posible parada en Sequoia de camino. Check-in hotel desde 16:00."},
        {"date": "2026-06-19", "weekday": "viernes",   "summary": "Yosemite National Park."},
        {"date": "2026-06-20", "weekday": "sabado",    "summary": "Yosemite National Park."},
        {"date": "2026-06-21", "weekday": "domingo",   "summary": "Check-out hotel antes de 12:00. Regreso a San Diego."},
        {"date": "2026-06-22", "weekday": "lunes",     "summary": "San Diego."},
        {"date": "2026-06-23", "weekday": "martes",    "summary": "San Diego, ultimo dia completo para Fernanda y Zarela."},
        {"date": "2026-06-24", "weekday": "miercoles", "summary": "Fernanda y Zarela: drive SD -> LAX por la manana (salir 9-9:30 AM max). Vuelo LAX -> Lima a las 15:05."},
        {"date": "2026-06-25", "weekday": "jueves",    "summary": "Miranda vuela SAN -> SFO (19:35)."},
    ],

    "activities": [
        {
            "name": "Universal Studios Hollywood (Los Angeles)",
            "date_range": "2026-06-13 a 2026-06-14",  # sabado y domingo
            "status": "Confirmado (orden #UH00004JPS5).",
            "order_confirmation": "UH00004JPS5",
            "attendees": ["Miranda Cavalie", "Fernanda Jara"],
            "who_note": (
                "SOLO van Miranda y Fernanda. Zarela y Ariana se quedan en "
                "San Diego esos dias."
            ),
            "drive_from_san_diego": "~2-2.5 h en auto a Burbank/Sun Valley (cada tramo).",
            "lodging_note": (
                "1 noche en La Casa Motel (Burbank Airport) la noche del 13 jun. "
                "Ver 'accommodations'."
            ),
            "logistics": (
                "Escapada DENTRO de la estadia en San Diego (7-18 jun). Suben a LA "
                "el 13, vuelven el 14. La base de San Diego (4605 Voltaire St) se "
                "mantiene; Zarela y Ariana siguen alli."
            ),
        },
        {
            "name": "Yosemite National Park",
            "date_range": "2026-06-18 a 2026-06-21",
            "status": "Confirmado (hotel reservado en Oakhurst).",
            "entry": "Annual Pass cubre la entrada del vehiculo.",
        },
        {
            "name": "Sequoia National Park",
            "date_range": "2026-06-18",
            "status": "POSIBLE parada de un dia camino a Yosemite. No 100% confirmado.",
            "entry": "Annual Pass cubre la entrada.",
            "logistics": "SD -> Sequoia 5-6h. Sequoia -> Oakhurst 2-3h.",
        },
    ],

    "san_diego_attractions": {
        "ocean_beach_walking": ["Ocean Beach Pier", "Sunset Cliffs"],
        "drive_10_to_20_min": [
            "Mission Bay", "Balboa Park", "San Diego Zoo",
            "Old Town", "USS Midway Museum",
        ],
        "drive_20_to_30_min": ["La Jolla", "Coronado Island", "Gaslamp Quarter"],
    },

    "transport": {
        "from_san_to_base": "SAN aeropuerto -> 4605 Voltaire St: 10-15 min en auto. Uber/Lyft directo.",
        "around_san_diego": (
            "Uber/Lyft funcionan bien. El trolley cubre algunas zonas. "
            "Para excursiones (Universal Studios Hollywood, Yosemite) necesitan auto."
        ),
        "drives_key": {
            "san_diego_to_lax": "2-3 h (peor con trafico de LA)",
            "san_diego_to_oakhurst": "6-7 h",
            "san_diego_to_sequoia": "5-6 h",
            "sequoia_to_oakhurst": "2-3 h",
            "oakhurst_to_yosemite_south_entrance": "30 min",
            "san_diego_to_burbank_sun_valley": "2-2.5 h (escapada a Universal Studios Hollywood)",
        },
        "fernanda_zarela_to_lax_24jun": {
            "deadline_salir_sd": "9:00-9:30 AM maximo el 24 jun",
            "reason": (
                "Vuelo internacional sale 15:05 de Terminal B en LAX. Llegar 3h antes "
                "(estar en LAX 12:00-12:30). Drive SD->LAX son 2-3h con riesgo de trafico LA."
            ),
        },
    },

    "emergency": {
        "local_emergency_number": "911",
        "embassy_peru_in_la": "PENDIENTE - confirmar direccion y telefono del Consulado del Peru en Los Angeles",
        "nearby_hospital": "PENDIENTE - investigar hospital cercano a 4605 Voltaire St, San Diego",
        "travel_insurance": {
            "provider": "PENDIENTE",
            "policy_number": "PENDIENTE",
            "phone": "PENDIENTE",
        },
        "trusted_contacts": [
            # PENDIENTE - agregar contactos de emergencia (familia en Lima, etc.)
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
