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
        #with open("README.txt","r",encoding="utf-8") as o:
        #ubicacion = o.readline()            
        #print(ubicacion)
        with open("valores.csv","r",encoding="utf-8") as f:
            lineas = f.read().splitlines()
            lineas.pop(0)    
            for l in lineas:
                linea = l.split(',')
                self.datos.append(float(linea[2]))
                self.datos.append(float(linea[3]))
        return self.datos
        

class Armo_json:        
    def armo_json(self,datos):  
        print("creo json") 
        self.data = {} 
        self.data['Moneda'] = []
        self.data['Moneda'].append({
            "id": 1,
            "value1": datos[0],
            "value2": datos[1],
            "name": "Dolar"})
        self.data['Moneda'].append({
            "id": 2,
            "value1": datos[2],
            "value2": datos[3],
            "name": "Euro"})
        self.data['Moneda'].append({
            "id": 3,
            "value1": datos[4],
            "value2": datos[5],
            "name": "Real"})
        with open('data.json', 'w') as file:
            json.dump(self.data, file, indent=4) 
        return self.data
#data = json.loads(open('data.json').read())
class Main:

    def __init__(self):
            pass

    def print_msg(self):
        print("Hasta luego...")
        exit(1)

    def handler(self,sig, frame):  # define the handler  
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
i=0
P=Main()

while i<=5:     #envìo cada 3 segundos solo 4 veces para prueba
    P.main()
    time.sleep(5)
    i+=1
