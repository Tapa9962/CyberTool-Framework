import socket
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

init()

def grab_banner(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        s.connect((ip, port))
        
        if port in [80, 8080, 443]:
            s.send(b"HEAD / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
        banner = s.recv(1024).decode(errors='ignore').strip()
        s.close()
        return banner.replace('\n', ' ').replace('\r', ' ')[:40]
    except:
        return "Desconocido"

def scan_single_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1) 
        result = s.connect_ex((target, port))
        if result == 0:
            banner = grab_banner(target, port)
            return {'port': port, 'banner': banner}
        s.close()
    except:
        pass
    return None

def iniciar_escaneo(target):
    print(f"\n{Fore.CYAN}--- CONFIGURACIÓN DE ESCANEO ---{Style.RESET_ALL}")
    print(f"{Fore.WHITE}1. Escaneo Rápido (Puertos más comunes - Muy veloz){Style.RESET_ALL}")
    print(f"{Fore.WHITE}2. Escaneo Completo (Todos los 65,535 puertos - Puede tardar){Style.RESET_ALL}")
    print(f"{Fore.WHITE}3. Volver{Style.RESET_ALL}")
    
    modo = input(f"\n{Fore.YELLOW}[?] Selecciona el modo de escaneo: {Style.RESET_ALL}")

    if modo == "3":
        return []

    
    if modo == "1":
        ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 3306, 3389, 8000, 8080]
        print(f"\n{Fore.GREEN}[+] Modo Rápido activado.{Style.RESET_ALL}")
    elif modo == "2":
        ports_to_scan = range(1, 65536) 
        print(f"\n{Fore.RED}[!] MODO MASIVO ACTIVADO. Escaneando 65,535 puertos...{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[!] Opción no válida.{Style.RESET_ALL}")
        return []

    print(f"{Fore.YELLOW}{'PUERTO':<8} | {'ESTADO':<8} | {'SERVICIO / VERSIÓN':<30}{Style.RESET_ALL}")
    print("-" * 55)

    found_services = []

    
    workers = 200 if modo == "2" else 20
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        
        results = list(executor.map(lambda p: scan_single_port(target, p), ports_to_scan))

    
    for res in results:
        if res:
            print(f"{Fore.GREEN}{res['port']:<8} | OPEN     | {res['banner']}{Style.RESET_ALL}")
            found_services.append(res)

    print(f"\n{Fore.CYAN}--- Escaneo Finalizado ---{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Total de puertos abiertos encontrados: {len(found_services)}{Style.RESET_ALL}")
    
    return found_services
