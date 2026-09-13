from modules.sniffer.packet_sniffer import iniciar_sniffer

def menu():
    print("--- CYBERTOOL FRAMEWORK ---")
    print("1. Escáner de puertos (Próximamente)")
    print("2. Sniffer de paquetes")
    print("3. Salir")
    
    opcion = input("\nSelecciona una opción: ")

    if opcion == "1":
        print("El módulo de escaneo está en desarrollo...")
    elif opcion == "2":
        # Aquí llamamos al sniffer
        # Si quieres una interfaz específica, podrías pasarle el nombre: iniciar_sniffer("eth0")
        iniciar_sniffer()
    elif opcion == "3":
        print("Saliendo...")
        exit()
    else:
        print("Opción no válida.")
        menu()

if __name__ == "__main__":
    menu()
