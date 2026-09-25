from django.http import HttpResponse

lista = ["fiorella", "camila", "vanessa", "sofia"]

def listar(request):
    # Generar los ítems de la lista en formato HTML con diseño de Steam
    items_html = "".join([
        f'''
        <li class="steam-item">
            <span class="user-avatar">{nombre[0].upper()}</span>
            <span class="user-name">{nombre.capitalize()}</span>
            <span class="status-badge">En línea</span>
        </li>
        '''
        for nombre in lista
    ])

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}
            body {{
                font-family: "Motiva Sans", Arial, Helvetica, sans-serif;
                background: linear-gradient(135deg, #101822 0%, #1b2838 100%);
                color: #c6d4df;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}
            .steam-panel {{
                background: rgba(23, 29, 37, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 4px;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
                padding: 2rem;
                width: 100%;
                max-width: 420px;
                backdrop-filter: blur(8px);
            }}
            .panel-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                padding-bottom: 0.8rem;
                margin-bottom: 1rem;
            }}
            h2 {{
                color: #ffffff;
                font-size: 1.2rem;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .count {{
                background: #67c1f5;
                color: #101822;
                font-size: 0.8rem;
                font-weight: bold;
                padding: 2px 8px;
                border-radius: 2px;
            }}
            .steam-list {{
                list-style: none;
            }}
            .steam-item {{
                display: flex;
                align-items: center;
                background: rgba(0, 0, 0, 0.2);
                margin-bottom: 8px;
                padding: 10px 12px;
                border-radius: 2px;
                border-left: 3px solid #67c1f5;
                transition: background 0.2s ease, transform 0.1s ease;
            }}
            .steam-item:hover {{
                background: rgba(103, 193, 245, 0.15);
                transform: translateX(3px);
            }}
            .user-avatar {{
                width: 32px;
                height: 32px;
                background: linear-gradient(135deg, #2a475e 0%, #1b2838 100%);
                border: 1px solid #67c1f5;
                color: #ffffff;
                font-weight: bold;
                display: flex;
                justify-content: center;
                align-items: center;
                border-radius: 2px;
                margin-right: 12px;
            }}
            .user-name {{
                color: #e1e8ed;
                font-weight: 600;
                flex-grow: 1;
            }}
            .status-badge {{
                font-size: 0.75rem;
                color: #66c0f4;
            }}
        </style>
    </head>
    <body>
        <div class="steam-panel">
            <div class="panel-header">
                <h2>Lista de Usuarios</h2>
                <span class="count">{len(lista)}</span>
            </div>
            <ul class="steam-list">
                {items_html}
            </ul>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)
def saludar(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }
            body {
                font-family: "Motiva Sans", Arial, Helvetica, sans-serif;
                background: linear-gradient(135deg, #101822 0%, #1b2838 100%);
                color: #c6d4df;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .steam-card {
                background: rgba(23, 29, 37, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 4px;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
                padding: 2.5rem;
                max-width: 480px;
                width: 90%;
                backdrop-filter: blur(8px);
            }
            .badge {
                display: inline-block;
                background: rgba(103, 193, 245, 0.1);
                color: #67c1f5;
                font-size: 0.75rem;
                font-weight: bold;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                padding: 4px 10px;
                border-radius: 2px;
                margin-bottom: 1.2rem;
            }
            h1 {
                color: #ffffff;
                font-size: 2rem;
                font-weight: 700;
                margin-bottom: 0.8rem;
                letter-spacing: -0.5px;
            }
            p {
                color: #8f98a0;
                font-size: 1.05rem;
                line-height: 1.5;
                margin-bottom: 2rem;
            }
            .btn-steam {
                display: block;
                width: 100%;
                text-align: center;
                background: linear-gradient(90deg, #47bfff 0%, #1a9fff 100%);
                color: #ffffff;
                font-weight: bold;
                text-decoration: none;
                padding: 12px 0;
                border-radius: 2px;
                box-shadow: 0 4px 12px rgba(26, 159, 255, 0.3);
                transition: filter 0.2s ease;
            }
            .btn-steam:hover {
                filter: brightness(1.2);
            }
        </style>
    </head>
    <body>
        <div class="steam-card">
            <span class="badge">Nuevo Curso</span>
            <h1>¡Hola!</h1>
            <p>Bienvenidos al Curso de Python con Django</p>
            <a href="#" class="btn-steam">INICIAR CURSO</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)

def saludar_nombre(request, nombre):
    texto = f"Hola {nombre}"
    return HttpResponse(texto)

def factorial(request, numero):
    resultado = 1
    for i in range(1, numero + 1):
        resultado = resultado * i

        return HttpResponse(f"El factorial de {numero} es {resultado}")

from django.shortcuts import render
def inicio_render(request):
    return render(request,'app1/inicio.html')
