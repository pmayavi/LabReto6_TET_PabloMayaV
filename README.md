# Reto de programación N1

**Curso:** Tópicos Especiales en Telemática <br>
**Título:** Comunicación entre Procesos Remotos: gRPC.

---

## Tabla de Contenido

1. [Introducción](#introduction)
2. [Problemas](#problemas)
3. [Recursos](#resources)
4. [Desarrollo](#development) 
5. [Despliegue](#deployment) <br>

---

## 1. Introducción

En este reto de laboratorio aprendí a crear clusters en AWS y los puse en práctica.

---

## 2. Problemas

Tuve que cambiar un poco el código de 'wordcount-local.py' y documentarme bien acerca de los comandos para poder editarlos con los respectivos permisos.

---

## 3. Recursos

Utilicé los conocimientos dados en el Laboratorio 5 y comandos tomados y adaptados de los siguientes recursos:

- [Repositorio del Laboratorio N6-MapReduce](https://github.com/ST0263/st0263-2023-1/tree/main/Laboratorio%20N6-MapReduce)
- [Guía de instalación de AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Cómo crear y ejecutar un clúster EMR utilizando AWS CLI](https://towardsdatascience.com/how-to-create-and-run-an-emr-cluster-using-aws-cli-3a78977dc7f0#6df6)
- [Hadoop: Cómo listar archivos y directorios usando HDFS dfs](https://sparkbyexamples.com/apache-hadoop/hadoop-how-to-list-files-and-directories-using-hdfs-dfs/)

---

## 4. Desarrollo

Estos pasos solo los tuve que realizar una vez:  

### Creación del S3:  
![S3](./images/S3.png)

### Edición del security group de la Node Primaria/Master para que reciba SSH de todos lados:  
![securitySSH](./images/securitySSH.png)

### Instalación de AWS CLI:
```sh
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```
Tomado de [Guía de instalación de AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
![AWSCLIinstall](./images/AWSCLIinstall.jpeg)

### Configuración de las credenciales de AWS CLI:  
Se necesita crear una carpeta en el directorio root del usuario llamada '.aws' y dentro de ella se crean 2 archivos sin extensión llamados 'credentials' y 'config':  

![AWSCredentials](./images/AWSCredentials.png)

El contenido del archivo 'credentials' es el siguiente:
```plaintext
[default]
aws_access_key_id=
aws_secret_access_key=
aws_session_token=
```

---

## 5. Laboratorio 5

Crea el cluster usando la interfaz gráfica de AWS:  

![Lab5-1](./images/Lab5-1.png)
![Lab5-2](./images/Lab5-2.png)
![Lab5-3](./images/Lab5-3.png)
![Lab5-4](./images/Lab5-4.png)

Instalación de requerimientos:
```sh
sudo yum install python3-pip &&
sudo pip3 install mrjob &&
sudo yum install git -y
```

Clonar el repositorio:
```sh
git clone https://github.com/p

mayavi/LabReto6_TET_PabloMayaV.git
cd LabReto6_TET_PabloMayaV/wordcount
```

Prueba del código:
```sh
python wordcount-mr.py /home/hadoop/LabReto6_TET_PabloMayaV/datasets/gutenberg-small/*.txt
```
![wordcountFuncional](./images/wordcountFuncinal.jpeg)

---

## 6. Creación del cluster mediante AWS CLI

Se crea el cluster desde la consola con las especificaciones dadas usando AWS CLI:
```sh
aws emr create-cluster --release-label emr-6.10.0 --instance-type m4.large --instance-count 3 --log-uri s3://pmayav-lab-emr/logs --use-default-roles --ec2-attributes KeyName=emr-key,SubnetId=subnet-01fd4a313d0de3645 --no-termination-protected
```

Luego de que se cree correctamente el cluster, se toma el nombre DNS de la Node Primaria/Master:  
![PrimaryNode](https://raw.githubusercontent.com/pmayavi/LabReto6_TET_PabloMayaV/main/images/PrimaryNode.png)
y se establece la conexión SSH:
```sh
ssh -i emr-key.pem hadoop@ec2-44-192-253-171.compute-1.amazonaws.com
```

---

## 7. Funcionalidad de la Main Node

Instalación de requerimientos:
```sh
sudo yum install python3-pip &&
sudo pip3 install mrjob &&
sudo yum install git -y
```

Clonar el repositorio:
```sh
git clone https://github.com/pmayavi/LabReto6_TET_PabloMayaV.git
cd LabReto6_TET_PabloMayaV/wordcount
```

Creación de usuario admin de Hadoop y copiar los datasets al usuario:
```sh
hdfs dfs -mkdir /user/admin/
hdfs dfs -copyFromLocal /home/hadoop/LabReto6_TET_PabloMayaV/datasets/ /user/admin/
```

Ejecutar el wordcount-mr.py en los datasets de Hadoop, el resultado se almacenará en la carpeta 'output1':
```sh
python wordcount-mr.py hdfs:///user/admin/datasets/gutenberg-small/*.txt -r hadoop --output-dir hdfs:///user/admin/output1
```

Para ver las partes del output, usar el comando:
```sh
hdfs dfs -ls -r /user/admin/output1/
```

Para ver el contenido de cada parte individualmente, usar el siguiente comando:
```sh
hdfs dfs -cat /user/admin/output1/part-00000
```
![DirOutput](./images/DirOutput.jpeg)

---

## 8. Reto de programación 1

Para recibir el output se necesita que la carpeta no exista, para testing y errores use este comando para borrar las carpetas del Hadoop:
```sh
hdfs dfs -rm -r /user/admin/output1-a/
```  
a) El salario promedio por Sector Económico (SE):
```sh
python Salario-Sector.py hdfs:///user/admin/datasets/otros/dataempleados.txt -r hadoop --output-dir hdfs:///user/admin/output1-a
```
| Sector economico | Salario promedio |
|------------------|------------------|
| 1212             | 77000.0          |
| 1234             | 37500.0          |
| 5434             | 36000.0          |
| 1412             | 76000.0          |
  
Para visualizar la data use estos comandos:
```sh
hdfs dfs -ls -r /user/admin/output1-a/
hdfs dfs -cat /user/admin/output1-a/part-00000
```
![Reto1-a](./images/Reto1-a.jpeg)  
  
b) El salario promedio por Empleado:
```sh
python Salario.py hdfs:///user/admin/datasets/otros/dataempleados.txt -r hadoop --output-dir hdfs:///user/admin/output1-b
```
| ID del empleado | Salario promedio |
|-----------------|------------------|
| 3237            | 40000.0          |
| 1115            | 76500.0          |
| 3233            | 35500.0          |
  
Para visualizar la data use estos comandos:
```sh
hdfs dfs -ls -r /user/admin/output1-b/
hdfs dfs -cat /user/admin/output1-b/part-00000
```
![Reto1-b](./images/Reto1-b.jpeg)  
  
c) Número de SE por Empleado que ha tenido a lo largo de la estadística:
```sh
python Sector-Empleado.py hdfs:///user/admin/datasets/otros/dataempleados.txt -r hadoop --output-dir hdfs:///user/admin/output1-c
```
| ID del empleado | Numero de SE |
|-----------------|--------------|
| 3237            | 1            |
| 1115            | 2            |
| 3233            | 2            |
  
Para visualizar la data use estos comandos:
```sh
python Sector-Empleado.py hdfs:///user/admin/datasets/otros/dataempleados.txt -r hadoop --output-dir hdfs:///user/admin/output1-c
hdfs dfs -ls -r /user/admin/output1-c/
hdfs dfs -cat /user/admin/output1-c/part-00000
```
![Reto1-c](./images/Reto1-c.jpeg)  
