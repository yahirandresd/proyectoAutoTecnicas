def cargar_archivo(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()
