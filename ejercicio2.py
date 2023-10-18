import http.server
import socketserver
import requests

# Tu API Key de OpenWeatherMap
API_KEY = "afe6244129ebe84657cbc82062d08959"
#API de GeoNames
geonames_username = "rodri"

#Funcion que obtiene datos de Geonames
def obtener_geoname(ciudad):
    url = f"http://api.geonames.org/searchJSON?name={ciudad}&maxRows=1&username={geonames_username}"
    try:
        response = requests.get(url)
        data2 = response.json()
        if "geonames" in data and data["geonames"]:
            ubicacion = data["geonames"][0]
            print(f"Ubicación obtenida de GeoNames: \nCiudad: {ubicacion['name']}\nPais: {ubicacion['countryName']}\nPoblación: {ubicacion['population']}")
    except Exception as e:
        print(f"Error: {str(e)}")

# Clase personalizada para manejar las solicitudes
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/weather/'):
            ciudad = self.path[9:]
            #resultado = obtener_datos_meteorologicos(ciudad)
            resultado = obtener_geoname(ciudad)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(resultado.encode())
        else:
            super().do_GET()

# Configuración del servidor
with socketserver.TCPServer(("", 9090), MyHandler) as httpd:
    print("Servidor web en el puerto 9090 para Geonames")
    httpd.serve_forever()
