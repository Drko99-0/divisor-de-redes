from netaddr import IPNetwork, IPAddress

def get_subnet_mask(hosts):
    n = 0
    while (2 ** n) - 2 < hosts:
        n += 1
    return 32 - n

def calculate_vlsm(network, hosts_required):
    network = IPNetwork(network)
    current_base_address = network.network
    subnets = []

    for hosts in hosts_required:
        subnet_mask = get_subnet_mask(hosts)
        subnet = IPNetwork(f"{current_base_address}/{subnet_mask}")
        subnets.append(subnet)
        current_base_address = IPAddress(subnet.broadcast + 1)

    return subnets

def calculate_vlsm_ipv6(network, subnets_required):
    network = IPNetwork(network)
    current_base_address = network.network
    subnets = []

    for subnet_size in subnets_required:
        subnet_mask = 64  # mask para ipv6
        subnet = IPNetwork(f"{current_base_address}/{subnet_mask}")
        subnets.append(subnet)
        current_base_address = IPAddress(subnet[-1] + 1)

    return subnets

def show_header():
    print("******************************************")
    print("*                                        *")
    print("*              DIVISOR DE REDES          *")
    print("*                                        *")
    print("*              BY Drko                   *")
    print("*                                        *")
    print("******************************************")

def show_menu():
    print("*  1. Dividir red (IPv4)                 *")
    print("*  2. Dividir red (IPv6)                 *")
    print("*  3. Guardar resultados en archivo      *")
    print("*  4. Ver subredes actuales              *")
    print("*  5. Limpiar pantalla                   *")
    print("*  6. Ayuda                              *")
    print("*  7. Salir                              *")
    print("******************************************")

def get_network(ipv6=False):
    while True:
        try:
            if ipv6:
                network = input("Introduce la red inicial (por ejemplo, 2001:db8::/32) o escribe 'regresar' para volver: ")
            else:
                network = input("Introduce la red inicial (por ejemplo, 192.168.10.0/24) o escribe 'regresar' para volver: ")
            if network.lower() == 'regresar':
                return None
            IPNetwork(network) 
            return network
        except Exception as e:
            print(f"Red inválida: {e}. Inténtalo de nuevo.")

def get_num_lans():
    while True:
        try:
            num_lans = input("Introduce el número de subredes (LANs) o escribe 'regresar' para volver: ")
            if num_lans.lower() == 'regresar':
                return None
            num_lans = int(num_lans)
            return num_lans
        except ValueError:
            print("Número de subredes inválido. Inténtalo de nuevo.")

def get_hosts(num_lans):
    hosts_required = []
    for i in range(num_lans):
        while True:
            try:
                hosts = input(f"Introduce el número de hosts para LAN {i + 1} o escribe 'regresar' para volver: ")
                if hosts.lower() == 'regresar':
                    return None
                hosts = int(hosts)
                hosts_required.append(hosts)
                break
            except ValueError:
                print("Número de hosts inválido. Inténtalo de nuevo.")
    return hosts_required

def show_subnets(subnets):
    for i, subnet in enumerate(subnets):
        usable_ips = subnet.size - 2
        print(f"\nLAN {i + 1}:")
        print(f"  Subnet: {subnet}")
        print(f"  Máscara: {subnet.netmask}")
        print(f"  Primer IP válida: {subnet.network + 1}")
        print(f"  Última IP válida: {subnet.broadcast - 1}")
        print(f"  Dirección de Broadcast: {subnet.broadcast}")
        print(f"  IPs utilizables: {usable_ips}")

def show_subnets_ipv6(subnets):
    for i, subnet in enumerate(subnets):
        usable_ips = subnet.size - 2
        print(f"\nLAN {i + 1}:")
        print(f"  Subnet: {subnet}")
        print(f"  Máscara: {subnet.prefixlen}")
        print(f"  Primer IP válida: {subnet.network + 1}")
        print(f"  Última IP válida: {subnet[-1]}")
        print(f"  Dirección de Broadcast: No es necesaria en IPv6")
        print(f"  IPs utilizables: {usable_ips}")

