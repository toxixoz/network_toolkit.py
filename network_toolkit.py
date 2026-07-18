import socket
import sys
import os
import platform
import time
from datetime import datetime

# =====================================================================
# 🛡️                  ADVANCED NETWORK SECURITY TOOLKIT
# =====================================================================
# Author: Muhin
# Description: Multi-functional network scanning & diagnostic framework.
# Language: Python 3.x
# =====================================================================

def clear_screen():
    """Clears the terminal screen based on the operating system."""
    if platform.system().lower() == "windows":
        os.system("cls")
    else:
        os.system("clear")

def print_header():
    """Displays the main tool interface banner with styling."""
    print("=" * 65)
    print("    ⚡  [ CYBER SHIELD: ADVANCED NETWORK TOOLKIT v2.5 ]  ⚡    ")
    print("=" * 65)
    print(f"  📌 Started At : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  📌 Platform   : {platform.system()} ({platform.release()})")
    print("=" * 65)

def resolve_target(target):
    """Resolves a domain name to an IP address with error handling."""
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        print("\n [✖] ALERT: Invalid Domain or IP Address. Resolution Failed.")
        return None

def ping_host(ip):
    """Pings the target host to verify network accessibility."""
    print(f"\n [🔍] Sending ICMP Echo Request (PING) to: {ip}...")
    
    # Set ping flag based on OS
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = f"ping {param} 1 {ip} > {"nul" if platform.system().lower() == "windows" else "/dev/null"} 2>&1"
    
    response = os.system(command)
    if response == 0:
        print(" [✔] HOST STATUS: ONLINE 🔥")
        return True
    else:
        print(" [✖] HOST STATUS: OFFLINE ❄️ (Or blocking ICMP packets)")
        return False

def grab_banner(ip, port):
    """Attempts to grab the service banner from an open port."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        s.connect((ip, port))
        s.send(b"Hello\r\n")
        banner = s.recv(1024).decode().strip()
        s.close()
        return banner if banner else "Active Service (No banner)"
    except:
        return "Protected / No response"

def advanced_port_scan(ip):
    """Scans predefined industry-standard ports and fetches data."""
    common_ports = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        443: "HTTPS",
        3306: "MySQL",
        8080: "HTTP-Proxy"
    }

    print(f"\n [🚀] Launching Advanced Scan Matrix on target: {ip}...")
    print(" [~] Scanning core network channels...\n")
    print(f" {'PORT':<10}{'SERVICE':<15}{'STATUS':<15}{'METADATA / BANNER'}")
    print("-" * 65)

    open_ports_count = 0
    start_time = time.time()

    for port, service in common_ports.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        
        result = s.connect_ex((ip, port))
        
        if result == 0:
            open_ports_count += 1
            status = "OPEN 🟢"
            banner = grab_banner(ip, port)
            print(f" {port:<10}{service:<15}{status:<15}{banner}")
        else:
            print(f" {port:<10}{service:<15}{'CLOSED 🔴':<15}{'N/A'}")
            
        s.close()

    end_time = time.time()
    total_time = end_time - start_time

    print("-" * 65)
    print(f" [💥] Matrix Scan Complete! Found {open_ports_count} active target(s).")
    print(f" [⏱️] Total Execution Time: {total_time:.2f} seconds.")

def main():
    clear_screen()
    print_header()
    
    user_input = input(" 🎯 Enter Target Domain or IP (e.g., nmap.org): ").strip()
    if not user_input:
        print(" [✖] ERROR: Input string cannot be empty.")
        sys.exit()

    target_ip = resolve_target(user_input)
    if not target_ip:
        sys.exit()

    print(f" [✔] TARGET RESOLVED => IP: {target_ip}")

    while True:
        print("\n [ 🛠️ SYSTEM MODULES ]")
        print(" ━━━" * 5)
        print(" 1️⃣  Run Live Ping Test")
        print(" 2️⃣  Run Advanced Port Scan & Banner Grabbing")
        print(" 3️⃣  Run Full Diagnostic Framework (Ping + Scan)")
        print(" 4️⃣  Exit Security Toolkit")
        print(" ━━━" * 5)
        
        choice = input("\n 📥 Select Module (1-4): ").strip()

        if choice == '1':
            ping_host(target_ip)
        elif choice == '2':
            advanced_port_scan(target_ip)
        elif choice == '3':
            if ping_host(target_ip):
                advanced_port_scan(target_ip)
        elif choice == '4':
            print("\n" + "=" * 65)
            print("    🛡️ [ shutdown ] Toolkit Closed Safely. Secure System. Bye! 🛡️")
            print("=" * 65)
            break
        else:
            print(" [✖] INVALID MODULE! Please choose a valid operation (1-4).")
            
        input("\n 📂 Press Enter to return to main dashboard...")
        clear_screen()
        print_header()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n [✖] TERMINATED: Process interrupted by user input. Exiting...")
        sys.exit()
