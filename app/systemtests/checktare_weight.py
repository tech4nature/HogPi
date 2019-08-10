import weight
import time
#initiate separately as we will once an hour
while True:
    weight_sensor = weight.sensor()
    print(weight_sensor.read())
    weight_sensor.tare_weight()
    time.sleep(10) # wait 30s try different values 1 to 30s
    # =======carry out action as if in loop ============
    weight_sensor = weight.sensor()
    print(weight_sensor.write("weight.csv", 30))
    weight_sensor.avrg("weight.csv", "avrweight.csv")  #
# weight_sensor.tare_weight(100)  # 100 = min tolerance
