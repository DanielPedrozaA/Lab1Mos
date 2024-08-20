from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

numTrabajadores=3
numTrabajos = 5

p=RangeSet(1, numTrabajadores)
q=RangeSet(1, numTrabajos)

valorTrabajadores={1:8, 2:10, 3:6}
valorTrabajo = {1:(50,4), 2:(60,5), 3:(40,3), 4:(70,6), 5:(30,2)}

Model.x = Var(q,p, domain=Binary)

Model.obj = Objective(expr=sum(Model.x[j, i] * valorTrabajo[j][0] for j in q for i in p), sense=maximize)

def horasLimite(Model, i):
    return sum(Model.x[j, i] * valorTrabajo[j][1] for j in q) <= valorTrabajadores[i]

Model.res1 = Constraint(p, rule=horasLimite)


def trabajoUnico(Model, j):
    return sum(Model.x[j, i] for i in p) <=1

Model.res2 = Constraint(q, rule=trabajoUnico)

# Especificación del solver
SolverFactory('glpk').solve(Model)

# Mostrar resultados
Model.display()


