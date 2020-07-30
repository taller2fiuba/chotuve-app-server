[![Build Status](https://travis-ci.com/taller2fiuba/chotuve-app-server.svg?branch=master)](https://travis-ci.com/taller2fiuba/chotuve-app-server)
[![Coverage Status](https://coveralls.io/repos/github/taller2fiuba/chotuve-app-server/badge.svg?branch=master)](https://coveralls.io/github/taller2fiuba/chotuve-app-server?branch=master)

# Chotuve App Server

## Configuración
Toda la configuración del servidor de aplicación de Chotuve se realiza a través de variables de entorno. Aquellas variables definidas como "requeridas" deben tener un valor definido para poder iniciar el servidor y generarán un error en caso contrario.

### Básica
Las siguientes configuraciones son necesarias para la funcionalidad básica del servidor de aplicación de Chotuve.
- `DATABASE_URL`: Requerido. URL de la base de datos, en formato `esquema://usuario:clave@host:puerto/nombre_db`. Los esquemas soportados por las imágenes de Docker son `sqlite` y `postgres`. Sólo se garantiza el correcto funcionamiento con bases de datos PostgreSQL. Ejemplo: `postgres://chotuve:s3cr3t0@localhost:5432/chotuve_app`.
- `CHOTUVE_MEDIA_URL`: URL del servidor de medios de Chotuve. Valor por defecto: `http://localhost:27080`.
- `CHOTUVE_AUTH_URL`: URL del servidor de autenticación de Chotuve. Valor por defecto: `http://localhost:26080`.
- `PORT`: Sólo productivo. Requerido. Puerto en el cual se aceptarán conexiones.

### Seguridad

Las siguientes configuraciones permiten mejorar la seguridad de toda la red de Chotuve autenticando cada solicitud realizada entre servidores.

- `APP_SERVER_TOKEN`: Opcional. Token de autenticación para la red Chotuve. En caso de configurarse debe tomar como valor un token de servidor de aplicación generado desde el administrador web.

### Firebase

Para utilizar las funcionalidades de chat entre usuarios y notificaciones push se debe utilizar un servicio externo provisto por Firebase. 

Las siguientes variables permiten establecer la configuración del servicio externo a utilizar. Todas las variables de ambiente de esta sección son opcionales. En caso de no configurarse se desactivará la funcionalidad de chat y notificaciones push.

- `FIREBASE_CREDENCIALES`: Credenciales de aplicación de Firebase. Estas credenciales se obtienen desde la consola de Firebase que generará un archivo en formato `JSON`. Se debe codificar el contenido de este archivo en `base64` y el resultado codificado configurarlo en esta variable de ambiente. Por ejemplo, para configurarlo en un sistema Unix se podría utilizar el siguiente comando: `export FIREBASE_CREDENCIALES=$(base64 archivo.json)`.

#### Chats

- `FIREBASE_CHAT_DB_URL`: URL de la base de datos de tiempo real de Firebase utilizada para almacenar la información de los chats. Valor por defecto: `https://chotuve-a8587.firebaseio.com/`.
- `FIREBASE_CHAT_DB_RAIZ`: Nodo raíz de la base de datos a utilizar. Este parámetro permite tener más de una instancia de chat en la misma base de datos, por ejemplo, una para producción y otra para *staging* o *testing*. Valor por defecto: `app-server-dev`.
- `FIREBASE_CHAT_DB_RECURSO_CHATS`: Nombre del nodo debajo del cual se almacenará la metadata de chats. Valor por defecto: `chats`.
- `FIREBASE_CHAT_DB_RECURSO_MENSAJES`: Nombre del nodo debajo del cual se almacenará el contenido de los chats. Valor por defecto: `mensajes`.

#### Notificaciones push

- `FIREBASE_NOTIFICADOR_DB_URL`: URL de la base de datos de tiempo real de Firebase utilizada para almacenar la información de los chats. Puede utilizarse la misma base que se utiliza para los chats. Valor por defecto: `https://chotuve-a8587.firebaseio.com/`.
- `FIREBASE_NOTIFICADOR_DB_RAIZ`: Nodo raíz de la base de datos a utilizar. Ver detalle en `FIREBASE_CHAT_DB_RAIZ`. Puede utilizarse el mismo nodo raíz que se utilizó para chats. Valor por defecto: `app-server-dev`.
- `FIREBASE_NOTIFICADOR_DB_RECURSO`: Nombre del nodo debajo del cual se almacenarán los metadatos necesarios para las notificaciones. Valor por defecto: `notificaciones`.

### Misceláneas
- `FLASK_ENV`: Opcional. Entorno de Flask a utilizar. Valor por defecto: `development`. Debe configurarse manualmente a `production` en un entorno productivo.

## Despliegue productivo

Para el despliegue productivo de la aplicación se provee un archivo `Dockerfile`. El mismo permitirá construir una imagen productiva de Docker del servidor de aplicación de Chotuve.

### Dependencias

Para el entorno productivo la única dependencia requerida es Docker. 

En caso de querer realizar una instalación sin Docker, se requieren las siguientes bibliotecas:
- Python 3.8.3
- Flask
- Jinja2
- Werkzeug
- requests 
- flask-cors
- flask-restful
- flask-sqlalchemy
- flask-migrate
- psycopg2
- firebase-admin
- business-rules

### Ejemplo de despliegue productivo

En el siguiente ejemplo se lanzará una versión productiva de Chotuve App Server con la siguiente configuración:
- Base de datos SQLite en el archivo `/tmp/app.db`
- Chotuve Media Server en `http://localhost:27080`
- Chotuve Auth Server en `http://localhost:26080`
- Aceptará conexiones en el puerto 5000.

```bash
~/chotuve-app-server$ docker build -t chotuve-app-server:latest .
...
Successfully tagged chotuve-app-server:latest
~/chotuve-app-server$ docker run \
    -e FLASK_ENV=production \
    -e DATABASE_URL="sqlite:////tmp/app.db" \
    -e PORT=5000 \
    --network="host" \
    -d \
    chotuve-app-server:latest
b51f513fc78cc222b32226d617b689a3960e4eb5b8f6d021dd6714163c14fb8b
~/chotuve-app-server$
```

> **IMPORTANTE**: No olvidar configurar la variable de ambiente `FLASK_ENV` en `production` para hacer el despliegue productivo.

Ahora el servidor de aplicación estará corriendo.

> El servidor de aplicación no funcionará si no puede acceder a los servidores de medios y de autenticación en las URLs indicadas.

## Desarrollo

Todo el proyecto está dockerizado de modo de poder desarrollar sin tener que instalar ninguna dependencia adicional más que Docker y Docker Compose.

Para esto se provee un conjunto de scripts para levantar el servidor de desarrollo y simplificar algunas tareas comunes:
- `bin/dev-compose`: Wrapper para `docker-compose`. El servidor de desarrollo utiliza un archivo `docker-compose.yml` que está ubicado en `bin/chotuve_app/docker-compose.yml`. Para evitar tener que indicar explícitamente la ruta a `docker-compose` en cada invocación se provee este script. Ejecutar `bin/dev-compose` es equivalente a ejecutar `docker-compose -f bin/chotuve_app/docker-compose.yml`.
- `bin/exec-dev`: Permite ejecutar un comando dentro del contenedor de desarrollo del servidor de aplicación. Útil para cuando es necesario abrir un intérprete de Python o ejecutar un script de Flask dentro del contenedor. Requiere que el contenedor de desarrollo esté iniciado.
- `bin/run-unit-tests`: Corre el *linter* y las pruebas unitarias del proyecto dentro del contenedor de desarrollo. Requiere que el contenedor de desarrollo esté iniciado.

### Iniciar el servidor de desarrollo
El servidor de desarrollo tendrá acceso al código fuente del proyecto mediante un montaje de tipo *bind*, lo cual implica que cualquier cambio que se realice sobre el código impactará directamente sobre el servidor.

```bash
~/chotuve-app-server$ bin/dev-compose up
```

Para iniciar el servidor en segundo plano o pasarle opciones extras a `docker-compose`, se pueden agregar al final de la línea de comandos, por ejemplo:

```bash
~/chotuve-app-server$ bin/dev-compose up -d
```

### Para detener el servidor de desarrollo

Si estaba corriendo interactivamente (en una terminal) `Ctrl-C`, si estaba corriendo
en segundo plano:

```bash
~/chotuve-app-server$ bin/dev-compose down
```

> Para detener el servidor y además borrar su base de datos, se puede ejecutar `dev-compose down -v`.

### Para correr las pruebas unitarias

```bash
~/chotuve-app-server$ bin/run-unit-tests
```

Puede ser necesario, eventualmente, correr alguna prueba específica o correr las pruebas sin correr el *linter*. Para esto se puede abrir un `bash` dentro del contenedor y ejecutar los comandos manualmente. Por ejemplo:

```bash
~/chotuve-app-server$ bin/exec-dev bash
root@chotuve:/var/www/app# cd src
root@chotuve:/var/www/app/src# nose2 tests.test_chat
....
----------------------------------------------------------------------
Ran 4 tests in 0.294s

OK
root@chotuve:/var/www/app/src#
```

### Para correr un comando de Flask

Para correr un comando de Flask, se debe ingresar al contenedor y ejecutar el comando dentro del mismo. Cualquier archivo creado se verá reflejado fuera del contenedor.

Por ejemplo, para correr `flask db migrate`:

```bash
~/chotuve-app-server$ bin/exec-dev bash
root@chotuve:/var/www/app# cd src
root@chotuve:/var/www/app/src# flask db migrate
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
root@chotuve:/var/www/app/src#
```

> **NOTA**: Hay una consideración a tener en cuenta cuando algún comando crea archivos dentro del contenedor. Debido a cómo está hecha la imagen `python:3.8.3`, el usuario con el que se corren los comandos es `root`, con lo cual los archivos creados tendrán usuario y grupo `root`. La solución es simplemente cambiarles el usuario y grupo luego de crearlos.

### Para abrir un intérprete de Python dentro del contenedor de desarrollo

```bash
~/chotuve-app-server$ bin/exec-dev bash
root@chotuve:/var/www/app# cd src
root@chotuve:/var/www/app/src# python
Python 3.8.3 (default, Jun  9 2020, 17:39:39) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

## Base de datos

Se utiliza el ORM SQLAlchemy y Alembic para las migraciones. Para el proyecto se utilizan los *wrappers* `flask-sqlalchemy` y `flask-migrate` que lo que hacen es exportar las funcionalidades de los paquetes a través del CLI de Flask.

El servidor de aplicación fue diseñado considerando que el motor de la base de datos es PostgreSQL 12. En principio podría funcionar con otros motores pero no hay ninguna garantía de que funcione correctamente en esos casos.

### Migraciones
Cada vez que se realiza un cambio estructural en la base de datos se debe generar la correspondiente migración. Para esto, una vez modificado el modelo en código, se debe ejecutar el siguiente comando:

```bash
~/chotuve-app-server$ bin/exec-dev bash
root@chotuve:/var/www/app# cd src
root@chotuve:/var/www/app/src# flask db migrate
...
Generating migration [...]
root@chotuve:/var/www/app/src#
```

Este comando va a generar un nuevo archivo `.py` en `src/migrations/versions` que deberá ser versionado y contendrá los cambios incrementales realizados sobre la estructura de la base.

> **NOTA**: Se debe tener especial cuidado al cambiar de branch o mergear branches con el orden en que se generaron las migraciones y el estado actual de la base de datos. Ver el apartado "Conflictos con migraciones".

Una vez que las migraciones fueron creadas correctamente, deben ser aplicadas a la base de datos de la siguiente forma:

```bash
~/chotuve-app-server$ bin/exec-dev bash
root@chotuve:/var/www/app# cd src
root@chotuve:/var/www/app/src# flask db upgrade
...
root@chotuve:/var/www/app/src#
```

#### Conflictos con migraciones
Podría suceder que haya cambios simultáneos en dos ramas a la estructura de la base de datos. Lamentablemente, resolver estos conflictos no es una tarea tan simple como hacer `git merge`.

Alembic maneja las migraciones como si fueran una especie de lista enlazada. Cada migración (o revisión) "sabe" cuál es la versión siguiente y la versión anterior de la base de modo de poder actualizar o desactualizar la base de una versión a la otra.

En el caso en que haya conflictos de migraciones lo que termina sucediendo es que la lista diverge. Por ejemplo:
```
           v3 <[branch 1]
          /
 v1 -> v2 
          \
           v4 <[branch 2]
```

En el caso en que se genere un conflicto de este estilo, la forma de proceder es la siguiente:
- Desactualizar la base de datos hasta una versión que sea común entre los dos branches. En el caso de la figura sería desactualizar a la revisión `v2`.
- Borrar las migraciones posteriores a la revisión `v2` de la carpeta `src/migrations/versions`.
- Con la base en esa revisión, realizar el *merge* de los archivos `.py` de los modelos (y del resto del código si fuera necesario).
- Generar las nuevas migraciones (`flask db migrate`).
- Actualizar la base a la última versión (`flask db upgrade`).
- Versionar los cambios en migraciones.

## Pruebas de aceptación

Este proyecto cuenta con pruebas de aceptación utilizando `behave`. Para correr las pruebas ver su documentación en [el repositorio de pruebas](https://github.com/taller2fiuba/chotuve-integration-tests).

Para simplificar las pruebas de aceptación se provee un archivo `docker-compose.yml` en la raíz del repositorio que permite levantar una imagen semi-productiva del proyecto y una base de datos PostgreSQL para el mismo.

Este archivo se puede utilizar también para levantar una versión productiva del servidor y la base de datos en una misma máquina, haciéndole algunos cambios a las variables de entorno.

Para que este archivo `docker-compose.yml` pueda funcionar correctamente se asume la existencia de una red de Docker denominada `chotuve` que permite conectar todos los servidores entre sí. 

En caso de que esta red no exista se puede crear con el siguiente comando:

```bash
$ docker network create -d bridge chotuve
```

No es necesario crear la red de Docker para correr las pruebas de aceptación, el script que corre las pruebas se encargará de crearla si no existiera.

## Integración continua

Se utiliza Travis CI como servidor de integración continua y despliegue automático a Heroku, bajo la siguiente configuración:
- En todas las ramas se corren las pruebas unitarias en cada commit.
- En los PR se corren las pruebas unitarias y además las pruebas de aceptación. Es necesario que el PR tenga una aprobación y que pase las pruebas **unitarias** para poder mergearlo a `master`.
- En `master` se corren las pruebas unitarias y de aceptación, y en caso de que todas las pruebas pasen se hace un deploy automático a Heroku.
