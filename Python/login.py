from ldap3 import Server, Connection, SAFE_SYNC,  SUBTREE
import bcrypt

# LDAP
server = Server('CYC-SERVICES.COM.CO')


def start_ldap():
    # Conexion a LDAP mediante usuario ADMIN
    conn = Connection(server, user='Staffnet', password='T3cn0l0g142023*',
                      client_strategy=SAFE_SYNC, auto_bind=True)
    return conn, server


def consulta_login(body, conexion):
    cursor = conexion.cursor()
    password = body['password']
    user = body['user']
    query = "SELECT password, permission_consult, permission_create, permission_edit, permission_disable, permission_create_admins FROM users WHERE `user` = %s"
    # La coma de user si es necesaria
    cursor.execute(query, (user,))
    result_query = cursor.fetchone()
    if result_query != None and result_query != []:
        # print(bcrypt.hashpw(bytes("", 'utf-8'), bcrypt.gensalt()))
        password_bd_encode = bytes(result_query[0], 'utf-8')
        if bcrypt.checkpw(bytes(password, 'utf-8'), password_bd_encode):
            print("Logged by MYSQL")
            response = {"disable": result_query[4], "edit": result_query[3], 'status': 'success', "consult": result_query[1], "create": result_query[2],
                        'create_admins': result_query[5]}
        else:
            status, result, response, _ = consulta_usuario_ad(user, 'name')
            if len(response) >= 4:
                # Login
                atributos = response[0]['attributes']
                nombre = atributos['name']
                try:
                    login = Connection(
                        server, user=nombre, password=password, client_strategy='SYNC', auto_bind=True, read_only=True)
                    response = {"disable": result_query[4], "edit": result_query[3], 'status': 'success', "consult": result_query[1], "create": result_query[2],
                                'create_admins': result_query[5]}
                    try:
                        hashed_password = encriptar_password(password)
                        consulta = "UPDATE users SET password = '{}' WHERE user = '{}'".format(
                            hashed_password.decode('utf-8'), user)
                        cursor.execute(consulta)
                        conexion.commit()
                        print("Actualizacion exitosa")
                    except Exception as e:
                        print("Error encriptando: ", e)
                    login.unbind()
                except Exception as e:
                    print("Error en la contrase??a LDAP: ", e)
                    response = {'status': 'failure',
                                'error': 'Contrase??a Incorrecta'}
            else:
                print("usuario no encontrado LDAP")
                response = {'status': 'failure',
                            'error': 'usuario no encontrado'}
    else:
        response = {'status': 'failure',
                    'error': 'usuario no encontrado'}
    cursor.close()
    return response


def consulta_usuario_ad(user, attributes):
    conn, server = start_ldap()
    # Busqueda del usuario
    status, result, response, _ = conn.search(
        'dc=CYC-SERVICES,dc=COM,dc=CO', '(sAMAccountName=%s)' % (user), search_scope=SUBTREE,  attributes=attributes)
    return status, result, response, _


def encriptar_password(password):
    hashed_password = bcrypt.hashpw(
        bytes(password, 'utf-8'), bcrypt.gensalt())
    return hashed_password
