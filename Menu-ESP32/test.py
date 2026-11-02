import requests

def procurar_temp_cpu(node):

    if isinstance(node, dict):

        if (
            node.get("Type") == "Temperature"
            and node.get("Text") == "Core (Tctl/Tdie)"
        ):
            return node.get("Value")

        for value in node.values():
            resultado = procurar_temp_cpu(value)

            if resultado:
                return resultado

    elif isinstance(node, list):

        for item in node:
            resultado = procurar_temp_cpu(item)

            if resultado:
                return resultado

    return None


data = requests.get(
    "http://localhost:8085/data.json"
).json()

temp = procurar_temp_cpu(data)

print(temp)