import cv2
import urllib.request
import numpy as np
import random
import tkinter as tk
from PIL import Image, ImageTk
import datetime
import random
import os
from google.cloud import storage
import time
import pandas as pd
from google.cloud import bigquery


def main():
    

    url = 'ip de mi camara web'
    winName = 'ESP32 CAMERA'
    cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(winName, 1280, 900)  # Ajusta el tamaño de la ventana

    classNames = []
    classFile = 'coco.names'
    with open(classFile, 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')

    configPath = 'ssd_mobilenet.pbtxt'
    weightsPath = 'frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)



    root = tk.Tk()
    root.title("Detección de Objetos")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Definir el tamaño de la ventana
    window_width = 1050
    window_height = 720

    # Calcular las coordenadas para centrar la ventana
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Establecer la geometría de la ventana para centrarla
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    # Crear un lienzo para mostrar la imagen
    canvas = tk.Canvas(root, width=900, height=600)
    canvas.pack()

    # Variable de cadena de Tkinter para el contador de objetos
    contador_var = tk.StringVar()
    contador_var.set("Objetos detectados: 0")

    # Etiqueta para mostrar el contador de objetos
    contador_label = tk.Label(root, textvariable=contador_var, font=("Helvetica", 16))
    contador_label.pack()

    clases_detectadas_var = tk.StringVar()
    clases_detectadas_var.set("Clases detectadas: ")

    # Etiqueta para mostrar las clases detectadas
    clases_detectadas_label = tk.Label(root, textvariable=clases_detectadas_var, font=("Helvetica", 16))
    clases_detectadas_label.pack()


    def upload_to_gcs(credentials_file, bucket_name, file_to_upload):
        try:
            # Inicializa el cliente de Storage con las credenciales
            storage_client = storage.Client.from_service_account_json(credentials_file)

            # Obtiene el objeto de Bucket
            bucket = storage_client.get_bucket(bucket_name)

            # Define el nombre del archivo en el bucket
            blob_name = os.path.basename(file_to_upload)

            # Crea un objeto Blob en el bucket
            blob = bucket.blob(blob_name)

            # Sube el archivo al bucket
            blob.upload_from_filename(file_to_upload)

            print(f"El archivo '{file_to_upload}' se ha subido exitosamente a '{bucket_name}' como '{blob_name}'.")

        except Exception as e:
            print(f"Error al subir el archivo: {e}")


    def tomar_foto():
        imgResponse = urllib.request.urlopen(url)
        imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)


        fecha_hoy = datetime.datetime.now().strftime("%Y%m%d")
        valor_random = random.randint(1000000, 9999999)

        directorio="fotos"
        nombre_foto = fecha_hoy +"-"+ str(valor_random)+ str(valor_random)
        ruta_foto = os.path.join(directorio, f'{nombre_foto}.jpg')
        cv2.imwrite(ruta_foto, img)

        credentials_file = "proyecto-arduino-403318-5750e3241bc9.json"
        bucket_name = "fotos-arduino"
        file_to_upload = ruta_foto
        upload_to_gcs(credentials_file, bucket_name, file_to_upload)

    def procesar_data():
        global df_clases_detectadas

        project_id = "proyecto-arduino-403318"
        dataset_id = "imagenes_arduino"
        table_id = "Datos detección de objetos"

        # Crea un DataFrame de Pandas con tus datos
        data = df_clases_detectadas
        # Inicializa el cliente de BigQuery
        client = bigquery.Client(project=project_id)

        # Define la referencia a la tabla en BigQuery
        table_ref = client.dataset(dataset_id).table(table_id)

        # Crea un objeto JobConfig para la carga de datos
        job_config = bigquery.LoadJobConfig()
        #WRITE_APPEND
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND  # Opcional: ajusta esta configuración según tus necesidades

        # Carga el DataFrame en BigQuery
        client.load_table_from_dataframe(data, table_ref, job_config=job_config)

        
    x_coord = 900 
    y_coord = 50

    boton_foto = tk.Button(root, text="Tomar Foto", command=tomar_foto, width=15, height=2, bg="blue", fg="white")
    boton_foto.place(x=x_coord, y=y_coord)
    boton_foto.configure(cursor="hand2") 

    #boton_procesar = tk.Button(root, text="Procesar Data", command=procesar_data, width=15, height=2, bg="blue", fg="white")
    #boton_procesar.place(x=900, y=100)
    #boton_procesar.configure(cursor="hand2") 

    df_clases_detectadas = pd.DataFrame(columns=["Clase", "Confianza", "Fechas"])

    # Función para actualizar la imagen en el lienzo de la interfaz
    def actualizar_imagen():
        
        global df_clases_detectadas 

        imgResponse = urllib.request.urlopen(url)
        imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)
        classIds, confs, bbox = net.detect(img, confThreshold=0.5)


        if len(classIds) != 0:
            lista_objetos=[]
            confianza=[]
            clases=[]
            fechas=[]
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
                cv2.rectangle(img, box, color=color, thickness=3)
                label = f'{classNames[classId - 1]}: {confidence*100:.1f}%'
                cv2.putText(img, label, (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)
                
                fecha_hoy = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
                lista_objetos.append(label)
                clases.append(classNames[classId - 1])
                confianza.append(confidence)
                fechas.append(fecha_hoy)
                nueva_fila = pd.DataFrame({"Clase": clases,
                                            "Confianza": confianza, 
                                            "Fechas": fechas})
                
                df_clases_detectadas = pd.concat([df_clases_detectadas, nueva_fila], ignore_index=True)
                #print(nueva_fila)
                #print(df_clases_detectadas)

                #print(clases)
                #print(confianza)
                

            clases_detectadas_var.set("Clases detectadas: " + ', '.join(lista_objetos))

            contador_objetos = len(classIds)
            contador_label.config(text=f"Objetos detectados: {contador_objetos}")

            contador_objetos = len(classIds)
            contador_var.set(f"Objetos detectados: {contador_objetos}")

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        
        canvas.img = img
        canvas.create_image(0, 0, anchor=tk.NW, image=img)
        root.after(100, actualizar_imagen)


    actualizar_imagen()

    root.mainloop()


if __name__ == "__main__":
    df_clases_detectadas = pd.DataFrame(columns=["Clase", "Confianza", "Fechas"])
    main()
    print(df_clases_detectadas)
    df_clases_detectadas.to_csv("clase_detectadas.csv", index=False)
