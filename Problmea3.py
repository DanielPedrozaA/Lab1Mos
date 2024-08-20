from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory


# Definición del modelo
Model = ConcreteModel()

# Conjuntos
recursos = RangeSet(1, 5)
aviones = RangeSet(1, 3)

# Parámetros
valor = {1: 50, 2: 100, 3: 120, 4: 60, 5: 40}
peso = {1: 15, 2: 5, 3: 20, 4: 18, 5: 10}
volumen = {1: 8, 2: 2, 3: 10, 4: 12, 5: 6}

capacidad_peso = {1: 30, 2: 40, 3: 50}
capacidad_volumen = {1: 25, 2: 30, 3: 35}

# Variable de decisión
Model.x = Var(recursos, aviones, domain=Binary)

# Función objetivo: Maximizar el valor total de los recursos transportados
Model.obj = Objective(expr=sum(Model.x[i, j] * valor[i] for i in recursos for j in aviones), sense=maximize)

# Restricciones de capacidad de los aviones
def capacidad_peso_rule(Model, j):
    return sum(Model.x[i, j] * peso[i] for i in recursos) <= capacidad_peso[j]
Model.capacidad_peso = Constraint(aviones, rule=capacidad_peso_rule)

def capacidad_volumen_rule(Model, j):
    return sum(Model.x[i, j] * volumen[i] for i in recursos) <= capacidad_volumen[j]
Model.capacidad_volumen = Constraint(aviones, rule=capacidad_volumen_rule)

# Restricción de exclusividad de recursos
def exclusividad_recursos_rule(Model, i):
    return sum(Model.x[i, j] for j in aviones) == 1
Model.exclusividad_recursos = Constraint(recursos, rule=exclusividad_recursos_rule)

# Restricción de seguridad de medicamentos
Model.seguridad_medicamentos = Constraint(expr=Model.x[2, 1] == 0)

# Restricción de compatibilidad entre equipos médicos y agua potable
def compatibilidad_rule(Model, j):
    return Model.x[3, j] + Model.x[4, j] <= 1
Model.compatibilidad = Constraint(aviones, rule=compatibilidad_rule)

# Especificación del solver
SolverFactory('glpk').solve(Model)

# Mostrar resultados
Model.display()