def save_results_to_file(subnets, ipv6=False):
    with open("subnet_results.txt", "w") as f:
        for i, subnet in enumerate(subnets):
            usable_ips = subnet.size - 2
            f.write(f"\nLAN {i + 1}:\n")
            f.write(f"  Subnet: {subnet}\n")
            f.write(f"  Máscara: {subnet.netmask if not ipv6 else subnet.prefixlen}\n")
            f.write(f"  Primer IP válida: {subnet.network + 1}\n")
            f.write(f"  Última IP válida: {subnet[-1]}\n")
            if not ipv6:
                f.write(f"  Dirección de Broadcast: {subnet.broadcast}\n")
            else:
                f.write(f"  Dirección de Broadcast: No es necesaria en IPv6\n")
            f.write(f"  IPs utilizables: {usable_ips}\n")

def view_subnets(subnets, ipv6=False):
    if subnets:
        if ipv6:
            show_subnets_ipv6(subnets)
        else:
            show_subnets(subnets)
    else:
        print("No hay subredes calculadas.")

def show_help():
    print("******************************************")
    print("*                 AYUDA                  *")
    print("******************************************")
    print("1. Dividir red (IPv4)")
    print("   - Esta opción permite dividir una red IPv4 en subredes más pequeñas.")
    print("   - Ejemplo: Introduce la red inicial (por ejemplo, 192.168.10.0/24)")
    print("   - Introduce el número de subredes y los hosts necesarios para cada subred.")
    print()
    print("2. Dividir red (IPv6)")
    print("   - Esta opción permite dividir una red IPv6 en subredes más pequeñas.")
    print("   - Ejemplo: Introduce la red inicial (por ejemplo, 2001:db8::/32)")
    print("   - Introduce el número de subredes y los hosts necesarios para cada subred.")
    print()
    print("3. Guardar resultados en archivo")
    print("   - Guarda los resultados de las subredes calculadas en un archivo.")
    print("   - Asegúrate de haber calculado subredes antes de usar esta opción.")
    print()
    print("4. Ver subredes actuales")
    print("   - Muestra las subredes calculadas en la sesión actual.")
    print()
    print("5. Limpiar pantalla")
    print("   - Limpia la pantalla y muestra el menú principal.")
    print()
    print("6. Ayuda")
    print("   - Muestra esta guía de usuario.")
    print()
    print("7. Salir")
    print("   - Sale del programa.")
    print()
    print("Consejos:")
    print("   - Asegúrate de introducir datos válidos.")
    print("   - Guarda los resultados después de calcular subredes.")
    print("******************************************")
    input("Presiona Enter para volver al menú principal...")

def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    show_header()
    show_menu()

def main():
    subnets = []
    hosts_required = []
    ipv6 = False
    clear_screen()
    while True:
        choice = input("\nElige una opción: ")
        clear_screen()
        if choice == '1':
            try:
                ipv6 = False
                network = get_network()
                if network is None:
                    clear_screen()
                    continue  
                num_lans = get_num_lans()
                if num_lans is None:
                    clear_screen()
                    continue 
                hosts_required = get_hosts(num_lans)
                if hosts_required is None:
                    clear_screen()
                    continue  
                subnets = calculate_vlsm(network, hosts_required)
                clear_screen()
                show_subnets(subnets)
            except Exception as e:
                print(f"Ocurrió un error: {e}")
        elif choice == '2':
            try:
                ipv6 = True
                network = get_network(ipv6=True)
                if network is None:
                    clear_screen()
                    continue 
                num_lans = get_num_lans()
                if num_lans is None:
                    clear_screen()
                    continue 
                subnets_required = get_hosts(num_lans)
                if subnets_required is None:
                    clear_screen()
                    continue  
                subnets = calculate_vlsm_ipv6(network, subnets_required)
                clear_screen()
                show_subnets_ipv6(subnets)
            except Exception as e:
                print(f"Ocurrió un error: {e}")
        elif choice == '3':
            try:
                if subnets:
                    save_results_to_file(subnets, ipv6)
                    clear_screen()
                    print("Resultados guardados en subnet_results.txt")
                else:
                    clear_screen()
                    print("No hay subredes calculadas para guardar.")
            except Exception as e:
                clear_screen()
                print(f"Ocurrió un error al guardar los resultados: {e}")
        elif choice == '4':
            clear_screen()
            view_subnets(subnets, ipv6)
        elif choice == '5':
            clear_screen()
        elif choice == '6':
            clear_screen()
            show_help()
            clear_screen()
        elif choice == '7':
            clear_screen()
            print("Saliendo del programa...")
            break
        else:
            clear_screen()
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()
