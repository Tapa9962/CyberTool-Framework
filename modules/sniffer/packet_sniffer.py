from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP, DNS, Raw
from colorama import Fore, Style, init

init()


PROTOCOL_FILTERS = {
    "1": ("TCP", "tcp"),
    "2": ("UDP", "udp"),
    "3": ("ICMP", "icmp"),
    "4": ("ARP", "arp"),
    "5": ("DNS", "port 53"),
    "6": ("HTTP", "port 80"),
    "7": ("HTTPS", "port 443"),
    "8": ("FTP", "port 21"),
    "9": ("SSH", "port 22")
}

def procesar_paquete(pkt):
    
    try:
        proto_name = "OTROS"
        color = Fore.WHITE

        
        if pkt.haslayer(ARP):
            proto_name = "ARP"
            color = Fore.YELLOW
        elif pkt.haslayer(ICMP):
            proto_name = "ICMP"
            color = Fore.CYAN
        elif pkt.haslayer(TCP):
            proto_name = "TCP"
            color = Fore.GREEN
        elif pkt.haslayer(UDP):
            proto_name = "UDP"
            color = Fore.BLUE
        elif pkt.haslayer(DNS):
            proto_name = "DNS"
            color = Fore.MAGENTA

       
        if pkt.haslayer(IP):
            src = pkt[IP].src
            dst = pkt[IP].dst
        elif pkt.haslayer(ARP):
            src = pkt[ARP].hwsrc
            dst = pkt[ARP].psrc
        else:
            src = "N/A"
            dst = "N/A"

        
        payload = ""
        if pkt.haslayer(Raw):
            payload = str(pkt[Raw].load)[:40] 

        
        print(f"{color}[{proto_name:^5}] {src} -> {dst} | Data: {payload}{Style.RESET_ALL}")

    except Exception as e:
        
        pass

def iniciar_sniffer():
    print(f"\n{Fore.CYAN}--- MÓDULO DE SNIFFER PRO ---{Style.RESET_ALL}")
    print(f"{Fore.WHITE}1. Escaneo Completo (Todos los protocolos){Style.RESET_ALL}")
    print(f"{Fore.WHITE}2. Escaneo Filtrado (Seleccionar protocolo){Style.RESET_ALL}")
    print(f"{Fore.WHITE}3. Volver al menú principal{Style.RESET_ALL}")
    
    opcion = input(f"\n{Fore.YELLOW}[?] Selecciona una opción: {Style.RESET_ALL}")

    if opcion == "1":
        print(f"\n{Fore.BLUE}[*] Iniciando captura total... (Ctrl+C para parar){Style.RESET_ALL}")
        try:
            sniff(prn=procesar_paquete, store=0)
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}[!] Captura detenida.{Style.RESET_ALL}")

    elif opcion == "2":
        print(f"\n{Fore.CYAN}--- SELECCIÓN DE PROTOCOLO ---{Style.RESET_ALL}")
        for k, v in PROTOCOL_FILTERS.items():
            print(f"{Fore.WHITE}{k}. {v[0]}{Style.RESET_ALL}")
        
        sel = input(f"\n{Fore.YELLOW}[?] Elige el número del protocolo: {Style.RESET_ALL}")
        
        if sel in PROTOCOL_FILTERS:
            nombre_proto, filtro_bpf = PROTOCOL_FILTERS[sel]
            print(f"\n{Fore.BLUE}[*] Capturando solo {nombre_proto}... (Ctrl+C para parar){Style.RESET_ALL}")
            try:
                
                sniff(filter=filtro_bpf, prn=procesar_paquete, store=0)
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}[!] Captura detenida.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Selección no válida.{Style.RESET_ALL}")

    elif opcion == "3":
        return
    else:
        print(f"{Fore.RED}[!] Opción no válida.{Style.RESET_ALL}")
