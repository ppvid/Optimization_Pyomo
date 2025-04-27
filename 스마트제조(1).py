#1.1 장난감 공장의 단일 제품 생산 계획 문제 풀이

from pyomo.environ import *
#Abstract Model(추상 모델): 수식으로 표현된 모델
#Concrete Model(확정 모델): 추상 모델에 구체적인 수치를 대입한 모델
#문제를 풀 시에는 계수가 확정된 모델인 확정 모델을 사용한다.
model=ConcreteModel()
#결정변수 x를 정의 (domain=NonNegativeReals)은 비음 조건, 실수 변수 설정함. 
model.x= Var(domain=NonNegativeReals)
#Objective( expr = 결정변수x와 계수값 넣어서 목적함수를 정의, sense = 최대화/최소화 결정)
#expr(expression, 수식을 의미)
model.profit=Objective(
    expr=270*model.x-(100*model.x+50*model.x+40*(2*model.x)),
    #sense를 안 쓰면 default는 Minimize이다.
    sense = maximize
)
#Constrant(expr = 제약식 정의)
#수요 제약식
model.demand = Constraint(expr = model.x <= 40)
#가용시간 제약식 
model.laborA = Constraint(expr = model.x <= 80)
model.laborB = Constraint(expr = 2*model.x <=100)
#.pprint: 모델 안의 변수, 목적함수, 제약식을 확인할 수 있는 출력 함수수
model.pprint()
#solver=SolverFactory('glpk') : solver.를 지정한다
#glpk: GNU Linear Programming Kit
#solver.solve(model) :  풀 문제를 지정한다 
#여기서 glpk가 불러지지 않았다. 시스템 환경 변수에 들어가 환경변수, path 편집, 새로 만들기 후 설치한 경로 넣었더니 실행됨.
SolverFactory('glpk').solve(model).write()

model.profit.display() #목적함수 해 출력 
model.x.display() #결정 변수 해 출력 
#출력값에서  변수 선언 부분 Fixed는 고정값인지 변수값인지 나타냄
#fixed: False > 변수
#fixed: Ture > 상수
#변수선언부분 stale은 갱신된 값인지 아닌지를 나타냄
#stale : True > 변수의 값이 최신 계산 결과가 아님
#stale : False > 변수의 값이 갱신된 값임

#Solver Results 해석
#Number of nonzeros : 0이 아닌 계수의 수 (희소 행결(sparse matrix)일 경우 중요함)
#Solver information 해석
#status : OK > 정상적으로 계산 완료되었다.
#branch and bound : 가지치기 기법을 사용했는지 확인 가능

print(f'최대이익 = {model.profit()} 천원/주')
print(f'x의 최적 생산량 = {model.x()} 개/주')

#1.2 장난감 공장의 단일 제품 생산 계획 문제 풀이_제품 Y 추가
from pyomo.environ import *
model2 = ConcreteModel()
model2.x= Var(domain=NonNegativeReals)
model2.y= Var(domain=NonNegativeReals)

model2.profit = Objective(
    expr= 270*model2.x-(100*model2.x+50*model2.x+40*(2*model2.x)) + 210*model2.y-(90*model2.y+50*model2.y+40*model2.y),
    sense=maximize
)

model2.demand = Constraint(expr=model2.x <= 40)
model2.demand = Constraint(expr=model2.x+model2.y<=80)
model2.labor = Constraint(expr = 2*model2.x+model2.y <= 100)

SolverFactory('glpk').solve(model2).write()

print(f'최대이익= {model2.profit()} 천원/주')
print(f'x의 최적생산량 = {model2.x()} 개/주')
print(f'y의 최적생산량= {model2.y()} 개/주')


#LP모형 및 해에 대한 시각화
#라이브러리 불러오기
import matplotlib.pyplot as plt
import numpy as np
#그래프의 크기 결정
plt.figure(figsize=(6,6))#가로 세로 6인치인 정사각형 캔버스스
plt.axis([0,100,0,100])#x축을 0부터 100, y축을 0부처 100까지
plt.xlabel('X Production')
plt.ylabel('Y Production')
#제약조건의 경계선 및 범례 추가

#수요 제약, 녹색 선 표시 
plt.plot([40,40],[0,100], 'g',lw=2)#x좌표 40부터 40, 즉 x=40, y좌표는 0부터 100까지
#A노동력 제약, 붉은 선 표시 
x=np.array([0,80])#x값을 0부터 80까지
plt.plot(x,80-x,'r',lw=2)#y=80-x
#B노동력 제약, 파란선 표시 
x=np.array([0,50])
plt.plot(x,100-2*x,'b', lw=2)
#범례 표시
plt.legend(['Labor A Constraint','Labor B Constraint','Demand Constraint'])

#fill 함수
#fill_between: 두 수평방향의 곡선 사이를 채움
#fill_betweenx(): 두 수직 방향의 곡선 사이를 채움
#fill(): 다각형 영역을 채움

#제약조건
#A노동력 제약 영역 채우기
#(0,80) → (80,0) → (100,0) 이 세 점을 따라 그린 아래쪽 선과,
#(0,100) → (80,100) → (100,100) 이 윗선을 기준으로 사이 영역을 채움
#제약식의 꼭짓점(x,y절편이나 경계값)을 직접 넣어 색을 칠한 것
plt.fill_between(
    [0,80,100],#x좌표 세개
    [80,0,0],#아래쪽 y좌표(Lower bound)
    [100,100,100],#위쪽 y 좌표(upper bound)
    color='r',
    alpha=0.15#투명도(15%불투명)
    ) 
#B노동력 제약 영역 채우기
plt.fill_between(
    [0,50,100],[100,0,0],[100,100,100],
    color='b',
    alpha=0.15)
#수요 제약 영역 채우기
plt.fill_between(
    [40,100],[0,0],[100,100],
    color='g',
    alpha=0.15)

#목적함수
#이익의 크기에 따른 등고선 표시
#목적함수 정리: z=40x+30y
x=np.array([0,100])
for z in np.linspace(0,3600,10): #z값(목적함수 값)은 0-3600 사이 10가지 균등한 값값
    y=(z-40*x)/30
    plt.plot(x,y,'y--') #'y--': 점선으로 그래프를 그린다

#화살표 추가
arrowprops=dict(shrink=.3,width=.5, headwidth=5)
#shrink: 화살표의 길이 조절, width: 화살표 몸통 두께, headwidth: 화살촉 두께께
plt.plot(20,60,'r.', ms=20) #점을 찍는 곳 지정정
#ms: 마커 크기
plt.annotate(
    'Mixed Product Strategy',
    xy=(20,60), #화살표가 가르키는 위치
    xytext=(50,70), #텍스트를 표시할 위치
    arrowprops=arrowprops
)
plt.plot(0,80,'b.',ms=20)
plt.annotate(
    'Y Only',
    xy=(0,80),
    xytext=(20,90),
    arrowprops=arrowprops
)

plt.plot(40,0,'b.',ms=20)
plt.annotate(
    'X Only',
    xy=(40,0),
    xytext=(70,20),
    arrowprops=arrowprops
)
plt.text(4,23,'Increasing Profit')
plt.annotate(
    '',
    xy=(20,15),
    xytext=(0,0),
    arrowprops=arrowprops
)

plt.show()

