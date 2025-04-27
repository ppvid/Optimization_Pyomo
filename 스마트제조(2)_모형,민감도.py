from pyomo.environ import *
model2=ConcreteModel()

#민감도 분석을 위해 Dual Suffix를 설정(제약식마다 대응하는 쌍대값(민감도정보)를 저장장)
#.dual : 쌍대변수를 저장하는 공간에 모델을 추가하는 것
#Suffix: 모델에 추가 정보를 저장하는 문법
#Direction=Suffix.IMPORT : 최적화 후, 솔버로부터 쌍대변수 값을 가져오기 위한 코드
model2.dual= Suffix(direction=Suffix.IMPORT)
#의사결정변수 
model2.x=Var(domain=NonNegativeReals)
model2.y=Var(domain=NonNegativeReals)
#목적함수
model2.profit= Objective(
    expr=40*model2.x+30*model2.y,
    sense=maximize
)
#제약조건 
model2.demand=Constraint(expr=model2.x<=40)
model2.laborA=Constraint(expr=model2.x+model2.y<=80)
model2.laborB=Constraint(expr=2*model2.x+model2.y<=100)

SolverFactory('glpk').solve(model2).write()

print(f'최대이익= {model2.profit()} 천원/주')
print(f'x의 최적생산량 = {model2.x()} 개/주')
print(f'y의 최적생산량= {model2.y()} 개/주')
print('\n민감도 분석(Sensitivity Analysis)')
#각 제약 조건의 쌍대값이 민감도이다 
print(f'demand= {model2.dual[model2.demand]} (수요가 1 증가하면 이익은 0 증가함)')
print(f'laborA = {model2.dual[model2.laborA]} (A노동력이 1 증가하면 이익은 20 증가함)')
print(f'laborB = {model2.dual[model2.laborB]} (B 노동력이 1 증가하면 이익은 10 증가함)')
#결과값을 출력하면 A노동력을 증가시키는 것이 이익에 대한 기여도가 가장 크므로 A 노동력을 추가로 확보할 필요가 있음
str='{0:7.2f}{1:15.2f}{2:7.2f}{3:7.2f}'
#숫자들을 출력할 때 포맷을 지정하는 문자열, 각 숫자를 소수점 둘째자리까지 출력하고, 칸을 7,15,7,7칸 각각 확보한다는 뜻뜻
print('Constraint current value lslack uslack dual')
for c in[model2.demand,model2.laborA,model2.laborB]:
    print(c,str.format(c(),c.lslack(),c.uslack(),model2.dual[c]))

from pyomo.environ import *
#dictionary형 data를 이용한 모델링링
data={
    'A':{'abv':0.045,'cost':0.32},
    'B':{'abv':0.037,'cost':0.25},
    'W':{'abv':0.000, 'cost':0.05}
}
vol=100
abv=0.040
def beer_blend(vol,abv,data):
    C=data.keys()#A,B,W 키를 불러온다
    model=ConcreteModel()
    model.x=Var(C,domain=NonNegativeReals)

    model.cost=Objective(expr=sum(model.x[c]*data[c]['cost'] for c in C))
    model.vol=Constraint(expr=vol==sum(model.x[c] for c in C))
    model.abv=Constraint(expr=0==sum(model.x[c]*(data[c]['abv']-abv) for c in C))

    solver=SolverFactory('glpk')
    solver.solve(model)

    print('최적배합')
    for c in C:
        print('  ',c,':', model.x[c](),'리터')
    print()
    print('Volume = ',model.vol(),'리터')
    print('Cost = ',model.cost(),'천원')

beer_blend(vol,abv,data)