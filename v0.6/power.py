from output import Output
from subprocess import Popen

fileRW = Output()

class Power:
    def check_weight(self, filename):
        data = fileRW.read("/home/pi/" + filename, 1, True)
        last_3 = data[-3:]
        for i in last_3:
            if i < 100:
                shutdown_pi()

    def shutdown_pi(self):
        Popen(['sudo', 'poweroff'])

    def reboot_pi(self):
        Popen(['sudo', 'reboot'])
