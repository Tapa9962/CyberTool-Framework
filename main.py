from modules.sniffer.packet_sniffer import iniciar_sniffer
from modules.scanner.port_scanner import iniciar_escaneo
from modules.exploit.vuln_checker import run_exploit_check # <--- NUEVO

def menu():
    print("--- CYBERTOOL FRAMEWORK ---")
    print("1. Escáner de puertos")
    print("2. Sniffer de paquetes")
    print("3. Verificador de Vulnerabilidades (Exploit)")
    print("4. Salir")
    
    opcion = input("\nSelecciona una opción: ")

    if opcion == "1":
        target = input("Introduce la IP objetivo: ")
        iniciar_escaneo(target)
        menu()
    elif opcion == "2":
        iniciar_sniffer()
        menu()
    elif opcion == "3":
        target = input("Introduce la IP objetivo: ")
        port = int(input("Introduce el puerto a analizar: "))
        run_exploit_check(target, port)
        menu()
    elif opcion == "4":
        print("Saliendo...")
        exit()
    else:
        print("Opción no válida.")
        menu()

if __name__ == "__main__":
    menu()
