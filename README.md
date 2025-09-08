# GridDFS - Client

El **Cliente** permite interactuar con GridDFS desde la terminal.  
Se conecta al **NameNode vía HTTP** y a los **DataNodes vía gRPC**.

---

## 🚀 Funcionalidades principales
- **Gestión de usuarios**
  - `register <user> <pass>`
  - `login <user> <pass>`
  - `logout`

- **Gestión de archivos**
  - `put <archivo> [--dir /ruta]`
  - `get <archivo> <output> [--dir /ruta]`
  - `rm <archivo> [--dir /ruta]`

- **Gestión de directorios**
  - `mkdir <dirname> [--parent /ruta]`
  - `rmdir <dirname> [--parent /ruta]`
  - `ls [--dir /ruta]`
  - `tree`

---

## 🏗 Arquitectura de la API

- **Con NameNode (HTTP)**
  - Autenticación en `/auth/*`.
  - Operaciones en `/namenode/*` (ls, mkdir, allocate, rm, metadata).

- **Con DataNodes (gRPC)**
  - `UploadBlock` → subir bloques.
  - `DownloadBlock` → descargar bloques.
  - `DeleteBlock` → eliminar bloques.

---

## ⚡️ Ejemplo de `.env`
```env
NAMENODE_URL="http://127.0.0.1:8000/api/v1"
BLOCK_SIZE=67108864 # 64MB
```

---

## ▶️ Ejemplo Ejecución
```bash
python3 main.py register juan 1234
python3 main.py login juan 1234
python3 main.py mkdir docs
python3 main.py put ./test.txt --dir /docs
python3 main.py ls --dir /docs
python3 main.py get test.txt ./output.txt --dir /docs
```
