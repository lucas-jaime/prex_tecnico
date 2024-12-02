Buenos días equipo PREX, cómo están?
A continuación les dejo un detalle de mi paso a paso sobre el challenge técnico.
En primera instancia organicé los paths de manera tal que se pueda dockerizar, es decir: 

*/prex_tecnico/agent/ :
agent.py
requeriments.txt
dockerfile

*/prex_tecnico/appi/ :
app.py
requeriments.txt
dockerfile

Luego desarrollé el agente ya que la api tendría dependencia del mismo. En cuanto a este, no enfreté muchas complicaciones al realizarlo ya que si bien 
nunca hice un código similar de consulta de tal tipo sobre servidores, la librería era sencilla de utilizar.
Una vez realizado el agente di comienzo con la API, aqui sí enfrenté más problemas y tuve que leer mucha documentación ya que nunca había inicializado un sqlite embebido al código, 
por ende tuve que aprender un poco sobre como flask se comportaba ante este escenario. Finalmente logré crearla y levantarla.

Desde AWS cree mi EC2, un Linux Ubuntu de capa gratuita.
Una vez instalado cloné mi repositorio:

git clone https://github.com/lucas-jaime/prex_tecnico.git

![image](https://github.com/user-attachments/assets/36207167-4300-477c-ab37-9812b69fe553)

Luego realizo la instalación de docker para poder ejecutar mi archivo yml en la raíz del repositorio

sudo apt install -y docker-compose

![image](https://github.com/user-attachments/assets/13446712-3d87-403c-9aea-4e3bf531d70b)


Verificar la instalación:

![image](https://github.com/user-attachments/assets/7a04d43f-3595-49b5-a50f-4c160effffd0)

Una vez realizada la instalación, ingresar al path donde fue almacenado el repo, en mi caso simplemente fue hacer cd a prex_tecnico. Situados en el repo, inicializar docker

docker-compose build
docker-compose up -d

![image](https://github.com/user-attachments/assets/533aac2b-3261-4dab-b32e-e707bac51a61)

![image](https://github.com/user-attachments/assets/ddaf65db-e07e-4a39-9299-ea2d3caef7e9)

Podemos verificar la instalación corriendo el comando ps ya que nos brindará un estado de nuestra api y agente

docker-compose ps

![image](https://github.com/user-attachments/assets/acc1f510-99c0-4fb4-902f-c15cced923b3)

Debería verse algo tal que así, tiene sentido que el agente no esté "UP" ya que no itera, sino que se basa en una consulta por ejecución, en cambio la API sí.

Por último, corremos el agente:

docker-compose run agent

![image](https://github.com/user-attachments/assets/813cec97-9601-4fe2-a45e-f50c79bee168)

Y para realizar la consulta a la API realizamos un POST del tipo:

curl http://3.137.162.127:5000/get_server_info/<IP>

Aquí lamentablemente me encontré con un error el cual no pude solucionar, 

![image](https://github.com/user-attachments/assets/c4a57eb5-3450-405f-a8d1-6c61592e20da)

Investigando, logré hallar que la infromación a la API es, en efecto, enviada desde el agente, ya que si corremos

docker exec -it prex_tecnico_api_1 /bin/bash

Buscamos la base de datos creada:

find / -name "*.db"

Observamos la tabla creada desde la consola de python:

import sqlite3
conn = sqlite3.connect('/app/instance/server_info.db')  
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
print(cursor.fetchall())  

Consultamos los datos dentro de la tabla:

cursor.execute('SELECT * FROM server_info;')
print(cursor.fetchall())

![image](https://github.com/user-attachments/assets/df3a6eee-3a33-4f72-a8b6-009d9f8f2f37)



Y en efecto, la info es enviada pero al hacer la consulta falla al no encontrar la IP solicitada. He revisado reiteradas veces el código y lamentablemente no pude concluír donde se 
encuentra el error. 

Espero que les haya servido y muchas gracias por la oportunidad. Saludos!



