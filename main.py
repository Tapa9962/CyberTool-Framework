import os
from colorama import Fore, Style, init
from modules.scanner.port_scanner import iniciar_escaneo
from modules.sniffer.packet_sniffer import iniciar_sniffer
from modules.exploit.vuln_checker import run_exploit_check


init()


ultimo_objetivo = None

def limpiar():
    os.system('clear')

def menu():
    global ultimo_objetivo  
    
    while True:
        limpiar()
        print(f"{Fore.MAGENTA}============================================")
        print(f"{Fore.WHITE}       MEGATOOL FRAMEWORK v2.0             ")
        print(f"{Fore.MAGENTA}============================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Escáner de Red y Puertos (Avanzado)")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Sniffer de Paquetes (Inteligente)")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Verificador de Vulnerabilidades")
        print(f"{Fore.RED}4.{Style.RESET_ALL} Salir")
        print(f"{Fore.MAGENTA}============================================{Style.RESET_ALL}")
        
        opcion = input(f"{Fore.YELLOW}Selecciona una opción: {Style.RESET_ALL}")

        if opcion == "1":
            target = input(f"\n{Fore.BLUE}[?] Introduce la IP objetivo: {Style.RESET_ALL}")
            
            servicios = iniciar_escaneo(target)
            if servicios:
                ultimo_objetivo = {"ip": target, "servicios": servicios}
            else:
                ultimo_objetivo = None
            input(f"\n{Fore.WHITE}Presiona Enter para volver al menú...")

        elif opcion == "2":
            iniciar_sniffer()
            input(f"\n{Fore.WHITE}Presiona Enter para volver al menú...")

        elif opcion == "3":
            
            if ultimo_objetivo is None:
                print(f"\n{Fore.RED}[!] ERROR: Primero debes realizar un Escaneo (Opción 1).{Style.RESET_ALL}")
                input(f"\n{Fore.WHITE}Presiona Enter para volver al menú...")
                continue

            print(f"\n{Fore.YELLOW}[*] Analizando servicios detectados en {ultimo_objetivo['ip']}...{Style.RESET_ALL}")
            
            encontrado_alguna = False
            
            for servicio in ultimo_objetivo['servicios']:
                run_exploit_check(
                    ultimo_objetivo['ip'], 
                    servicio['port'], 
                    servicio['banner']
                )
                encontrado_alguna = True
            
            if not encontrado_alguna:
                print(f"{Fore.RED}[!] No se encontraron servicios para analizar.{Style.RESET_ALL}")
            
            input(f"\n{Fore.WHITE}Presiona Enter para volver al menú...")

        elif opcion == "4":
            print(f"{Fore.GREEN}[+] Saliendo del sistema...{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}[!] Opción no válida.{Style.RESET_ALL}")
            input(f"\n{Fore.WHITE}Presiona Enter para volver al menú...")

if __name__ == "__main__":
    menu()
