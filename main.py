import requests
import time
import os
from mcrcon import MCRcon as mcf
import jdk
from multiprocessing import Process
import shlex
import subprocess
from pathlib import Path
from mcstatus import JavaServer

root = os.getcwd()
version_choice = "."


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_color(message, color):
    print(f"{color}{message}{bcolors.ENDC}")


def new_server():
    global version_choice
    version_choice = input("Please enter a server version: ")
    url = f"https://api.papermc.io/v2/projects/paper/versions/{version_choice}"

    while True:
        try:
            response = requests.get(url)

            if response.status_code == 200:
                paper_data = response.json()
                paper_data_builds = paper_data["builds"]
                url = f"https://api.papermc.io/v2/projects/paper/versions/{version_choice}/builds/{paper_data_builds[-1]}"
                response = requests.get(url)
                paper_data = response.json()
                paper_data_filename = paper_data["downloads"]["application"]["name"]
                print(paper_data_filename)
                download = requests.get(
                    f"https://api.papermc.io/v2/projects/paper/versions/{version_choice}/builds/{paper_data_builds[-1]}/downloads/{paper_data_filename}")
                new_server_folder = input("Name the server folder (DO NOT USE A TAKEN NAME!): ")
                os.mkdir(new_server_folder)
                open(f"{new_server_folder}\\{version_choice}.jar", "wb").write(download.content)
                print("Download successful!\nReturning to the main menu...")
                time.sleep(2.5)
                break
            else:
                print("Error downloading file:", response.status_code)
                print("Returning to main menu...")
                time.sleep(2.5)
                break
        except:
            print("Error, make sure you are connected to the internet!\nReturning to main menu...")
            time.sleep(2.5)
            break

    main()


