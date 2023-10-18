#Pedroza Velarde Luis Rodrigo
#Práctica 4
import http.server
import socketserver
import requests

# Tu API Key de OpenWeatherMap
API_KEY = "afe6244129ebe84657cbc82062d08959"
# API de GeoNames
geonames_username = "rodri"

# Función para obtener datos meteorológicos
def obtener_datos_meteorologicos(ciudad):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if "main" in data and "weather" in data:
            temperatura = data["main"]["temp"] - 273.15  # Convertir de Kelvin a Celsius
            condiciones_climaticas = data["weather"][0]["description"]
            return f"Temperatura: {temperatura:.2f}°C<br>Condiciones Climáticas: {condiciones_climaticas}"
        else:
            return "Datos meteorológicos no disponibles."
    except Exception as e:
        return f"Error: {str(e)}"

# Funcion que obtiene datos de Geonames
def obtener_geoname(ciudad):
    try:
        url_geonames = f"http://api.geonames.org/searchJSON?name={ciudad}&maxRows=1&username={geonames_username}"
        response_geonames = requests.get(url_geonames)
        data_geonames = response_geonames.json()

        if "geonames" in data_geonames and data_geonames["geonames"]:
            ubicacion = data_geonames["geonames"][0]
            print(f"Ubicación obtenida de GeoNames:\nCiudad: {ubicacion['name']}\nPais: {ubicacion['countryName']}\nPoblación: {ubicacion['population']}")

            url_openweathermap = f"http://api.openweathermap.org/data/2.5/weather?q={ubicacion['name']}&appid={API_KEY}"
            response_openweathermap = requests.get(url_openweathermap)
            data_openweathermap = response_openweathermap.json()

            if "main" in data_openweathermap and "weather" in data_openweathermap:
                temperatura = data_openweathermap["main"]["temp"] - 273.15
                condiciones_climaticas = data_openweathermap["weather"][0]["description"]
                return f"Información obtenida de OpenWeatherMap<br>Temperatura en {ubicacion['name']}: {temperatura:.2f} °C<br>Condiciones Climaticas en {ubicacion['name']}: {condiciones_climaticas}"
            else:
                return "Datos meteorológicos no disponibles en OpenWeatherMap."
        else:
            return "Ubicación no encontrada en GeoNames."
    except Exception as e:
        return f"Error: {str(e)}"

# Clase personalizada para manejar las solicitudes
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/weather/'):
            ciudad = self.path[9:]
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
