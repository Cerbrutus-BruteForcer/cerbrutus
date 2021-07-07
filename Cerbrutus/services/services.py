import time
import paramiko
import sys
sys.tracebacklimit = None   


class SSH:
    @staticmethod
    def connect(ip: str, port: int, username: str, password: str):
        time.sleep(0.1)
        ssh_client = paramiko.client.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # print(f"{username=} {password=}")
        try:
            ssh_client.connect(hostname=ip, port=port, username=username, password=password, allow_agent=False, look_for_keys=False, banner_timeout=60, auth_timeout=4)
        except paramiko.ssh_exception.AuthenticationException:
            ssh_client.close()
            return False
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            #  CANNOT CONNECT TO SERVER
            return None
        except paramiko.SSHException:
            # print("Timing out for 5 seconds...")
            time.sleep(2)
            ssh_client.close()
            return SSH.connect(ip, port, username, password)

        ssh_client.close()
        return True


valid_services = {'SSH': {"class": SSH, "reccomendedThreads": 100, "port": 22}}  # maybe add reccomended number of threads based on testing
