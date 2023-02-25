import http.server
import threading
import socketserver
import json
import mysql.connector
from insert import insert
from login import consulta_login
from edit import edit
from search import search
from sessions import verify_token
from transaction import insert_or_update_transaction
# Port number to use for the server
PORT = 5000

# Define a custom request handler


def conexion_mysql():
    try:
        global conexion
        conexion = mysql.connector.connect(
            host="172.16.0.6",
            user="root",
            password="*4b0g4d0s4s*",
            database='StaffNet'
        )
        global cursor
        cursor = conexion.cursor()
    except Exception as err:
        print(err)


class Handler(http.server.SimpleHTTPRequestHandler):
    # Override the end_headers method to add a header to allow cross-origin requests
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin',
                         'http://localhost:5173')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    # Handle POST requests
    def do_POST(self):
        conexion_mysql()
        # Get the content length of the request body
        content_length = int(self.headers.get('Content-Length', 0))
        # Read the request body and convert in a JSON object
        body = json.loads(self.rfile.read(content_length))
        # Log the request data
        print("Peticion: ", body)
        # Send a response to the client
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # Manejar la petición
        request = body['request']
        # if request != 'login':
        #     token = body['token']

        if request == 'login':
            response = consulta_login(body, conexion)

        elif request == 'validate_create_admins':
            validate = verify_token(body["token"], "create_admins")
            if validate:
                response = {'status': 'success'}
            else:
                response = {'status': 'False'}
        elif request == 'validate_consult':
            if verify_token(body["token"], "consult"):
                response = {'status': 'success'}
            else:
                response = {'status': 'False'}

        elif request == 'search_user_ad':
            print(len(body))
            username = (body['username'],)
            response = search('permission_consult, permission_create, permission_edit, permission_disable', 'users',
                              'WHERE user = %s', username, cursor, True, body['username'])

        elif request == 'edit':
            table = "users"
            fields = "permission_consult", "permission_create", "permission_edit", "permission_disable"
            condition = "WHERE user = %s"
            parameters = (body["permissions"]["consultar"], body["permissions"]["crear"], body[
                "permissions"]["editar"], body["permissions"]["inhabilitar"], body["user"],)
            response = edit(table, fields,
                            condition, parameters, conexion)

        elif request == 'create':
            parameters = (body["user"], body["permissions"]["consultar"], body["permissions"]["crear"], body[
                "permissions"]["editar"], body["permissions"]["inhabilitar"],)
            columns = ("user", "permission_consult",
                       "permission_create", "permission_edit", "permission_disable")
            response = insert('users', columns, parameters, conexion)

        elif request == "insert_transaction":

            info_tables = {
                "personal_information": {
                    "cedula": body["cedula"], "nombre": body["nombre"], "fecha_nacimiento": body["fecha_nacimiento"],
                    "genero": body["genero"], "edad": body["edad"], "rh": body["rh"],
                    "estado_civil": body["estado_civil"], "hijos": body["hijos"], "personas_a_cargo": body["personas_a_cargo"],
                    "estrato": body["estrato"], "tel_fijo": body["tel_fijo"], "celular": body["celular"],
                    "correo": body["correo"], "direccion": body["direccion"], "barrio": body["barrio"],
                    "contacto_emergencia": body["contacto_emergencia"], "parentesco": body["parentesco"], "tel_contacto": body["tel_contacto"]},
                "educational_information": {
                    "cedula": body["cedula"],
                    "nivel_escolaridad": body["nivel_escolaridad"],
                    "profesion": body["profesion"],
                    "estudios_en_curso": body["estudios_en_curso"]
                },
                "employment_information": {
                    "cedula": body["cedula"], "fecha_afiliacion": body["fecha_afiliacion"], "eps": body["eps"],
                    "pension": body["pension"], "cesantias": body["cesantias"], "cambio_eps_pension_fecha": body["cambio_eps_pension_fecha"],
                    "cuenta_nomina": body["cuenta_nomina"], "fecha_ingreso": body["fecha_ingreso"], "cargo": body["cargo"],
                    "gerencia": body["gerencia"], "campana_general": body["campana_general"], "area_negocio": body["area_negocio"],
                    "tipo_contrato": body["tipo_contrato"], "salario_2023": body["salario_2023"], "subsidio_transporte_2023": body["subsidio_transporte_2023"],
                    "fecha_cambio_campana_periodo_prueba": body["fecha_cambio_campana_periodo_prueba"]
                },
                "performance_evaluation": {
                    "cedula": body["cedula"],
                    "desempeno_1_sem_2016": body["desempeno_1_sem_2016"],
                    "desempeno_2_sem_2016": body["desempeno_2_sem_2016"],
                    "desempeno_2017": body["desempeno_2017"],
                    "desempeno_2018": body["desempeno_2018"],
                    "desempeno_2019": body["desempeno_2019"],
                    "desempeno_2020": body["desempeno_2020"],
                    "desempeno_2021": body["desempeno_2021"]
                },
                "disciplinary_actions": {
                    "cedula": body["cedula"],
                    "llamado_atencion": body["llamado_atencion"],
                    "memorando_1": body["memorando_1"],
                    "memorando_2": body["memorando_2"],
                    "memorando_3": body["memorando_3"]
                },
                "vacation_information": {
                    "cedula": body["cedula"],
                    "licencia_no_remunerada": body["licencia_no_remunerada"],
                    "periodo_tomado_vacaciones": body["periodo_tomado_vacaciones"],
                    "periodos_faltantes_vacaciones": body["periodos_faltantes_vacaciones"],
                    "fecha_salida_vacaciones": body["fecha_salida_vacaciones"],
                    "fecha_ingreso_vacaciones": body["fecha_ingreso_vacaciones"]
                },
                "leave_information": {
                    "cedula": body["cedula"],
                    "fecha_retiro": body["fecha_retiro"],
                    "tipo_de_retiro": body["tipo_de_retiro"],
                    "motivo_de_retiro": body["motivo_de_retiro"],
                    "estado": body["estado"]
                }
            }
            response = insert_or_update_transaction(conexion, info_tables)
        elif request == "update_transaction":
            info_tables = {
                "personal_information": {
                    "cedula": body["cedula"], "nombre": body["nombre"], "fecha_nacimiento": body["fecha_nacimiento"],
                    "genero": body["genero"], "edad": body["edad"], "rh": body["rh"],
                    "estado_civil": body["estado_civil"], "hijos": body["hijos"], "personas_a_cargo": body["personas_a_cargo"],
                    "estrato": body["estrato"], "tel_fijo": body["tel_fijo"], "celular": body["celular"],
                    "correo": body["correo"], "direccion": body["direccion"], "barrio": body["barrio"],
                    "contacto_emergencia": body["contacto_emergencia"], "parentesco": body["parentesco"], "tel_contacto": body["tel_contacto"]},
                "educational_information": {
                    "cedula": body["cedula"],
                    "nivel_escolaridad": body["nivel_escolaridad"],
                    "profesion": body["profesion"],
                    "estudios_en_curso": body["estudios_en_curso"]
                },
                "employment_information": {
                    "cedula": body["cedula"], "fecha_afiliacion": body["fecha_afiliacion"], "eps": body["eps"],
                    "pension": body["pension"], "cesantias": body["cesantias"], "cambio_eps_pension_fecha": body["cambio_eps_pension_fecha"],
                    "cuenta_nomina": body["cuenta_nomina"], "fecha_ingreso": body["fecha_ingreso"], "cargo": body["cargo"],
                    "gerencia": body["gerencia"], "campana_general": body["campana_general"], "area_negocio": body["area_negocio"],
                    "tipo_contrato": body["tipo_contrato"], "salario_2023": body["salario_2023"], "subsidio_transporte_2023": body["subsidio_transporte_2023"],
                    "fecha_cambio_campana_periodo_prueba": body["fecha_cambio_campana_periodo_prueba"]
                },
                "performance_evaluation": {
                    "cedula": body["cedula"],
                    "desempeno_1_sem_2016": body["desempeno_1_sem_2016"],
                    "desempeno_2_sem_2016": body["desempeno_2_sem_2016"],
                    "desempeno_2017": body["desempeno_2017"],
                    "desempeno_2018": body["desempeno_2018"],
                    "desempeno_2019": body["desempeno_2019"],
                    "desempeno_2020": body["desempeno_2020"],
                    "desempeno_2021": body["desempeno_2021"]
                },
                "disciplinary_actions": {
                    "cedula": body["cedula"],
                    "llamado_atencion": body["llamado_atencion"],
                    "memorando_1": body["memorando_1"],
                    "memorando_2": body["memorando_2"],
                    "memorando_3": body["memorando_3"]
                },
                "vacation_information": {
                    "cedula": body["cedula"],
                    "licencia_no_remunerada": body["licencia_no_remunerada"],
                    "periodo_tomado_vacaciones": body["periodo_tomado_vacaciones"],
                    "periodos_faltantes_vacaciones": body["periodos_faltantes_vacaciones"],
                    "fecha_salida_vacaciones": body["fecha_salida_vacaciones"],
                    "fecha_ingreso_vacaciones": body["fecha_ingreso_vacaciones"]
                },
                "leave_information": {
                    "cedula": body["cedula"],
                    "fecha_retiro": body["fecha_retiro"],
                    "tipo_de_retiro": body["tipo_de_retiro"],
                    "motivo_de_retiro": body["motivo_de_retiro"],
                    "estado": body["estado"]
                }
            }
            response = insert_or_update_transaction(
                conexion, info_tables, "cedula")
        elif request == "inhabilitate":
            response = edit("leave_information", "estado",
                            "WHERE cedula = %s", body["cedula"], conexion)
        # Enviar respuesta
        print("Respuesta: ", response)
        self.wfile.write(json.dumps(response).encode())

# Start the server and serve forever


class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


with ThreadedHTTPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
conexion.close()