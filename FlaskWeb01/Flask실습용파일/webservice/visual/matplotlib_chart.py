# 라인차트와 산점도 그리기 - 차트 선 색상, 선 스타일, 범례 세부 설정, 이미지 저장 
import matplotlib.pyplot as plt
import numpy as np

# 다양한 색상과 선 스타일로 sin, cos 곡선을 그려주는 함수
def chartLineStyle():
    
    print("chartListStyle() 실행됨...")
    # linspace() 함수는 인수로 지정한 구간을 균등하게 나눠주는 함수
    # 아래는 0과 10 사이를 1000개의 구간으로 균등하게 나눈 1차원 배열을 반환    
    x = np.linspace(0, 10, 1000)    
    
    # linestyle : solid(-), dashed(--), dashdot(-.), dotted(:)
    plt.plot(x, np.sin(x - 0), color="blue", label="solid", linestyle="solid", linewidth=3)
    plt.plot(x, np.sin(x - 1), color="g", label="dashed", linestyle="dashed", lw=3)
    
    # 0과 1사이의 회색조
    plt.plot(x, np.sin(x - 2), color="0.75", label="gray solid", linestyle="solid")
    
    # RGB 색상 지정
    plt.plot(x, np.sin(x - 3), color="#FFDD44", label="dotted", linestyle="dotted")
    plt.plot(x, np.sin(x - 4), color=(1.0, 0.2, 0.3), label="point dashed", linestyle="-.")
    
    # -g(g-) : 녹색 실선, :b(b:) : 파란 점선, g-- : 녹색 대쉬선, b-. : 파란 1점 쇄선 
    plt.plot(x, np.sin(x - 5), "-g", label="solid green")
    
    # axis() 함수를 이용해 x와 y축의 범위나 비율에 대한 값을 지정한다.
    # equal : x축과 y축 비율을 같은 비율로 표시
    # scaled : x축과 y축 비율을 같은 비율로 표시(여백 축소)
    # on/off : 축과 눈금 등을 보이거나 숨김
    # [0, 10, -3, 3] : x축과 y축의 범위를 지정
    # plt.axis("equal")    
    plt.axis([0, 10, -1.5, 1.5])
    # plt.axis("off")
        
    # 범례의 위치, 모서리, 그림자, 컬럼 수, x, y, width, height를 지정 
    # x, y, width, height는 loc 지정에 따라서 화면에 표시되는 것이 다를 수 있다.
    plt.legend(loc="upper center", fancybox=True, shadow=True, 
               ncol=3, bbox_to_anchor=(0.01, 1.30, 0.98, -0.2))
    
    #plt.show()
    
    # 다음과 같이 차트를 화면에 띄우지 않고 이미지로 저장할 수 있다.
    # 위의 show() 메서드 호출 부분을 주석으로 처리하고 아래를 실행해야 함.
    #plt.savefig("chartLineStyle.png")
    
    return plt


# 다양한 색상과 크기로 산점도를 출력하는 함수
def multiSizeScatter():

    print("multiSizeScatter() 실행됨...")

    # 다양한 색상과 투명도를 가지는 산점도를 그리기 위해서 메르센느 트위스터(Mersenne Twister)
    # 알고리즘을 이용해 난수를 발생해 주는 프로그램용 컨테이너 생성 
    rng = np.random.RandomState(0)
    
    # 앞에서 생성한 컨테이너를 이용해 표준편차 1, 평균이 0인 정규분포에서 100개의 난수 생성
    x = rng.randn(100)
    y = rng.randn(100)
    
    # 균등분포에서 0 ~ 1 사이의 실수로된 100개의 표본을 추출
    colors = rng.rand(100)
    sizes = 1000 * rng.rand(100)
    
    # 색상, 크기, 투명도를 지정해 산점도를 출력
    plt.scatter(x, y, c=colors, s=sizes, alpha=0.3)
    
    # 색상 척도 차트에 출력
    plt.colorbar()
    #plt.show()
    
    return plt


if __name__ == "__main__":
    #plt = chartLineStyle()
    plt = multiSizeScatter()
    
    plt.show()