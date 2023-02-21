from login import consulta_usuario_ad


def search(campos, tabla, condicion, params, cursor, active_directory, user_ad):
    results = run_query(campos, tabla, condicion, cursor, params)
    response = process_query(results, active_directory, user_ad)
    return response


def run_query(campos, tabla, condicion, cursor, params):
    query = "SELECT {} FROM {} {}".format(
        campos, tabla, condicion)
    print(query % params)
    cursor.execute(query, params)
    return cursor.fetchone()


def process_query(results, active_directory, user_ad):
    if results is not None:
        print("register found")
        response = {'status': 'success', 'info': results}
        print(response)
    else:
        if active_directory:
            status, result, respuesta, _ = consulta_usuario_ad(user_ad, 'name')
            if len(respuesta) >= 4:
                response = {'status': 'success'}
            else:
                print("Registro no encontrado LDAP")
                response = {'status': 'false',
                            'error': 'Usuario de windows no encontrado'}
        else:
            response = {'status': 'false', 'error': 'Registro no encontrado'}
    return response
