import plotly.express as px
from dash import Dash, dcc, html

import pandas as pd

app = Dash(__name__)

data = pd.read_csv("/Users/hajun/Desktop/대쉬보드 프로젝트/P2 - 공공자전거 대여소 정보(23.06월 기준)/공공자전거 대여소 정보(23.06월 기준).csv", encoding="cp949")
data["총 거치대수"] = data["LCD 거치 대수"] + data["QR 거치 대수"]
grouped_data = data.groupby("소재지(위치)")["총 거치대수"].sum().reset_index()
data = data.loc[:, [
    "대여소 번호", "보관소(대여소)명", "소재지(위치)", "상세주소", "설치 시기", "총 거치대수", "운영방식"]]
data.columns = ["대여소 번호", "보관소명", "시군구", "상세주소", "설치시기", "총 거치대 수", "운영방식"]

# "시군구"를 가나다 순으로 정렬
data = data.sort_values(by="시군구")

# 그래프 정의
fig = px.bar(
    data, x="시군구", y="총 거치대 수", 
    labels={"총 거치대 수": "총 거치대 수"},  # 축 레이블 변경
    title="시군구별 총 거치대 수",  # 그래프 제목 추가
    color_discrete_sequence=["blue"],  # 바 색상 변경
    height=500  # 그래프 높이 설정
)

# 그래프 레이아웃 및 스타일 변경
fig.update_layout(
    xaxis_title="시군구",  # x축 제목
    yaxis_title="총 거치대 수",  # y축 제목
    showlegend=False,  # 범례 숨김
    margin=dict(l=40, r=40, t=60, b=40),  # 그래프 여백 설정
    plot_bgcolor="white",  # 그래프 배경색
)
app.layout = html.Div(children=[
    html.H1(
        children="공공자전거 대여소 정보(23.06월 기준)",
        style={"textAlign": "center"}
    ),
    html.H4(
        children="시군구별 총 거치대 수", 
    ),
    dcc.Graph(
        id="graph",
        figure=fig
    ),
], style={"width": "90%", "margin": "auto"})

if __name__ == '__main__':
    app.run_server(debug=True)