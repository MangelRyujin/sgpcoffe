from django.db.models import Sum
from decimal import Decimal
from django.http import HttpResponse
import requests
from pathlib import Path
BASE_DIR_LOGO = Path(__file__).resolve().parent
from apps.cuentas.models import Order

def generar_html_impresion_funtion(order):
    html_content = """
    <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; text-align:center;}
                table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                th, td { border: 1px solid black; padding: 5px; text-align: left; }
                .total { font-weight: bold; background-color: #f0f0f0; }
                .containers { width: 100%; display: flex; justify-content: space-between; align-items: center; }
            </style>
        </head>
        <body>
            <h1>Rueda de la fortuna</h1>
            <h2>Gracias por escogernos</h2>
            <table>
                <tr class="total">
                    <th><h2>Producto</h2></th>
                    <th><h2>Precio</h2></th>
                </tr>
    """

    total_price = order.total_price
    rate = order.rate
    
    items = order.item_set.filter(state="entregado")
    
    for item in items:
        html_content += f"""
        <tr>
            <td><h3>{item.product.name}</h3></td>
            <td><h3>${Decimal(item.total_price):.2f}</h3></td>
        </tr>
        """
    
    html_content += f"""
    <tr class="total">
        <td><h3>Importe CUP:</h3></td>
        <td><h3>${Decimal(total_price):.2f}</h3></td>
    </tr>
    <tr class="total">
        <td><h3>Otras monedas:</h3></td>
        <td><h3>${Decimal(rate):.2f}</h3></td>
    </tr>
    </table>
    </body>
    </html>
    """
    
    """
    Esta lista de operaciones puede ser infinita.
    Puedes definirla así, o invocar a append cuantas
    veces sea necesario
    Lista de operaciones disponibles: https://parzibyte.me/http-esc-pos-desktop-docs/es/
    """
    operaciones = [
        {
            "nombre": "Iniciar",
            "argumentos": [],
        },
        {
        "nombre": "CargarImagenLocalEImprimir",
        "argumentos": [
        f"{BASE_DIR_LOGO}\\logo2.jpg",
        380,
        0,
        True
        ]
        },
        {
        "nombre": "GenerarImagenAPartirDeHtmlEImprimir",
        "argumentos": [
            html_content,
        380,
        380,
        0,
        False
        ]
    }
    ]

    nombre_impresora = "mpt"
    serial = ""
    carga_util = {
        "operaciones": operaciones,
        "nombreImpresora": nombre_impresora,
        "serial": serial,
    }


    respuesta_http = requests.post("http://localhost:8000/imprimir", json=carga_util)
    respuesta = respuesta_http.json()
    if respuesta["ok"]:
        print("Impresión exitosa")
    else:
        print("Error: " + respuesta["message"])
    return HttpResponse(respuesta, status=404)