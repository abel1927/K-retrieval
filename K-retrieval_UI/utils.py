import os


def temp_load(path:str = 'D:\AMS\Estudios\#3roS1\Redes'):
    files = []
    for ruta, _ , archivos in os.walk(path, topdown=True):
        for elemento in archivos:
            if elemento.endswith((".txt", ".pdf")):
                files.append(elemento)
                archivo = ruta + os.sep + elemento
    return files

def temp_query(query:str, path:str):
    files = temp_load(path)
    result = [f for f in files if len(f)>10]
    return result

