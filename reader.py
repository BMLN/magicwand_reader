import os
import serial
import threading



class Reader(threading.Thread):
    def __init__(self, monitor):
        threading.Thread.__init__(self)
        self.monitor = monitor
        self.should_run = True
        self.output = []

    #uglyaf
    def __sanitize(self):
        self.output = [ x.decode("utf-8").replace("\r\n", "").split(',') for x in self.output ]
        self.output = list(filter(lambda line : len(line) == 8 and str(line[0])[0] == '#' and str(line[-1])[-1] == '#' , self.output))
        self.output = [ ";".join(x[1:4] + x[5:]).replace('#', '') for x in self.output ]

    def run(self):
        while self.should_run:
            self.output.append(monitor.readline())
        
        self.__sanitize()







user_input = 0
name_index = 0
monitor = serial.Serial(port=os.environ["ARD_PORT"], baudrate=os.environ["ARD_BAUD"], timeout=.1)


while user_input != "quit":
    user_input = input("'quit' or Spell name to record? ")
    spell_name = user_input

    while user_input != "quit":
        user_input = input("'quit', 'new' or 'Enter' to record: ")

        if user_input == "new":
            break
        elif user_input == "":
            #read
            monitor.flushInput()
            monitor.flushOutput()
            output = []

            recording = Reader(monitor)
            recording.start() 

            input("recording...\n'Enter' to end recording\n")
            recording.should_run = False
            recording.join()


            #write
            while os.path.exists("./" + str(name_index) + ".csv"):
                name_index += 1

            f = open(str(name_index) + ".csv", "w")
            f.write("wizardName;spellName;accX;accY;accZ;gyroX;gyroY;gyroZ\n")
            for line in recording.output:
                f.write( "lol, im a wizard" + ";" + str(spell_name) + ";" + str(line) + "\n")
            f.close()

monitor.close()
exit()