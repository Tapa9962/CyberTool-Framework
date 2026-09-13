import socket
import threading
from queue import Queue

# Lista para guardar los puertos que encontremos abiertos
puertos_abiertos = []

def scan_port(target, port):
    """
    Intenta conectar a un puerto específico.
    """
    try:
        # Creamos el socket (AF_INET es IPv4, SOCK_STREAM es TCP)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Timeout corto para que sea rápido (0.5 segundos)
        sock.settimeout(0.5)
        
        # connect_ex devuelve 0 si la conexión fue exitosa
        result = sock.connect_ex((target, port))
        
        if result == 0:
            print(f"[+] Puerto {port} ABIERTO")
            puertos_abiertos.append(port)
        
        sock.close()
    except Exception:
        pass

def threader(target, queue):
    """
    Función que gestiona los hilos (threads).
    """
    while True:
        # Saca un puerto de la cola de tareas
        port = queue.get()
        scan_port(target, port)
        # Avisa que la tarea terminó
        queue.task_done()

def iniciar_escaneo(target):
    """
    Función principal del módulo de escaneo.
    """
    print(f"[*] Iniciando escaneo rápido en: {target}")
    print("[*] Esto puede tardar unos segundos...")
    
    # Limpiar la lista de puertos abiertos de escaneos anteriores
    puertos_abiertos.clear()
    
    # Creamos una cola de tareas para los puertos
    queue = Queue()

    # Definimos qué puertos queremos escanear. 
    # Puedes poner un rango: list(range(1, 1025))
    # O una lista de puertos comunes para que sea ultra rápido:
    puertos_comunes = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 3306, 3389, 8080]
    
    for port in puertos_comunes:
        queue.put(port)

    # Creamos 50 hilos (personas revisando puertas al mismo tiempo)
    for _ in range(50):
        t = threading.Thread(target=threader, args=(target, queue))
        t.daemon = True # Para que se cierren si el programa principal se cierra
        t.start()

    # Esperamos a que la cola se vacíe
    queue.join()

    print("\n" + "="*30)
    if puertos_abiertos:
        print(f"[!] ESCANEO FINALIZADO. Puertos abiertos: {puertos_abiertos}")
    else:
        print("[!] ESCANEO FINALIZADO. No se encontraron puertos abiertos.")
    print("="*30 + "\n")
