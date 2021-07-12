# Cerbrutus
Modular brute force tool written in Python, for very fast password spraying SSH, and FTP and in the near future other network services.

COMING SOON: **SMB, HTTP(s) POST, HTTP(s) GET, HTTP BASIC AUTH**
*Thanks to @0dayctf, Rondons, Enigma, and 001 for testing and contributing*

## Installation:
```bash
cd /opt
git clone https://github.com/Cerbrutus-BruteForcer/cerbrutus
```

## Usage:
```bash
python3 /opt/cerbrutus/cerbrutus.py --help
usage: cerbrutus.py [-h] -U USERS -P PASSWORDS [-p PORT] [-t THREADS] [-q [QUIET [QUIET ...]]] Host Service

Python based network brute forcing tool!

positional arguments:
  Host                  The host to connect to - in IP or VHOST/Domain Name form
  Service               The service to brute force (currently implemented 'SSH')

optional arguments:
  -h, --help            show this help message and exit
  -U USERS, --users USERS
                        Either a single user, or the path to the file of users you wish to use
  -P PASSWORDS, --passwords PASSWORDS
                        Either a single password, or the path to the password list you wish to use
  -p PORT, --port PORT  The port you wish to target (only required if running on a non standard port)      
  -t THREADS, --threads THREADS
                        Number of threads to use
  -q [QUIET [QUIET ...]], --quiet [QUIET [QUIET ...]]
                        Do not print banner
```

```bash
/opt/cerbrutus/cerbrutus.py 10.10.10.10 SSH -U "username" -P /opt/wordlists/fasttrack.txt -t 10

        ================================================================
            __    ___  ____   ____   ____  __ __  ______  __ __  _____
           /  ]  /  _]|    \ |    \ |    \|  |  ||      ||  |  |/ ___/
          /  /  /  [_ |  D  )|  o  )|  D  )  |  ||      ||  |  (   \_
         /  /  |    _]|    / |     ||    /|  |  ||_|  |_||  |  |\__  |
        /   \_ |   [_ |    \ |  O  ||    \|  :  |  |  |  |  :  |/  \ |
        \     ||     ||  .  \|     ||  .  \     |  |  |  |     |\    |
         \____||_____||__|\_||_____||__|\_|\__,_|  |__|   \__,_| \___|

        Network Brute Force Tool
        https://github.com/Cerbrutus-BruteForcer/cerbrutus
        ================================================================
        
[*] - Initialising password list...
Read in 224 words from /opt/wordlists/fasttrack.txt
[+] - Running with 10 threads...
[*] - Starting attack against username@10.10.10.10
[*] - Trying: 65/224
```

## Test Run:
```text
# The password is in line number 12600 in rockyou

64 threads -> 1400 seconds ~ 7 minutes (hydra took 30 minutes)
1000 threads -> 464 seconds -> 27 requests per second
100 threads took 1000 seconds -> 12 requests per second 

# the password is in line 460 
100 threads took 32 seconds -> 14 requests per second
1000 threads took 16 seconds -> 28 requests per second
64 threads took 51 seconds -> 9 requests per second (hydra took the same time)

# word number 20k in rockyou
1100 threads took 637 seconds which means 31 rps
110 threads took 1457 seconds so that's 13.7 rps
```

Uses a custom implementation of paramiko to overcome a few minor issues with implementing it for ssh brute forcing. - https://github.com/paramiko/paramiko/
