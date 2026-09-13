from scapy.all import sniff, IP, TCP, UDP

def packet_callback(packet):
    """
    Esta función se ejecuta CADA VEZ que el sniffer captura un paquete.
    """
    # Verificamos si el paquete tiene una capa IP (es un paquete de red)
    if IP in packet:
        ip_src = packet[IP].src  # IP de origen
        ip_dst = packet[IP].dst  # IP de destino
        proto = packet[IP].proto # Protocolo (TCP es 6, UDP es 17)

        # Identificar si es TCP o UDP para que sea más legible
        protocol_name = "Otro"
        if TCP in packet:
            protocol_name = "TCP"
        elif UDP in packet:
            protocol_name = "UDP"

        print(f"[+] {protocol_name} | Origen: {ip_src} -> Destino: {ip_dst}")

def iniciar_sniffer(interfaz=None):
    """
    Función principal para iniciar el sniffing.
    """
    print(f"[*] Iniciando sniffer en la interfaz: {interfaz if interfaz else 'Predeterminada'}")
    print("[*] Presiona Ctrl+C para detener el proceso.\n")
    
    try:
        # sniff() es la función mágica de Scapy
        # prn: la función que se llama por cada paquete
        # store: 0 significa que no guarde los paquetes en memoria (para no saturar la RAM)
        sniff(iface=interfaz, prn=packet_callback, store=0)
    except PermissionError:
        print("[!] ERROR: Necesitas permisos de ADMINISTRADOR o ROOT para usar el sniffer.")
    except Exception as e:
        print(f"[!] Ocurrió un error: {e}")
