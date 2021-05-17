from covid import app
import csv
import json

@app.route("/provincias")
def provincias():
    fichero = open("data/provincias.csv", "r", encoding="utf16")
    csvreader = csv.reader(fichero, delimiter=",")

    lista = []
    for registro in csvreader:
        d = {"codigo": registro[0], "valor": registro[1]}
        lista.append(d)

    fichero.close()
    print(lista)
    return json.dumps(lista)

@app.route("/provincia/<codigoProvincia>")
def laprovincia(codigoProvincia):
    fichero = open("data/provincias.csv", "r", encoding="utf16")
    dictreader = csv.DictReader(fichero, fieldnames=["codigo", "provincia"])
    for registro in dictreader:
        if registro["codigo"] == codigoProvincia:
            fichero.close()
            return registro["provincia"]
    
    fichero.close()
    return "El valor no existe. Largo de aquí!"


@app.route("/casos/<int:year>", defaults={"mes":None, "dia":None})
@app.route("/casos/<int:year>/<int:mes>", defaults={"dia":None})
@app.route("/casos/<int:year>/<int:mes>/<int:dia>")
def casos(year, mes, dia): #aquí podemos poner dia=None y quitar el defaults del segundo route
    
    # validar fecha
    
    if not mes:
        fecha = "{:04d}".format(year)
    elif not dia:
        fecha = "{:04d}-{:02d}".format(year, mes)
    else:
        fecha = "{:04d}-{:02d}-{:02d}".format(year, mes, dia)

    fichero = open("data/casos_diagnostico_provincia.csv", "r")
    dictReader = csv.DictReader(fichero)

    res = {
    'num_casos': 0,
    'num_casos_prueba_pcr': 0,
    'num_casos_prueba_test_ac': 0,
    'num_casos_prueba_ag': 0,
    'num_casos_prueba_elisa': 0,
    'num_casos_prueba_desconocida': 0
    }

    for registro in dictReader:
        if fecha in registro['fecha']:
            for clave in res:
                res[clave] += int(registro[clave])


        elif registro['fecha'] > fecha:
            break
    
    fichero.close()
    return json.dumps(res)
