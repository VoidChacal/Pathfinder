from audio_player import play
import json
import os

DB_FILE = "/home/athene/network-monitor/devices_db.json"


def load_db():
    if not os.path.exists(DB_FILE):
        return {}

    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def network_status():

    db = load_db()

    total = len(db)

    online = sum(
        1 for d in db.values()
        if d["online"]
    )

    offline = total - online

    unknown = sum(
        1 for d in db.values()
        if d["name"] == "DESCONHECIDO"
        and d["online"]
    )

    if unknown > 0:
        play("Existem_desconhecidos.wav")
    else:
        play("rede_estavel.wav")


    return (
        f"Status da rede. "
        f"{total} dispositivos cadastrados. "
        f"{online} online. "
        f"{offline} offline. "
        f"{unknown} desconhecidos."
    )


def online_devices():

    db = load_db()

    names = []

    for device in db.values():

        if device["online"]:

            names.append(
                device["name"]
            )

    if not names:
        return "Nenhum dispositivo online."

    return (
        "Dispositivos online: "
        + ", ".join(names)
    )


def offline_devices():

    db = load_db()

    names = []

    for device in db.values():

        if not device["online"]:

            names.append(
                device["name"]
            )

    if not names:
        return "Nenhum dispositivo offline."

    return (
        "Dispositivos offline: "
        + ", ".join(names)
    )


def unknown_devices():

    db = load_db()

    unknowns = []

    for device in db.values():

        if (
            device["name"] == "DESCONHECIDO"
            and device["online"]
        ):
            unknowns.append(
                device["ip"]
            )

    if not unknowns:

        play(
            "desconhecido_nenhum.wav"
        )

        return (
            "Não existem dispositivos "
            "desconhecidos online."
        )

    play(
        "desconhecido.wav"
    )

    return (
        f"Existem {len(unknowns)} "
        f"dispositivos desconhecidos online."
    )


def last_unknown():

    db = load_db()

    unknowns = []

    for mac, device in db.items():

        if device["name"] == "DESCONHECIDO":

            unknowns.append(
                (
                    device["last_seen"],
                    device
                )
            )

    if not unknowns:
        return (
            "Nenhum dispositivo "
            "desconhecido encontrado."
        )

    unknowns.sort(reverse=True)

    device = unknowns[0][1]

    return (
        f"Último dispositivo desconhecido. "
        f"IP {device['ip']}."
    )


def try_action(text):

    text = text.lower().strip()

    commands = {

        "status da rede":
        network_status,

        "dispositivos online":
        online_devices,

        "dispositivos offline":
        offline_devices,

        "desconhecidos":
        unknown_devices,

        "último alerta":
        last_unknown,

        "ultimo alerta":
        last_unknown
    }

    if text in commands:

        return commands[text]()

    return None
