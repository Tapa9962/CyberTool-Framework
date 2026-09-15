import socket
from colorama import Fore, Style, init

init()

def grab_banner(ip, port):
    """
    Intenta obtener la identidad (banner) del servicio corriendo en un puerto.
    """
    try:
        # Creamos el socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2) # Tiempo de espera para no quedarnos bloqueados
        s.connect((ip, port))

        # --- TÉCNICA DEL "NUDGE" (EL EMPUJÓN) ---
        # Algunos servicios (como HTTP) no responden si no les enviamos algo.
        if port in [80, 8080, 443, 8000]:
            s.send(b"HEAD / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
        elif port == 21: # FTP
            s.send(b"HELP\r\n")
        
        # Intentamos leer la respuesta
        banner = s.recv(1024).decode(errors='ignore').strip()
        s.close()
        
        # Limpiar el banner de saltos de línea para que la tabla se vea bien
        return banner.replace('\n', ' ').replace('\r', ' ')[:40]
    except:
        return "Desconocido (Sin respuesta)"

def iniciar_escaneo(target):
    print(f"\n{Fore.CYAN}[*] --- Escaneo de Puertos con Detección de Versión ---{Style.RESET_ALL}")
    print(f"{Fore.BLUE}[*] Objetivo: {target}{Style.RESET_ALL}")
    
    # Lista de puertos comunes para escanear
    common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 3306, 3389, 8080]
    
    found_services = []

    print(f"{Fore.YELLOW}{'PUERTO':<8} | {'ESTADO':<8} | {'SERVICIO / VERSIÓN':<30}{Style.RESET_ALL}")
    print("-" * 55)

    for port in common_ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.8)
        
        result = s.connect_ex((target, port))
        
        if result == 0:
            # Si el puerto está abierto, ¡activamos la detección de versión!
            print(f"{Fore.WHITE}[*] Analizando puerto {port}...", end="\r")
            banner = grab_banner(target, port)
            
            print(f"{Fore.GREEN}{port:<8} | OPEN     | {banner}{Style.RESET_ALL}")
            found_services.append({'port': port, 'banner': banner})
        
        s.close()

    print(f"\n{Fore.CYAN}--- Escaneo Finalizado ---{Style.RESET_ALL}")
    
    if not found_services:
        print(f"{Fore.RED}[!] No se encontraron puertos abiertos.{Style.RESET_ALL}")
    
    return found_services
