import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Dash 앱 초기화
app = dash.Dash(__name__)

# 데이터 로드 및 전처리 (예시)
data = pd.read_csv('/Users/hajun/Desktop/대쉬보드 프로젝트/P-4 서울시 부동산 실거래가 정보/서울시 부동산 실거래가 정보.csv', encoding="cp949")  # 데이터 파일 경로 지정
data = data.loc[:, [
    "접수연도", "자치구명", "계약일", "물건금액(만원)", "건물면적(㎡)", "토지면적(㎡)", "층", "건축년도", "건물용도"]]
data.columns = ["접수연도", "서울시 구", "계약일", "건물금액(만원)", "건물면적(㎡)", "토지면적(㎡)", "층", "건축년도", "건물용도"]

# 건물금액(만원)을 억(10,000) 단위로 변환하는 함수
def convert_to_억(amount):
    converted_amount = amount / 100000  # 10,000으로 나누어 억 단위로 변환
    return converted_amount

# 건물 면적(㎡)을 평(1 평 = 3.30578 제곱 미터)으로 변환하는 함수
def convert_to_평(area):
    converted_area = area / 33
    return converted_area

# 데이터프레임의 '건물금액(만원)' 열에 함수를 적용하여 억 단위로 변환한 값을 새로운 열에 추가
data['건물금액(억원)'] = data['건물금액(만원)'].apply(convert_to_억)

# 데이터프레임의 '건물면적(㎡)' 열에 함수를 적용하여 평 단위로 변환한 값을 새로운 열에 추가
data['건물면적(평)'] = data['건물면적(㎡)'].apply(convert_to_평)

groups = data["서울시 구"].unique()

# 레이아웃 정의
app.layout = html.Div(children=[
    html.H1(
        children="서울시 아파트 거래가",
        style={"textAlign": "center"}
    ),
    html.H4(
        children="구별 건물 면적에 따른 아파트 가격 분포",
    ),
    dcc.Dropdown(
        id="group",
        options=[{'label': group, 'value': group} for group in groups],
        value=groups[0]
    ),
    dcc.Graph(
        id="graph",
    ),
], style={"width": "90%", "margin": "auto"})

# 콜백 정의
@app.callback(
    Output(component_id="graph", component_property="figure"),
    Input(component_id="group", component_property="value"),
)
def update_graph(group):
    # 사용자가 선택한 서울시 구가 포함된 데이터를 필터링
    selected_data = data.loc[data["서울시 구"] == group]

    # 서울시 구별로 건물 면적에 따른 아파트 가격 분포를 산포도 그래프로 시각화
    fig = px.scatter(
        selected_data, x="건물면적(평)", y="건물금액(억원)",
        title=f"{group} 구 건물 면적에 따른 아파트 가격 분포",
        labels={"건물면적(평)": "건물 면적(평)", "건물금액(억원)": "아파트 가격(억원)"},
        height=500,  # 그래프 높이 설정
        hover_name="건축년도",  # Hover 기능을 통해 보여줄 정보 선택
    )
    return fig

# 앱 실행
if __name__ == '__main__':
    app.run_server(debug=True)
