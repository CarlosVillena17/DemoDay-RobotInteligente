# Robot Inteligente
## Descripcion
Este robot autónomo combina la potencia de la inteligencia artificial con la movilidad de
un vehículo controlado a distancia. Está equipado con una cámara web ESP32 –
CAM y la capacidad de conectarse a través de Bluetooth y Wi-Fi, este robot es capaz de
explorar, analizar y detectar objetos en tiempo real en las instalaciones de nuestra Facultad 
de Ingeniería de Sistemas e informática.
La detección de objetos se realiza a través del uso de algoritmos de visión artificial,
permitiendo al robot identificar y clasificar una amplia variedad de elementos, desde
materiales de laboratorio hasta personas y obstáculos en su camino. Esto no solo
amplía las capacidades de nuestro robot, sino que también contribuye a la seguridad y la 
eficiencia en la facultad
Asimismo, gracias a su capacidad de conexión Wi-Fi, el robot puede ser controlado de
forma remota, lo que permite a los usuarios supervisar su entorno en tiempo real y
tomar decisiones informadas desde cualquier ubicación. Ya sea para investigaciones
académicas, tareas de seguridad o simplemente para obtener información valiosa, nuestro robot se convierte en una herramienta versátil y valiosa en la FISI

![WhatsApp Image 2023-10-28 at 2 36 16 PM](https://github.com/CarlosVillena17/DemoDay-RobotInteligente/assets/86505880/962119ab-8090-4c47-ae04-ff33ef6698bd)

![WhatsApp Image 2023-10-28 at 2 36 08 PM](https://github.com/CarlosVillena17/DemoDay-RobotInteligente/assets/86505880/0a27569f-7c30-49bd-b53e-0c77c76f01c3)
## Diagrama del carro 

![diagrama](https://github.com/CarlosVillena17/DemoDay-RobotInteligente/assets/86505880/b173fdf2-13aa-43c9-b073-c74afd1ecbb6)

![1342db7c0ddc72a86809cbccc7c9f66a034f0885_2_690x406-removebg-preview](https://github.com/CarlosVillena17/DemoDay-RobotInteligente/assets/86505880/286c109e-bfca-4e74-b55d-e343bd095cef)

## Envío de fotos a Google Cloud Storage

**Captura de imágenes:** Utiliza la cámara web ESP32-CAM para capturar imágenes en tiempo real de los objetos o áreas de interés.

**Procesamiento de imágenes:** Procesa las imágenes según sea necesario para la detección de objetos y otras tareas.

**Google Cloud Storage:** Utiliza la API de Google Cloud Storage para cargar las imágenes procesadas en un bucket específico en tu proyecto de Google Cloud Storage. Puedes usar la biblioteca cliente de Google Cloud Storage o la herramienta `gsutil` para realizar esta acción.

**Almacenamiento y acceso:** Una vez que las imágenes se almacenan en el bucket de Google Cloud Storage, puedes acceder a ellas de manera segura desde cualquier ubicación y compartirlas según sea necesario.
