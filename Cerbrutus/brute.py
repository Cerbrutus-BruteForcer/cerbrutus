from typing import ValuesView
import Cerbrutus.services as services
import time
import sys
import threading
from colorama import Fore, Style
import Cerbrutus
'''
Add estimated time remaining...
Add output of how long its been running for already every few minutes.
'''


class BruteUtil:
    threads = []
    start = time.time()
    end = time.time()
    MAX_THREADS = 1000

    def __init__(self, ip: str, port: int, service: str, users: list, passwords: list, threads: int = 10):
        # Validate IP
        if not isinstance(ip, str) or '.' not in ip:
            raise ValueError("The Specified host to connect to does not seem to be a valid host.")
        self.ip = ip

        # Validate Port
        try:
            port = int(port)
        except Exception:
            raise ValueError("[-] - The Specified port to connect to does not seem to be a valid port between 1 and 65535.")
        if not isinstance(port, int) or 65535 < port or port < 0:
            raise ValueError("[-] - The Specified port to connect to does not seem to be a valid port between 1 and 65535.")
        self.port = port
        
        # Validate Service
        if not isinstance(service, str) or service.upper() not in services.valid_services:
            raise ValueError("[-] - The Specified service to connect to is not yet in the list of services. Please make a feature request, or write it and make a pull :P.")
        service_info = services.valid_services[service.upper()]
        self.service = service_info["class"]
        reccomended_threads = service_info["reccomendedThreads"]
        self.threads_num = threads
        if threads > reccomended_threads:
            print(f"[!] - Maximum reccomended threads for service {service.upper()} is {reccomended_threads}...\n[!] - Be aware you may need to minimise the number of threads you use for better efficiency")
        if threads > self.MAX_THREADS:
            self.threads_num = self.MAX_THREADS
            print(f"[*] - MAX NUMBER OF THREADS IS {self.MAX_THREADS}")
        print(f"[+] - Running with {self.threads_num} threads...")

        # Validate Users list
        if not isinstance(users, list) or not users:
            raise ValueError("[-] - The users to to attempt was not a list with items in.")
        self.users = users

        # Validate Passwords list
        if not isinstance(passwords, list) or not users:
            raise ValueError("[-] - The users to to attempt was not a list with items in.")
        self.passwords = passwords
        
    def test_connection(self):
        if self.service.connect(self.ip, self.port, "test", "adidfhudgaduydfguiadhg fuioa ngkfcgsiufhkjnfkasdhgfuyadgbuf") is None:
            print(f"[-] - COULD NOT CONNECT TO {self.ip}:{self.port}... EXITTING!")
            self._exit()

    def brute(self):
        self.start = time.time()
        self.creds_found = False
        self.test_connection()

        for user in self.users:
            print(f"[*] - Starting attack against {user}@{self.ip}:{self.port}")
            for pwd in self.passwords: 
                if self.creds_found:
                    self._exit()
                self.passwords[self.passwords.index(pwd)] = pwd = Cerbrutus.Wordlist.clean_word(pwd)
                thread = threading.Thread(target=self._auth, args=(user, pwd))
                self.threads.append(thread)
                while threading.active_count() > self.threads_num + 1:
                    continue
                sys.stdout.write(f"\r[*] - Trying: {self.passwords.index(pwd) + 1}/{len(self.passwords)}")
                thread.start()
        self._exit()

    def _auth(self, user, pwd):
        if self.creds_found:
            return
        # sys.stdout.write(f"\r{user}:{pwd}                     ")
        auth_result = self.service.connect(self.ip, self.port, user, pwd)
        if auth_result:
            self.creds_found = True 
            time.sleep(2)
            print()
            print(f"{Fore.GREEN}\033[1m[+] - VALID CREDENTIALS FOUND:\n\t{user}:{pwd}{Style.RESET_ALL}")
            print(f"[*] - Took {(self.passwords.index(pwd)+1)*(self.users.index(user)+1)} tries")
            self.end = time.time()
            print(f"[*] Total time - {self.end - self.start} seconds.")

    def _thread_collection(self):
        for thread in self.threads:
            try:
                thread.join()
            except RuntimeError:
                pass

    def _exit(self):
        if not self.creds_found:
            print("\n[*] - Approaching final keyspace...")

        self._thread_collection()

        if not self.creds_found:
                print(f"{Fore.RED}\033[1m[-] - Failed to find valid credentials for {self.ip}:{self.port}{Style.RESET_ALL}")
                self.end = time.time()
                print(f"[*] Total time - {self.end - self.start} seconds.")

        sys.exit()
