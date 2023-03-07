from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, constr, validator
import database as db
import helpers


headers = {"content-type": "charset=utf-8"}


class ModeloVehiculo(BaseModel):
    numero_de_serie: constr(min_length=7, max_length=7)
    color: constr(min_length=2, max_length=30)
    ruedas: constr(min_length=1, max_length=30)


class ModeloCrearCliente(ModeloVehiculo):
    @validator("numero_de_serie")
    def validar_dni(cls, dni):
        if not helpers.numero_valido(dni, db.Vehiculos.lista):
            raise ValueError("Cliente ya existente o DNI incorrecto")
        return dni


app = FastAPI(
    title="API del Gestor de vehiculos",
    description="Ofrece diferentes funciones para gestionar los vehiculos.")


@app.get("/clientes/", tags=["Clientes"])
async def clientes():
    content = [cliente.to_dict() for cliente in db.Vehiculos.lista]
    return JSONResponse(content=content, headers=headers)


@app.get("/clientes/buscar/{dni}/", tags=["Clientes"])
async def clientes_buscar(dni: str):
    cliente = db.Vehiculos.buscar(numero_de_serie=dni)
    if not cliente:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    return JSONResponse(content=cliente.to_dict(), headers=headers)


@app.post("/clientes/crear/", tags=["Clientes"])
async def clientes_crear(datos: ModeloCrearCliente):
    cliente = db.Vehiculos.crear(datos.numero_de_serie, datos.color, datos.ruedas, datos.velocidad, datos.cilindrada, datos.carga, datos.equipo, datos.tipo, datos.modelo)
    if cliente:
        return JSONResponse(content=cliente.to_dict(), headers=headers)
    raise HTTPException(status_code=404)


@ app.put("/clientes/actualizar/", tags=["Clientes"])
async def clientes_actualizar(datos: ModeloVehiculo):
    if db.Vehiculos.buscar(datos.numero_de_serie):
        cliente = db.Vehiculos.modificar(datos.numero_de_serie, datos.color, datos.ruedas, datos.velocidad, datos.cilindrada, datos.carga, datos.equipo, datos.tipo, datos.modelo)
        if cliente:
            return JSONResponse(content=cliente.to_dict(), headers=headers)
    raise HTTPException(status_code=404)


@app.delete("/clientes/borrar/{dni}/", tags=["Clientes"])
async def clientes_borrar(dni: str):
    if db.Vehiculos.buscar(numero_de_serie=dni):
        cliente = db.Vehiculos.borrar(numero_de_serie=dni)
        return JSONResponse(content=cliente.to_dict(), headers=headers)
    raise HTTPException(status_code=404)

print("Servidor de la API...")
