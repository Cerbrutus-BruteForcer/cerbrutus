#!/usr/bin/env python3
import argparse
import sys
import Cerbrutus

banner = """
\t================================================================
\t    __    ___  ____   ____   ____  __ __  ______  __ __  _____
\t   /  ]  /  _]|    \ |    \ |    \|  |  ||      ||  |  |/ ___/
\t  /  /  /  [_ |  D  )|  o  )|  D  )  |  ||      ||  |  (   \_ 
\t /  /  |    _]|    / |     ||    /|  |  ||_|  |_||  |  |\__  |
\t/   \_ |   [_ |    \ |  O  ||    \|  :  |  |  |  |  :  |/  \ |
\t\     ||     ||  .  \|     ||  .  \     |  |  |  |     |\    |
\t \____||_____||__|\_||_____||__|\_|\__,_|  |__|   \__,_| \___|
\t                                                              
\tNetwork Brute Force Tool
\thttps://github.com/Cerbrutus-BruteForcer/cerbrutus
\t================================================================
"""


def main():
    arg_parser = argparse.ArgumentParser(description="Python based network brute forcing tool!")
    arg_parser.add_argument("Host", help=f"The host to connect to - in IP or VHOST/Domain Name form")
    arg_parser.add_argument("Service", help=f"The service to brute force (currently implemented 'SSH')")
    arg_parser.add_argument("-U", "--users", help=f"Either a single user, or the path to the file of users you wish to use", required=True)
    arg_parser.add_argument("-P", "--passwords", help=f"Either a single password, or the path to the password list you wish to use", required=True)
    arg_parser.add_argument("-p", "--port", help=f"The port you wish to target (only required if running on a non standard port)")
    arg_parser.add_argument("-t", "--threads", help=f"Number of threads to use")
    arg_parser.add_argument("-q", "--quiet", help=f"Do not print banner", nargs='*')

    args = arg_parser.parse_args()
    if args.quiet is None:
        print(banner)

    host = args.Host
    
    service = args.Service.upper()
    if service not in Cerbrutus.services.valid_services:
        print(f"Service named {service} does not exist yet...")
        sys.exit(1)

    port = Cerbrutus.services.valid_services[service]["port"]
    if args.port:
        port = args.port

    if '/' not in args.users and '.' not in args.users and '\\' not in args.users:
        users = [args.users]
    else:
        try:
            userfile = Cerbrutus.Wordlist(args.users)
            users = userfile.read()
        except FileNotFoundError as e:
            print(e)
            sys.exit()

    if '/' not in args.passwords and '.' not in args.passwords and '\\' not in args.passwords:
        passwords = [args.passwords]
    else:
        try:
            passfile = Cerbrutus.Wordlist(args.passwords)
            print("[*] - Initializing password list...")
            passwords = passfile.read()
        except FileNotFoundError as e:
            print(e)
            sys.exit()

    threads = Cerbrutus.services.valid_services[service]["reccomendedThreads"]
    if args.threads:
        try:
            threads = int(args.threads)
        except Exception:
            print("[-] - Specified number of threads is not a number.")
            sys.exit()

    Cerbrutus.BruteUtil(host, port, service, users, passwords, threads=threads).brute()


if __name__ == '__main__':
    main()  
