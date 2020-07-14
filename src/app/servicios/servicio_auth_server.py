from app.servicios.cliente_http_base import ClienteHttpBase

class AuthServerError(Exception):
    def __init__(self, response):
        super().__init__()
        self.status_code = response.status_code
        self.payload = response.json()

class AuthServer(ClienteHttpBase):
    def autenticar(self, token: str):
        '''
        Valida un token de autenticación.
        Devuelve el ID del usuario autenticado o None si el token es
        inválido.
        '''
        response = self._get('/usuario/sesion', headers={'Authorization': f'Bearer {token}'})
        if response.status_code == 200:
            return response.json()['usuario_id']
        if response.status_code == 401:
            return None

        raise AuthServerError(response)

    def iniciar_sesion(self, email: str, clave: str):
        '''
        Crea una nueva sesión para el usuario.

        Devuelve una tupla con el token generado y el ID de usuario del estilo
        (token, ID) en caso de éxito o None si el email o clave es erróneo.
        '''
        response = self._post("/usuario/sesion", json={
            "email": email,
            "password": clave
        })

        if response.status_code == 200:
            data = response.json()
            return data['auth_token'], data['id']
        if response.status_code == 400:
            return None

        raise AuthServerError(response)

    def registrar_usuario(self, email: str, clave: str):
        '''
        Registra un nuevo usuario.

        Devuelve su token de autenticación y el ID de usuario en una tupla
        (token, ID). Si ya hay un e-mail registrado con ese email devuelve None.
        '''
        response = self._post("/usuario", json={
            'email': email,
            'password': clave
        })

        if response.status_code == 201:
            data = response.json()
            return data['auth_token'], data['id']
        if response.status_code == 400:
            return None

        raise AuthServerError(response)

    def obtener_usuario(self, usuario_id: int):
        '''
        Devuelve un diccionario con la información del usuario
        o None si el usuario no existe.
        '''
        response = self._get(f"/usuario/{usuario_id}")
        if response.status_code == 404:
            return None

        if response.status_code != 200:
            raise AuthServerError(response)

        return response.json()

    def obtener_usuarios(self, usuarios_id):
        '''
        Obtiene la información de un conjunto de usuarios.
        usuario_id: Iterable de IDs de usuario.

        Devuelve un diccionario {id: { perfil }}
        '''
        # Asegurarse de que son enteros mediante `map(int, usuarios_id)`
        # Convertirlos a `str` ya que `.join` no lo hace internamente
        ids = ','.join({str(uid) for uid in map(int, usuarios_id)})
        params = {'ids': ids, 'cantidad': len(ids)}

        response = self._get("/usuario", params=params)
        if response.status_code != 200:
            raise AuthServerError(response)

        return {u['id']: u for u in response.json()}

    def actualizar_usuario(self, usuario_id: int, data: dict):
        '''
        Actualiza la información de un usuario.
        data: dict con nombre de campo como clave y como valor el nuevo dato.
        '''
        data_saneada = {}
        for campo in ("nombre", "apellido", "telefono", "direccion", "foto"):
            if campo in data:
                data_saneada[campo] = data.pop(campo)

        if len(data) != 0:
            raise ValueError('Campos desconocido: ' + ','.join(data.keys()))

        response = self._put(f"/usuario/{usuario_id}", json=data_saneada)
        if response.status_code != 200:
            raise AuthServerError(response)

    def limpiar_base_de_datos(self):
        '''
        Borra la base de datos del servidor de autenticación.

        Devuelve True si se borró correctamente, False en caso contrario.
        '''
        response = self._delete("/base_de_datos")
        return response.status_code == 200
