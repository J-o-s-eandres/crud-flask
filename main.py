
from flask import Flask, render_template, jsonify,request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

app = Flask(__name__) #variables globales
cors= CORS(app)

#configuracion de MySQL
app.config['CORS_HEADERS'] ='Content-Type'
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'system'

#inicializar
mysql = MySQL(app)


@app.route('/api/customers') #se usa GET
@cross_origin() #permite que se pueda llamar de puertos y paginas web diferentes
def getAllCustomers():

    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM customers')
    data = cur.fetchall()#traemos todo lo que hallamos consultado
    result= []
    for row in data:
        content = {
                'id':row[0],
                'Nombre' : row[1], 
                'Apellido':row[2], 
                'email' : row[3], 
                'telefono' :row[4] , 
                'direccion': row[5]
         }

        result.append(content)
    return jsonify(result)#funcion que convierte el resultado en json
    

@app.route('/api/customers/<int:id>')# _se usa GET(siempre que llamamos a una URL)
@cross_origin()
def getCustomer(id):   
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM customers WHERE id ='+ str(id))
    data = cur.fetchall()#traemos todo lo que hallamos consultado
    content={}
    for row in data:
        content = {
            'id':row[0],
            'Nombre' : row[1], 
            'Apellido':row[2], 
            'email' : row[3], 
            'telefono' :row[4] , 
            'direccion': row[5]
         
         }
       
    return jsonify(content)#funcion que convierte el resultado en json
    

@app.route('/api/customers',methods=['POST']) #Se una POST

@cross_origin()
def createCustomer():


    if 'id' in request.json: #buscara si en la request hay id si lo hay modifica y sino crea
        updateCustomer()
    else:
        createCustomer()

    return 'ok'      

def createCustomer():   
    cur= mysql.connection.cursor()#devuelve objeto que nos permite modificar la BD
    cur.execute("INSERT INTO `customers` (`id`, `nombre`, `apellido`, `email`, `telefono`, `direccion`) VALUES (NULL, %s, %s, %s, %s, %s);", 
                (request.json['nombre'], request.json['apellido'], request.json['email'], request.json['telefono'], request.json['direccion']))
    mysql.connection.commit()#Empaqueta los llamados y los envia a la bd
    return 'Cliente Guardado'

def updateCustomer():   
    cur= mysql.connection.cursor()#devuelve objeto que nos permite modificar la BD
    cur.execute("UPDATE `customers` SET `nombre` = %s, `apellido` = %s, `email` = %s, `telefono` = %s, `direccion` = %s WHERE `customers`.`id` = %s;",
                (request.json['nombre'], request.json['apellido'], request.json['email'], request.json['telefono'], request.json['direccion'], request.json['id']))  
    mysql.connection.commit()#Empaqueta los llamados y los envia a la bd
    return 'Cliente Guardado'




@app.route('/api/customers/<int:id>',methods=['DELETE']) #Se una POST(y se usa el ID para poder eliminar un cliente en especifico y no a todos los clientes "pensar en el where de la bd")
@cross_origin()
def removeCustomer(id):
    cur= mysql.connection.cursor()#devuelve objeto que nos permite modificar la BD
    cur.execute("DELETE FROM `customers` WHERE `customers`.`id` = "+str(id) +";")#convertimos el id (que es int) en un str y lo hacemos dinamico (para que no solo reciba un id sino que pueda pasarse cualquiera)
    mysql.connection.commit()
    return 'Cliente Eliminado'



@app.route('/')#ruta por defecto
@cross_origin()

def index():
    return render_template('index.html')


@app.route('/<path:path>/')
@cross_origin()
def publicFile(path):
    return render_template(path)


if __name__ == '__main__':
    app.run(None, 3000, True)