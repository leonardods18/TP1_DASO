import json
import socket
import signal  
import time
import traceback


class leer_archivo:
    def __init__(self): 
        self.datos = []
        
    
    def updatearchivo(self):           
        print("leo archivo.csv")        
       
        with open("README.txt","r",encoding="utf-8") as u:  #busco la ubicacion del archivo readme.txt
            ubicacion = u.read()                        
                
        with open(ubicacion,"r",encoding="utf-8") as f:  #leo el archivo .csv y buardo en datos[]
        #with open('valores.csv',"r",encoding="utf-8") as f:  #leo el archivo .csv y buardo en datos[]
            lineas = f.read().splitlines()
            lineas.pop(0)    # salteo la primera fila de los nombres
            for l in lineas:
                linea = l.split(',')
                self.datos.append(linea[1])
                self.datos.append(float(linea[2]))
                self.datos.append(float(linea[3]))        
        return self.datos
        

class Armo_json:        # con los datos[] armo el json en self.data
    def armo_json(self,datos):  
        print("creo json") 
        self.data = []       
        self.data.append({
            "id": 1,
            "value1": datos[1],
            "value2": datos[2],
            "name": datos[0]})
        self.data.append({
            "id": 2,
            "value1": datos[4],
            "value2": datos[5],
            "name": datos[3]})
        self.data.append({
            "id": 3,
            "value1": datos[7],
            "value2": datos[8],
            "name": datos[6]})
        with open('data.json', 'w',encoding="utf-8") as file:
            json.dump(self.data, file, indent=4) 
        return self.data

class Main:

    def __init__(self):
            pass

    def print_msg(self):   #imprimo si llega señal
        print("Hasta luego...")
        exit(1)

    def handler(self,sig, frame):  # señal
        print("Signal Number:", sig, " Frame: ", frame)  
        traceback.print_stack(frame)	
        self.print_msg()

    def main(self):

        host = "localhost"
        port = 10000     
        
        signal.signal(signal.SIGINT, self.handler)  

        self.archivo = leer_archivo()
        datoArchivo = self.archivo.updatearchivo()
        self.Json_Data= Armo_json()
        json_data = self.Json_Data.armo_json(datoArchivo)
        
        print(json_data)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(json.dumps(json_data).encode('utf-8'), ("localhost", port))

        respuesta, addr = sock.recvfrom(1024) # espero la respuesta y la imprimo
        print("received message: %s" % respuesta)
i=0
P=Main()

while i<=50:     #envìo cada 10 segundos solo 50 veces para prueba
    P.main()     #sale del while con la señal contro+C
    time.sleep(10)
    i+=1
