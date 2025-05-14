import streamlit as st
import pandas as pd
import altair as alt

# CSV 파일 불러오기 및 정리
df = pd.read_csv(r"C:\streamlit\보일러_용량별_지역별_에너지사용현황_20250512190731.csv")
df.columns = df.iloc[0]
df = df.drop(index=0).reset_index(drop=True)
df_melted = df.melt(id_vars=['용량별(1)', '항목'], var_name='지역', value_name='값')
df_melted['값'] = pd.to_numeric(df_melted['값'], errors='coerce')
df_pivot = df_melted.pivot_table(index=['지역', '용량별(1)'], columns='항목', values='값').reset_index()
df_pivot.columns.name = None

# Streamlit UI
st.title("지역별 보일러 용량에 따른 에너지 사용현황 시각화")

region = st.selectbox("지역을 선택하세요", sorted(df_pivot['지역'].unique()))
capacity = st.selectbox("보일러 용량을 선택하세요", sorted(df_pivot['용량별(1)'].unique()))

filtered = df_pivot[df_pivot['지역'] == region]
single_row = filtered[filtered['용량별(1)'] == capacity]

# 첫 번째 차트: 선택한 지역의 모든 용량별 대수 및 사용량
bar_data = filtered[['용량별(1)', '대수 (대)', '사용량 (toe)']].melt(id_vars='용량별(1)',
                                                         var_name='항목',
                                                         value_name='값')
bar_chart = alt.Chart(bar_data).mark_bar().encode(
    x='용량별(1):O',
    y='값:Q',
    color='항목:N',
    tooltip=['용량별(1)', '항목', '값']
).properties(
    width=600,
    height=400,
    title=f"{region} 지역의 보일러 용량별 현황"
)
st.altair_chart(bar_chart, use_container_width=True)

# 두 번째 차트: 선택한 지역+용량의 상세 정보
if not single_row.empty:
    st.subheader(f"{region} - {capacity} 상세정보")
    st.metric("대수 (대)", int(single_row['대수 (대)'].values[0]))
    st.metric("사용량 (toe)", f"{int(single_row['사용량 (toe)'].values[0]):,}")
else:
    st.warning("선택한 조합에 대한 데이터가 없습니다.")