def find_property(search_string):
    with open('server.properties', 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if search_string in line:
                return line_number


def run_in_jdk8():
    global root
    print(root)
    for jdk_dir in os.scandir(f"{root}\\jdk8"):
        if jdk_dir.is_dir():
            print(jdk_dir.path)
    ram_choice = int(input("Give your RAM allocation in GB, specifying only the number of GBs: "))
    cmd = (
        f'{jdk_dir.path}\\bin\\java.exe -Xms{ram_choice}G -Xmx{ram_choice}G -Dcom.mojang.eula.agree=true -jar 1.20.1.jar')
    cmds = [
        Path(jdk_dir.path) / "bin" / "java.exe",
        f"-Xms{ram_choice}G",
        f"-Xmx{ram_choice}G",
        "-Dcom.mojang.eula.agree=true",
        "-jar", "1.20.1.jar"
    ]
    p = subprocess.Popen(cmds, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def run_in_jdk17():
    global root
    print(root)
    for jdk_dir in os.scandir(f"{root}\\jdk17"):
        if jdk_dir.is_dir():
            print(jdk_dir.path)
    ram_choice = int(input("Give your RAM allocation in GB, specifying only the number of GBs: "))
    cmd = (f'{jdk_dir.path}\\bin\\java.exe -Xms{ram_choice}G -Xmx{ram_choice}G -Dcom.mojang.eula.agree=true -jar 1.20.1.jar')
    cmds = [
        Path(jdk_dir.path) / "bin" / "java.exe",
        f"-Xms{ram_choice}G",
        f"-Xmx{ram_choice}G",
        "-Dcom.mojang.eula.agree=true",
        "-jar", "1.20.1.jar"
    ]
    p = subprocess.Popen(cmds, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def manage_servers():
    logo = r''' __  __                                 ____                          ___   __      
/\ \/\ \                               /\  _`\                      /'___\ /\ \__   
\ \ `\\ \      __       ___      ___   \ \ \/\_\   _ __     __     /\ \__/ \ \ ,_\  
 \ \ , ` \   /'__`\   /' _ `\   / __`\  \ \ \/_/_ /\`'__\ /'__`\   \ \ ,__\ \ \ \/  
  \ \ \`\ \ /\ \L\.\_ /\ \/\ \ /\ \L\ \  \ \ \L\ \\ \ \/ /\ \L\.\_  \ \ \_/  \ \ \_ 
   \ \_\ \_\\ \__/.\_\\ \_\ \_\\ \____/   \ \____/ \ \_\ \ \__/.\_\  \ \_\    \ \__\
    \/_/\/_/ \/__/\/_/ \/_/\/_/ \/___/     \/___/   \/_/  \/__/\/_/   \/_/     \/__/'''
    global root
    global version_choice
    print("\033c\033[3J", end='')
    print("\u001b[38;5;106m" + logo + "\u001b[0m")
    print("\u001b[38;5;106m" + "\n      Version Indev 0.1" + "\u001b[0m")
    print("\nSelect a server: ")

    inc = 1
    inc_filler = f"[{inc}]:"
    servers_fetched = []
    for file in os.listdir():
        d = os.path.join(file)
        if os.path.isdir(d):
            if ".idea" in d or "venv" in d or "jdk17" in d or "jdk8" in d:
                continue
            else:
                print(inc_filler, d)
                inc += 1
                servers_fetched.append(d)
    print(servers_fetched)
    manage_server_choice = int(input("[?]: "))
    if manage_server_choice:
        os.chdir(servers_fetched[manage_server_choice - 1])
        server_choice = servers_fetched[manage_server_choice - 1]
        print("\033c\033[3J", end='')
        print("\u001b[38;5;106m" + logo + "\u001b[0m")
        print("\u001b[38;5;106m" + "\n      Version Indev 0.1" + "\u001b[0m")
        print(f'\nSelected server: {server_choice}')
        task_choice = int(input("""What would you like to do?
[1] Start the server
[2] Access server console
[3] Edit server configuration
[?]: """))
        if task_choice == 1:
            print("\033c\033[3J", end='')
            print("\u001b[38;5;106m" + logo + "\u001b[0m")
            print("\u001b[38;5;106m" + "\n      Version Indev 0.1" + "\u001b[0m")
            jdk_choice = int(input("""\nSelect a Java version:
Note that Java 8 is required for 1.12 to 1.17, whereas Java 17 is required for 1.18+
[1] Java 8
[2] Java 17
[?]: """))
            if jdk_choice == 1:
                p = Process(target=run_in_jdk8())
                p.start()
                p.join()
            elif jdk_choice == 2:
                print(os.getcwd())
                p = Process(target=run_in_jdk17())
                p.start()
                p.join()

        elif task_choice == 2:
            while True:
                command = input("> ")
                if command != "exit":
                    with mcf('localhost', 'passw0rd') as server:
                        resp = server.command(command)
                    print(resp)
                else:
                    break

        elif task_choice == 3:
            running = True
            runningModif = True
            while running:
                # Ask question
                modif_question = str(input("[?] Do you want to modify the server properties [y/n]: "))
                if modif_question == "y":
                    print_color("[*] Modifying config.\n", bcolors.WARNING)

                    # All modifications will happen here
                    while runningModif:
                        what_to_edit = str(input("""What would you like to modify?
[1] Edit world seed
[2] Edit server name
[3] Edit max player value
[4] Edit view distance
[5] Server port
[6] Enbale/Disbale online mode
[7] Continue
[?]: """))

                        # Check answer
                        serv_prop = open("server.properties", "r+")
                        lines_prop = serv_prop.readlines()

                        match what_to_edit:
                            case "1":
                                seed = str(input("\n[?] Which seed would you like to set: "))
                                line_number = find_property("level-seed")
                                lines_prop[line_number - 1] = f"level-seed={seed}\n"

                                print_color(f"[*] Seed changed to {seed}.", bcolors.OKGREEN)

                            case "2":
                                name = str(input("\n[?] Which name would you like to set for your server: "))
                                line_number = find_property("motd")
                                lines_prop[line_number - 1] = f"motd={name}\n"

                                print_color(f"[*] Server name changed to {name}.", bcolors.OKGREEN)

                            case "3":
                                players = str(
                                    input("\n[?] How many players do you want to be able to join simultaneously: "))
                                line_number = find_property("max-players")
                                print(line_number)
                                lines_prop[line_number - 1] = f"max-players={players}\n"

                                print_color(f"[*] Player limit changed to {players}.", bcolors.OKGREEN)

                            case "4":
                                view = str(input("\nHow many chunks do you want the server to render? "))
                                line_number = find_property("view-distance")
                                lines_prop[line_number - 1] = "view-distance=" + view + "\n"

                                print_color(f"[*] Render distance changed to {view}.", bcolors.OKGREEN)

                            case "5":
                                port = str(input("\nWhat port do you want the server to run on? "))
                                line_number = find_property("server-port")
                                lines_prop[line_number - 1] = f"server-port={port}\n"

                                print_color(f"[*] Server port changed to {port}.", bcolors.OKGREEN)
                                print_color("Make sure to forward the port in your router! https://portforward.com",
                                            bcolors.WARNING)

                            case "6":
                                online = str(input("\n[?] Do you want to enable online mode [y/n]: "))
                                if online == "y":
                                    online_check = "enabled."
                                    line_number = find_property("online-mode")
                                    lines_prop[line_number - 1] = "online-mode=true\n"

                                if online == "n":
                                    online_check = "disabled."
                                    line_number = find_property("online-mode")
                                    lines_prop[line_number - 1] = "online-mode=false\n"

                                print_color(f"[*] Online mode {online_check}", bcolors.OKGREEN)

                            case "7":
                                print_color("[*] Saving config and exiting...", bcolors.WARNING)

                                # Save file
                                serv_prop.writelines(lines_prop)
                                serv_prop.close()

                                # Quit loops
                                runningModif = False
                                running = False
                            case _:
                                print_color("[x] Enter a valid answer", bcolors.FAIL)

                        line_number = find_property("enable-rcon")
                        lines_prop[line_number - 1] = "enable-rcon=true\n"
                        line_number = find_property("rcon.password")
                        lines_prop[line_number - 1] = "rcon.password=passw0rd\n"

                        serv_prop.close()

                        with open("server.properties", "w") as serv_prop:
                            serv_prop.writelines(lines_prop)


                elif modif_question == "n":
                    print_color("[*] Continuing without modifications.\n", bcolors.WARNING)
                    running = False
                else:
                    print_color("[x] Enter a valid answer", bcolors.FAIL)
    os.chdir(root)
    main()


def main():
    global root
    os.chdir(root)
    print("\033c\033[3J", end='')
    print("\u001b[38;5;106m" + r''' __  __                                 ____                          ___   __      
/\ \/\ \                               /\  _`\                      /'___\ /\ \__   
\ \ `\\ \      __       ___      ___   \ \ \/\_\   _ __     __     /\ \__/ \ \ ,_\  
 \ \ , ` \   /'__`\   /' _ `\   / __`\  \ \ \/_/_ /\`'__\ /'__`\   \ \ ,__\ \ \ \/  
  \ \ \`\ \ /\ \L\.\_ /\ \/\ \ /\ \L\ \  \ \ \L\ \\ \ \/ /\ \L\.\_  \ \ \_/  \ \ \_ 
   \ \_\ \_\\ \__/.\_\\ \_\ \_\\ \____/   \ \____/ \ \_\ \ \__/.\_\  \ \_\    \ \__\
    \/_/\/_/ \/__/\/_/ \/_/\/_/ \/___/     \/___/   \/_/  \/__/\/_/   \/_/     \/__/''' + "\u001b[0m")
    print("\u001b[38;5;106m" + "\n      Version Indev 0.1" + "\u001b[0m")
    time.sleep(0.5)
    print("\nWelcome to NanoCraft v0.1-Indev! Things can be highly unstable, so proceed with caution ;)")

    if os.path.exists(f"{root}\\jdk17") is False:
        print("\nJava 17 not detected! Installing now. Do not stop the program")
        os.mkdir("jdk17")
        jdk.install('17', path=f'{root}\\jdk17')
    if os.path.exists(f"{root}\\jdk8") is False:
        print("\nJava 8 not detected! Installing now. Do not stop the program")
        os.mkdir("jdk8")
        jdk.install('8', path=f'{root}\\jdk8')
    while True:
        try:
            task = int(input("""\nWhat do you want to do?
[0] Exit
[1] Create a new server
[2] Manage existing server(s)
[?]: """))
            break
        except:
            print("Uh oh! Looks like you didn't type a valid number")
            time.sleep(1)
            print("\033c\033[3J", end='')
            print("\u001b[38;5;106m" + r''' __  __                                 ____                          ___   __      
/\ \/\ \                               /\  _`\                      /'___\ /\ \__   
\ \ `\\ \      __       ___      ___   \ \ \/\_\   _ __     __     /\ \__/ \ \ ,_\  
 \ \ , ` \   /'__`\   /' _ `\   / __`\  \ \ \/_/_ /\`'__\ /'__`\   \ \ ,__\ \ \ \/  
  \ \ \`\ \ /\ \L\.\_ /\ \/\ \ /\ \L\ \  \ \ \L\ \\ \ \/ /\ \L\.\_  \ \ \_/  \ \ \_ 
   \ \_\ \_\\ \__/.\_\\ \_\ \_\\ \____/   \ \____/ \ \_\ \ \__/.\_\  \ \_\    \ \__\
    \/_/\/_/ \/__/\/_/ \/_/\/_/ \/___/     \/___/   \/_/  \/__/\/_/   \/_/     \/__/''' + "\u001b[0m")
            print("\u001b[38;5;106m" + "\n      Version Indev 0.1" + "\u001b[0m")
    if task == 1:
        new_server()
    elif task == 2:
        manage_servers()

    print("\033c\033[3J", end='')


if __name__ == '__main__':
    main()
