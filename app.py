import os
from flask import Flask, render_template, abort,request
import json
app = Flask(__name__)

with open("MSX.json") as fichero:
    info=json.load(fichero)


@app.route('/',methods=["GET"])
def inicio():
    return render_template("inicio.html")

@app.route('/juegos',methods=["GET","POST"])
def juegos():
    categorias=[]
    for i in info:
        categorias.append(str(i["categoria"]))
    categorias=list(set(categorias))
    if request.method=="GET":
        return render_template("juegos.html",categorias=categorias)
    #Mejora de una sola ruta. No se utiliza la plantilla listajuegos.html
    else:
        try:
            cadena=request.form.get("name")
        except:
            abort(404)
        categoria=request.form.get("cat")
        juegos=[]
        desarrolladores=[]
        identificadores=[]
        for juego in info:
            if cadena in str(juego["nombre"]) and categoria == str(juego["categoria"]):
                juegos.append(str(juego["nombre"]))
                desarrolladores.append(str(juego["desarrollador"]))
                identificadores.append(str(juego["id"]))
                filtro=zip(juegos,desarrolladores,identificadores,categorias)    
            elif cadena == "" and categoria == "":
                juegos.append(juego["nombre"])
            elif cadena in str(juego["nombre"]) and categoria == "Todos":
                juegos.append(str(juego["nombre"]))
                desarrolladores.append(str(juego["desarrollador"]))
                identificadores.append(str(juego["id"]))
                filtro=zip(juegos,desarrolladores,identificadores,categorias)    

        return render_template("juegos.html",juegos=filtro,cadena=cadena,categorias=categorias,categoria=categoria)

@app.route('/juego/<int:identificador>', methods=["GET","POST"])
def detallejuego(identificador):
    juegos=[]
    desarrolladores=[]
    identificadores=[]
    sistemas=[]
    distribuidores=[]
    categorias=[]
    anyos=[]

    for juego in info:
        if identificador == int(juego["id"]):
            juegos.append(str(juego["nombre"]))
            desarrolladores.append(str(juego["desarrollador"]))
            identificadores.append(str(juego["id"]))
            sistemas.append(str(juego["sistema"]))
            distribuidores.append(str(juego["distribuidor"]))
            categorias.append(str(juego["categoria"]))
            anyos.append(str(juego["año"]))
            filtro=zip(identificadores,juegos,sistemas,distribuidores,desarrolladores,categorias,anyos)    
    return render_template("detallejuego.html",juegos=filtro)
        




#Probar en el entorno de desarrollo
app.run(debug=True)

#Despliegue en Heroku
port=os.environ["PORT"]
app.run('0.0.0.0',int(port), debug=True)
