import streamlit as st
import pandas as pd
import requests
import xmltodict

def load_data():
    # CSV 파일 로드
    return pd.read_csv('C:/python.lee/naverblog/sicode.csv')

def get_real_estate_data(sigungu_code, yyyymm):
    # API 요청 준비
    service_key = "pII%2BrqHs3TfQwKgsYX%2Fx7fJuQiml0eppEVSKFnXO%2BJ4DgrCY53X9tKkMZaS4%2FbOTcfYEOfq3WtZoeONMjs3nPw%3D%3D"
    url = f"http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev?serviceKey={service_key}&pageNo=1&numOfRows=30&LAWD_CD={sigungu_code}&DEAL_YMD={yyyymm}"
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        data_dict = xmltodict.parse(content)
        items = data_dict['response']['body']['items'].get('item', [])
        if isinstance(items, dict):  # 단일 항목이면 리스트로 만들기
            items = [items]
        return pd.DataFrame(items)
    else:
        return None

# 페이지 설정
st.set_page_config(layout="wide",  # 'wide'로 설정하여 화면 전체 너비 사용
    page_title="부동산 거래 정보 조회",  # 탭 타이틀
    page_icon="🏠",  # 탭 아이콘
)

def main():
    st.title('부동산 거래 정보 조회')
    
    # CSV 파일 로드
    locations_df = load_data()
    
    # 사용자 입력
    user_input = st.text_input("법정동명을 입력하세요: ").strip()
    yyyymm = st.text_input("조회할 년월 입력 (YYYYMM): ")

    if st.button("조회"):
        if user_input and yyyymm:
            # 입력받은 법정동명을 이용해 해당 법정동코드 찾기
            matching_rows = locations_df[locations_df['법정동주소'].str.contains(user_input, case=False, na=False)]
            if not matching_rows.empty:
                sigungu_code = matching_rows['법정동코드'].iloc[0]  # 첫 번째 일치하는 코드 사용
                sigungu_code = int(sigungu_code)  # 정수로 변환
                df = get_real_estate_data(sigungu_code, yyyymm)
                if df is not None:
                    st.write(df)
                else:
                    st.error("API 요청 실패")
            else:
                st.error("입력한 법정동명에 해당하는 코드를 찾을 수 없습니다.")

if __name__ == '__main__':
    main()