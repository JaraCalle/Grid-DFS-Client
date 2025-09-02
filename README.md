# Grid-DFS-Client

Este es el **cliente CLI (`gridfs`)** para interactuar con el sistema **GridDFS**, compuesto por:
- **NameNode**: administra los metadatos de archivos y asignación de bloques.
- **DataNodes**: almacenan los bloques de archivos físicamente.
- **Cliente (este proyecto)**: interfaz de línea de comandos para subir y (próximamente) descargar/gestionar archivos.

---

## 🚀 Requisitos

- Python 3.9+
- NameNode y al menos un DataNode en ejecución
- Token de autenticación válido generado por el NameNode (`/auth/login`)

---

## 📂 Estructura del cliente

```

client/
├── main.py             # CLI principal
├── core/
│   └── config.py       # Configuración (URL NameNode, token, block size)
├── services/
│   ├── namenode.py     # Comunicación con el NameNode
│   └── datanode.py     # Comunicación con los DataNodes
└── utils/
└── files.py        # Funciones auxiliares (dividir archivos en bloques)

````

---

## ⚙️ Configuración

El cliente usa un archivo `.env` (opcional) o variables de entorno para configurarse.

Ejemplo de `.env`:

```env
NAMENODE_URL=http://127.0.0.1:8000/api/v1/namenode
AUTH_TOKEN=TU_TOKEN_DEL_ADMIN
BLOCK_SIZE=67108864   # 64 MB
````

---

## 📌 Uso básico

Ejecuta el cliente con:

```bash
python client/main.py <comando> [opciones]
```

### Comando `put`

Sube un archivo al sistema GridDFS:

```bash
python client/main.py put ./archivo.txt
```

**Flujo interno:**

1. El cliente obtiene el tamaño del archivo.
2. Envía una solicitud `POST /namenode/allocate` al NameNode para pedir asignación de bloques.
3. El NameNode responde con una lista de bloques (`block_id`) y las direcciones de los DataNodes correspondientes.
4. El cliente divide el archivo en bloques (`BLOCK_SIZE`).
5. Cada bloque se envía vía `PUT /datanode/block/{block_id}` al DataNode asignado.
6. Al finalizar, el archivo queda distribuido entre los DataNodes.

---

## 🔄 Ejemplo completo de flujo

1. Levantar el **NameNode**:

   ```bash
   uvicorn main:app --reload --port 8000
   ```

2. Levantar un **DataNode**:

   ```bash
   uvicorn main:app --reload --port 9001
   ```

3. Registrar el DataNode en el NameNode (manual o automático):

   ```bash
   POST http://127.0.0.1:8000/api/v1/namenode/register_datanode
   {
     "id": "dn1",
     "ip": "127.0.0.1",
     "port": 9001,
     "capacity": 1000
   }
   ```

4. Obtener un token de autenticación en el NameNode:

   ```bash
   POST http://127.0.0.1:8000/api/v1/auth/login
   {
     "username": "admin",
     "password": "admin123"
   }
   ```

5. Configurar el token en el cliente (`.env`).

6. Subir un archivo con el cliente:

   ```bash
   python client/main.py put ./archivo.txt
   ```

7. Verificar que el archivo fue dividido en bloques y guardado en el directorio `data/` de los DataNodes.

---

## 🛠️ Troubleshooting

* **Error 401: Invalid token**
  Verifica que el token en `AUTH_TOKEN` sea válido y esté activo.

* **Error: No DataNodes registered**
  Asegúrate de haber levantado al menos un DataNode y registrado en el NameNode.

* **Bloques no encontrados al descargar**
  Revisa que los DataNodes estén activos y que la carpeta `data/` no haya sido borrada.