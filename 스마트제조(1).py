from pyomo.environ import *
#Abstract Model(추상 모델): 수식으로 표현된 모델
#Concrete Model(확정 모델): 추상 모델에 구체적인 수치를 대입한 모델
#문제를 풀 시에는 계수가 확정된 모델인 확정 모델을 사용한다.
model=ConcreteModel()
#결정변수 x를 정의 (domain=NonNegativeReals)은 비음 조건을 나타냄냄
model.x= Var(domain=NonNegativeReals)
#Objective( expr = 결정변수x와 계수값 넣어서 목적함수를 정의, sense = 최대화/최소화 결정)
#expr(expression, 수식을 의미)
model.profit=Objective(
    expr=270*model.x-(100*model.x+50*model.x+40*(2*model.x)),
    #sense를 안 쓰면 default는 Minimize이다.
    sense = maximize
)
#Constrant(expr = 제약식 정의)
model.demand = Constraint(expr = model.x <= 40)
model.laborA = Constraint(expr = model.x <= 80)
model.laborB = Constraint(expr = 2*model.x <=100)
#.pprint: 모델 안의 변수, 목적함수, 제약식을 확인할 수 있는 출력 함수수
model.pprint()
#solver=SolverFactory('glpk') : solver.를 지정한다
#glpk: GNU Linear Programming Kit
#solver.solve(model) :  풀 문제를 지정한다 
SolverFactory('glpk').solve(model).write()

model.profit.display() #목적함수 해 출력 
model.x.display() #결정 변수 해 출력 