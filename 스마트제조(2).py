from pyomo.environ import *
model=ConcreteModel()
model.x=Var(domain=NonNegativeReals)
#최적화 모델 함수로 만듬(범용화 위해)
def setup_model(D,type_mp='LP')
    TH=len(D)#시평
    #0시간-TH
    TIME=range(0,TH+1)

    T=range(1,TH+1)
    #변수의 유형 정의
    if type_mp=='IP':
        type_var=NonNegativeReals
    else:
        type_var=NonNegativeReals
    #ConcreteModel 생성성
    m=ConcreteModel()
