from pyomo.environ import *
#D: 수요, default는 LP
def setup_model(D, type_mp ='LP'):
    #상수 정의
    #시평에 따름
    TH= len(D)
    TIME= range(0,TH+1)
    #0을 뺀 이유는 목적함수, 제약식 정의 시 초기값 제외하기 위해서서
    T= range(1,TH+1)
    
    #정수계획법을 사용, 변수의 유형 정리 
    if type_mp=='IP':
       type_var=NonNegativeIntegers
    #만약 변수가 정수계획법이 아니면 0이 아닌 실수
    else:
        type_var=NonNegativeReals
    
    m=ConcreteModel()
    
    #Time 개수대로 변수를 만듬, bounds는 0이상이라는 비음 조건 설정
    #IP일 시(정수계획법) bounds를 타이트하게 잡아줄수록 계산 시간이 작아짐
    #LP의 경우는 미분법을 사용해서 큰 상관 없으나 IP는 대입법이기 때문에
    m.W=Var(TIME, domain=type_var, bounds=(0,None))
    m.H=Var(TIME, domain=type_var, bounds=(0,None))
    m.L=Var(TIME, domain=type_var, bounds=(0,None))
    m.P=Var(TIME, domain=type_var, bounds=(0,None))
    m.I=Var(TIME, domain=type_var, bounds=(0,None))
    m.S=Var(TIME, domain=type_var, bounds=(0,None))
    m.C=Var(TIME, domain=type_var, bounds=(0,None))
    m.O=Var(TIME, domain=type_var, bounds=(0,None))

    #목적함수 정의
    m.Cost= Objective(
        expr=sum(640*m.W[t]+6*m.O[t]+300*m.H[t]+500*m.L[t]
                 +2*m.I[t]+5*m.S[t]+10*m.P[t]+30*m.C[t] for t in T),
        sense= minimize
    )

    #노동력 제약조건 정의
    #def labor_rule(m, t):
    #    return m.W[t] == m.W[t-1] + m.H[t] - m.L[t]
    #m.labor = Constraint(T, rule=labor_rule)
    #위의 코드 세 줄을 rule=lambda m, 을 사용해 짧게 나타낼 수 있다.
    #제약식에서 t-1 등을 사용하기 위해서 t=0인 초기값을 제외하기 위해 Time이 아닌 T라는 범위를 설정함
    #Constraint(expr=):함수 없이 식을 바로 모델에 지정
    #Constraint([집합],rule= lambda (모델), (인덱스):): 함수를 만들어 수식이 반복되거나 조건이 달라질 때 사용용
    m.labor= Constraint(T,rule=lambda m , t:m.W[t] == m.W[t-1]+m.H[t]-m.L[t])
    #생산능력 제약조건
    m.capacity = Constraint(T, rule= lambda m, t:m.P[t]<=40*m.W[t]+0.25*m.O[t])
    #재고균형 제약조건
    m.inventory= Constraint(T,rule=lambda m, t:m.I[t] ==m.I[t-1]+m.P[t]+m.C[t]-D[t-1]-m.S[t-1]+m.S[t])
    #초과근무 제약조건
    m.overtime= Constraint(T, rule=lambda m, t: m.O[t] <= 10*m.W[t])

    #초기월 제약조건
    m.W_0=Constraint(expr=m.W[0]==80)
    m.I_0=Constraint(expr=m.I[0]==1000)
    m.S_0=Constraint(expr=m.S[0]==0)

    #마지막월 제약 조건
    m.last_inventory = Constraint(expr=m.I[TH]>=500)
    m.last_shortage = Constraint(expr=m.S[TH]==0)

    return m
#상수정의
demand=[1600,3000,3200]
#선형으로 풀기, 후에 반올림 해서 구할 수 있음(정수계획법은 시간이 걸리기 때문에에)
model=setup_model(demand,'LP')
model.pprint()

#총괄생산계획 수행(LP)
demand=[1600,3000,3200,3800,2200,2200]
#이 T는 함수 안의 값과는 상과 없는 print용 인덱스값들
T=range(0,len(demand)+1)
model=setup_model(demand,'LP')
solver=SolverFactory('glpk').solve(model).write()


print('Minimal Cost = ' , model.Cost())
print('(수요) D = ', [0]+demand)
print('(작업자) W = ', [model.W[t]() for t in T])
print('(고용) H = ',[model.H[t]() for t in T])
print('(해고)) L = ',[model.L[t]() for t in T])
print('(생산) P = ',[model.P[t]() for t in T])
print('(재고) I = ',[model.I[t]() for t in T])
print('(부재고) S = ',[model.S[t]() for t in T])
print('(외주) C = ',[model.C[t]() for t in T])
print('(잔업) O = ',[model.O[t]() for t in T])


demand=[1600,5000,3200,5800,2200,2200,6500,2300]
#이 T는 함수 안의 값과는 상과 없는 print용 인덱스값들
T=range(0,len(demand)+1)
#모델을 IP로 바꾼다(정수계획법)
model=setup_model(demand,'IP')
solver=SolverFactory('glpk').solve(model).write()

print('Minimal Cost = ' , model.Cost())
print('(수요) D = ', [0]+demand)
print('(작업자) W = ', [model.W[t]() for t in T])
print('(고용) H = ',[model.H[t]() for t in T])
print('(해고)) L = ',[model.L[t]() for t in T])
print('(생산) P = ',[model.P[t]() for t in T])
print('(재고) I = ',[model.I[t]() for t in T])
print('(부재고) S = ',[model.S[t]() for t in T])
print('(외주) C = ',[model.C[t]() for t in T])
print('(잔업) O = ',[model.O[t]() for t in T])

