document.addEventListener("DOMContentLoaded",init);
const URL_API= 'http://localhost:3000/api/'

var customers=[]

function init(){
search()
}

function agregar(){
clean()
abrirFormulario()
}

function abrirFormulario(){
  //creacion de la variable que tiene contenida el elemento con id "modale"
htmlModale =document.getElementById("modale");
//al hacer click el la clase "modale" pasa a ser -> "modale opened" y esto abre el agregar
htmlModale.setAttribute("class", "modale opened");
 
}

// con la misma logica de arriba pero invertida 
function cerrarModale(){

htmlModale = document.getElementById("modale");

htmlModale.setAttribute("class", "modale");

}

async function search(){
   var url= URL_API + 'customers'
    var response = await fetch(url, {
      "method": 'GET',
      "headers" : {
      "Content-Type" : 'application/json'
      }
  })
      
  customers =await response.json();
   
  var html = ''
    for (customer of customers ){
      
     var row = `</tr>
    
      <td>${customer.Nombre}</td>
      <td>${customer.Apellido}</td>
      <td>${customer.email}</td>
      <td>${customer.telefono}</td>
      <td>${customer.direccion}</td>
      <td>
          <a href="#" onclick="edit(${customer.id})" class="myButton">Editar</a>
          <a href="#" onclick="remove(${customer.id})" class="myButtonDelete">Eliminar</a>
      </td>
    </tr>`
    html = html + row;

  }  
  document.querySelector('#customers > tbody').outerHTML= html
 
} 

function edit(id){
  abrirFormulario()
  var customer = customers.find(x => x.id == id)
  document.getElementById('txtId').value = customer.id;
  document.getElementById('txtNombre').value = customer.Nombre;
  document.getElementById('txtApellido').value = customer.Apellido;
  document.getElementById('txtCorreo').value = customer.email;
  document.getElementById('txtTelefono').value = customer.telefono;
  document.getElementById('txtDireccion').value = customer.direccion
  }

async function remove(id){

respuesta =confirm("¿Estas seguro de eliminar este cliente?")
  if (respuesta){
    var url= URL_API + 'customers/' + id
     await fetch(url, {
        "method": 'DELETE',
        "headers" : {
        "Content-Type" : 'application/json'
        }
    })

    alert("Se elimino el Cliente de forma exitosa")
    window.location.reload();
  }
}

function clean(){
  document.getElementById('txtId').value = ''
  document.getElementById('txtNombre').value = ''
  document.getElementById('txtApellido').value = ''
  document.getElementById('txtCorreo').value = ''
  document.getElementById('txtTelefono').value = ''
  document.getElementById('txtDireccion').value = ''
}


async function save(){
  
  var data=
  {
    "nombre": document.getElementById('txtNombre').value,
    "apellido": document.getElementById('txtApellido').value,
    "email": document.getElementById('txtCorreo').value,
    "telefono": document.getElementById('txtTelefono').value,
    "direccion": document.getElementById('txtDireccion').value

  }
  var id = document.getElementById('txtId').value

  if(id != '' ){
    data.id = id
  }
 
  var url= URL_API + 'customers'
  await fetch(url, {
      "method": 'POST',
      "body": JSON.stringify(data),
      "headers" : {
      "Content-Type" : 'application/json'
          }
      })
  
      alert("Se Guardo el cliente de manera exitosa")
      window.location.reload();
    }
  