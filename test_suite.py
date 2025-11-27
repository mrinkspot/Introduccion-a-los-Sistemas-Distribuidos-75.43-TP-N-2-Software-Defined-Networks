# ==========================================
# MAIN EXECUTION WRAPPER
# ==========================================
def main():
    import sys
    import time
    import gc
    # ==========================================
    # COLORES Y ESTILOS
    # ==========================================
    C_RED     = '\033[91m'
    C_GREEN   = '\033[92m'
    C_YELLOW  = '\033[93m'
    C_BLUE    = '\033[94m'
    C_MAGENTA = '\033[95m'
    C_CYAN    = '\033[96m'
    C_BOLD    = '\033[1m'
    C_RESET   = '\033[0m'

    def print_header(text):
        print(f"\n{C_MAGENTA}{C_BOLD}{'='*70}{C_RESET}")
        print(f"{C_MAGENTA}{C_BOLD}  {text}{C_RESET}")
        print(f"{C_MAGENTA}{C_BOLD}{'='*70}{C_RESET}")

    def print_step(text):
        print(f"{C_CYAN}➜ {text}{C_RESET}")

    def print_cmd(host_name, cmd):
        print(f"{C_YELLOW}  {host_name} {cmd}{C_RESET}")

    def print_pass(text):
        print(f"{C_GREEN}{C_BOLD}  ✓ PASS:{C_RESET} {C_GREEN}{text}{C_RESET}")

    def print_fail(text):
        print(f"{C_RED}{C_BOLD}  ✗ FAIL:{C_RESET} {C_RED}{text}{C_RESET}")

    def print_info(text):
        print(f"{C_BLUE}  ℹ {text}{C_RESET}")

    def print_output(output):
        if not output or not output.strip(): return
        print(f"{C_RESET}    {C_CYAN}Output del comando:{C_RESET}")
        for line in output.strip().split('\n'):
            print(f"    {C_RESET}│ {line}{C_RESET}")

    # ==========================================
    # OBTENCION DE OBJETO NET DE MININET
    # ==========================================
    def get_mininet_obj():
        # intenta obtener el objeto net de mininet de forma directa
        # Nota: Al estar dentro de main(), globals() sigue refiriéndose al scope global del módulo/exec
        if 'net' in globals(): return globals()['net']
        
        # En algunos entornos exec, net podría estar en el scope local del caller, 
        # pero no podemos acceder fácilmente al frame anterior sin inspect.
        # Intentamos buscar en __main__
        try:
            import __main__
            if hasattr(__main__, 'net'): return __main__.net
        except: pass

        # intenta buscar el objeto net en memoria
        print(f"{C_YELLOW}⚠️  Variable 'net' no encontrada en globals. Buscando en memoria...{C_RESET}")
        try:
            from mininet.net import Mininet
            for obj in gc.get_objects():
                if isinstance(obj, Mininet):
                    print(f"{C_GREEN}✅ Objeto Mininet recuperado exitosamente.{C_RESET}")
                    return obj
        except Exception as e:
            print(f"{C_RED}Error en búsqueda profunda: {e}{C_RESET}")
        
        return None

    # recupera el objeto net
    net = get_mininet_obj()

    if not net:
        print(f"\n{C_RED}❌ ERROR FATAL: No se pudo encontrar la red Mininet.{C_RESET}")
        return

    # ==========================================
    # TESTS
    # ==========================================
    class FirewallTestSuite:
        def __init__(self, net):
            self.net = net
            try:
                self.h1 = net.get('h1')
                self.h2 = net.get('h2')
                self.h3 = net.get('h3')
                self.h4 = net.get('h4')
            except KeyError as e:
                print(f"{C_RED}❌ Error: No se encuentra el host {e}. Verifica tu topología.{C_RESET}")
                return
            
        def banner(self):
            print(f"\n{C_BLUE}{'='*70}{C_RESET}")
            print(f"{C_BLUE}{C_BOLD}       🛡️  FIREWALL SDN TEST SUITE  🛡️{C_RESET}")
            print(f"{C_BLUE}       Sistemas Distribuidos - FIUBA{C_RESET}")
            print(f"{C_BLUE}{'='*70}{C_RESET}")

        def menu(self):
            print(f"\n{C_BOLD}MENU DE PRUEBAS:{C_RESET}")
            print(f" {C_GREEN}1){C_RESET} Pingall {C_CYAN}(Conectividad General){C_RESET}")
            print(f" {C_GREEN}2){C_RESET} Test Puerto 80 {C_CYAN}(TCP - Debe bloquearse){C_RESET}")
            print(f" {C_GREEN}3){C_RESET} Test Puerto 8000 {C_CYAN}(TCP - Debe permitirse){C_RESET}")
            print(f" {C_GREEN}4){C_RESET} Test UDP h1->h4:5001 {C_CYAN}(Debe bloquearse){C_RESET}")
            print(f" {C_GREEN}5){C_RESET} Test Bloqueo h2<->h3 {C_CYAN}(Bidireccional){C_RESET}")
            print(f" {C_GREEN}6){C_RESET} Test Tráfico Permitido {C_CYAN}(Reglas por defecto){C_RESET}")
            print(f" {C_GREEN}7){C_RESET} {C_BOLD}EJECUTAR TODOS LOS TESTS{C_RESET}")
            print(f" {C_RED}0) Salir{C_RESET}")
            
        def wait_key(self):
            input(f"\n{C_YELLOW}Presione Enter para continuar...{C_RESET}")

        def test_pingall(self):
            print_header("TEST 1: CONECTIVIDAD GENERAL (PingAll)")
            print_step("Ejecutando pingall en la red...")
            print_cmd("mininet", "pingall")
            self.net.pingAll()
            self.wait_key()

        def test_port80(self):
            print_header("TEST 2: BLOQUEO PUERTO 80 (TCP)")
            
            print_step("Iniciando servidor HTTP en h1:80...")
            cmd_srv = 'python3 -m http.server 80 > /dev/null 2>&1 &'
            print_cmd("h1", cmd_srv)
            self.h1.cmd(cmd_srv)
            time.sleep(2)
            
            print_step("Intentando conectar desde h4 (curl)...")
            cmd_client = 'curl -m 5 http://10.0.0.1:80'
            print_cmd("h4", cmd_client)
            res = self.h4.cmd(cmd_client)
            print_output(res)
            
            if not res.strip() or "Connection timed out" in res or "curl: (28)" in res:
                print_pass("Conexión bloqueada correctamente (Timeout)")
            else:
                print_fail(f"Se recibió respuesta (NO DEBERÍA)")
                
            print_step("Limpiando procesos...")
            print_cmd("h1", "killall python3")
            self.h1.cmd('killall python3')
            self.wait_key()

        def test_port8000(self):
            print_header("TEST 3: PUERTO PERMITIDO 8000 (TCP)")
            
            print_step("Iniciando servidor HTTP en h1:8000...")
            cmd_srv = 'python3 -m http.server 8000 > /dev/null 2>&1 &'
            print_cmd("h1", cmd_srv)
            self.h1.cmd(cmd_srv)
            time.sleep(2)
            
            print_step("Intentando conectar desde h4...")
            cmd_client = 'curl -m 5 http://10.0.0.1:8000'
            print_cmd("h4", cmd_client)
            res = self.h4.cmd(cmd_client)
            print_output(res)
            
            if "HTTP/1.0 200" in res or "HTTP/1.1 200" in res or "<html" in res.lower() or "Directory listing" in res:
                print_pass("Conexión exitosa (Contenido recibido)")
            else:
                print_fail(f"No se pudo conectar.")
                
            print_step("Limpiando procesos...")
            print_cmd("h1", "killall python3")
            self.h1.cmd('killall python3')
            self.wait_key()

        def test_udp(self):
            print_header("TEST 4: BLOQUEO UDP ESPECÍFICO")
            
            print_step("Iniciando servidor iperf UDP en h4:5001...")
            cmd_srv = 'iperf -s -u -p 5001 > /dev/null 2>&1 &'
            print_cmd("h4", cmd_srv)
            self.h4.cmd(cmd_srv)
            time.sleep(1)
            
            # h1 -> h4 (Bloqueado)
            print_step("Probando h1 -> h4 (Debe ser BLOQUEADO)...")
            cmd_client1 = 'iperf -c 10.0.0.4 -u -p 5001 -t 5'
            print_cmd("h1", cmd_client1)
            res1 = self.h1.cmd(cmd_client1)
            print_output(res1)
            if "Server Report" not in res1:
                print_pass("h1 bloqueado correctamente")
            else:
                print_fail("h1 logró conectar (NO DEBERÍA)")

            # h2 -> h4 (Permitido)
            print_step("Probando h2 -> h4 (Debe ser PERMITIDO)...")
            cmd_client2 = 'iperf -c 10.0.0.4 -u -p 5001 -t 5'
            print_cmd("h2", cmd_client2)
            res2 = self.h2.cmd(cmd_client2)
            print_output(res2)
            if "Server Report" in res2:
                print_pass("h2 conectó correctamente")
            else:
                print_fail("h2 no pudo conectar")
                
            print_step("Limpiando procesos...")
            print_cmd("h4", "killall iperf")
            self.h4.cmd('killall iperf')
            self.wait_key()

        def test_h2_h3(self):
            print_header("TEST 5: BLOQUEO BIDIRECCIONAL h2 <-> h3")
            
            print_step("Probando Ping h2 -> h3...")
            cmd1 = 'ping -c 4 10.0.0.3'
            print_cmd("h2", cmd1)
            r1 = self.h2.cmd(cmd1)
            print_output(r1)
            if "100% packet loss" in r1:
                print_pass("Tráfico h2->h3 bloqueado")
            else:
                print_fail("Tráfico h2->h3 pasó (NO DEBERÍA)")

            print_step("Probando Ping h3 -> h2...")
            cmd2 = 'ping -c 4 10.0.0.2'
            print_cmd("h3", cmd2)
            r2 = self.h3.cmd(cmd2)
            print_output(r2)
            if "100% packet loss" in r2:
                print_pass("Tráfico h3->h2 bloqueado")
            else:
                print_fail("Tráfico h3->h2 pasó (NO DEBERÍA)")
            self.wait_key()

        def test_permitted(self):
            print_header("TEST 6: TRÁFICO PERMITIDO")
            
            pairs = [
                (self.h1, '10.0.0.4', 'h1 -> h4'), 
                (self.h1, '10.0.0.2', 'h1 -> h2'),
                (self.h3, '10.0.0.4', 'h3 -> h4'),
                (self.h2, '10.0.0.4', 'h2 -> h4')
            ]
            
            passed_count = 0
            for host, ip, label in pairs:
                print_step(f"Probando {label}...")
                cmd = f'ping -c 4 {ip}'
                print_cmd(host.name, cmd)
                res = host.cmd(cmd)
                print_output(res)
                if "0% packet loss" in res:
                    print_pass(f"{label} OK")
                    passed_count += 1
                else:
                    print_fail(f"{label} FALLÓ")
            
            print(f"\n{C_BOLD}Resumen: {passed_count}/{len(pairs)} sub-tests pasaron.{C_RESET}")
            self.wait_key()

        def run_all(self):
            print_header("EJECUTANDO TODOS LOS TESTS")
            self.test_pingall()
            self.test_port80()
            self.test_port8000()
            self.test_udp()
            self.test_h2_h3()
            self.test_permitted()
            print(f"\n{C_GREEN}{C_BOLD}★ TODOS LOS TESTS COMPLETADOS ★{C_RESET}")

        def run(self):
            self.banner()
            while True:
                self.menu()
                try:
                    opt = input(f"{C_YELLOW}Opción: {C_RESET}")
                    if opt == '1': self.test_pingall()
                    elif opt == '2': self.test_port80()
                    elif opt == '3': self.test_port8000()
                    elif opt == '4': self.test_udp()
                    elif opt == '5': self.test_h2_h3()
                    elif opt == '6': self.test_permitted()
                    elif opt == '7': self.run_all()
                    elif opt == '0': 
                        print(f"\n{C_GREEN}Saliendo...{C_RESET}")
                        break
                    else: print(f"{C_RED}Opción inválida{C_RESET}")
                except KeyboardInterrupt:
                    print(f"\n{C_GREEN}Saliendo...{C_RESET}")
                    break
                except Exception as e:
                    print(f"{C_RED}Error inesperado: {e}{C_RESET}")
                    break

    FirewallTestSuite(net).run()

main()