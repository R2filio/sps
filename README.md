# Metrobus

Api metro bus cdmx
La Api esta desarrollada en Flask y se conecta a una base de datos postgresql.
El primer paso es abrir el archivo config.json para editar las credenciales de la base de datos que se va a utilizar

El segundo paso para correr el proyecto es restaurar la base de datos que se encuentra en el archivo base.sql
El tercer paso es Correr el scrpt con el nombre Monitor.py que cargara los datos abiertos de posiciones de metrobus de la CDMX.(Nota: Los datos son correspondientes a cada hora debido a que para acceder a los datos en tiempo real, se llevo a cabo una solicitud de datos, pero hasta el momento no he tenido respuesta para acceder a ellos.
El cuarto paso es correr el archivo run.py que inicializa la el servicio.

-El servicio cuanta con cuatro metodos
1- ubicacion/  regresa una lista de la posicion geografica de cada uno de los metrobuses asi como la alcaldia donde se encuentran

2- historial/<<int:id_mb>> regresa el historial de un dia completo de un metrobus(id_mb)

3- alcaldias/ regresa una lista de alcaldias en la ultima hora.

4- /historial/alcaldia/<int:id_alcaldia> regresa el historial de id_mb que estuvieron en una alcaldia determinada(id_alcaldia)
 
 
 
