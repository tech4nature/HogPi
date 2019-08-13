import pir
#========================
#class set up
#==========================
pir_sensor = pir.sensor(4)

#Main program
#==========================
if __name__=="__main__":
    while True:
        a = pir_sensor.read()
        print(a)
        if a == 1:
            print('pir on')
        else:
            print('pir off')
