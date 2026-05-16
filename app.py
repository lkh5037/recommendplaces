import streamlit as st

if "places" not in st.session_state:
    st.session_state.places = [
        {"이름":"강릉 경포해변","실내여부":"실외","가격대":0,"만족도":4.5,"운영시작":6,"운영종료":22,"혼잡도":14000},
        {"이름":"춘천 레고랜드","실내여부":"실외","가격대":45000,"만족도":4.4,"운영시작":10,"운영종료":18,"혼잡도":7000},
        {"이름":"강릉 중앙시장","실내여부":"실내","가격대":12000,"만족도":4.2,"운영시작":8,"운영종료":23,"혼잡도":16000},
        {"이름":"오죽헌","실내여부":"실내","가격대":3000,"만족도":4.6,"운영시작":9,"운영종료":18,"혼잡도":5000}
    ]

def place_output(result):
    if result == []:
        st.write("조건에 맞는 장소가 없습니다")
    else:
        for place in result:
            for key in place:
                st.write(key, " : ", place[key])
            st.write("---")

def place_search_by_category(place_list,key,value):
    result = []
    for place in place_list:
        if (place[key] == value or value == "전부"):
            result.append(place)
    return result

def place_search_by_number(place_list,key,value,mode):
    result = []
    for place in place_list:
        if mode == "전부" or (mode == "기준 이상" and place[key] >= value) or (mode == "기준 이하" and place[key] <= value):
            result.append(place)
    return result

def place_add(place_list,name,indoor,price,score,start,end,crowd):
    new_place = {
        "이름": name,
        "실내여부": indoor,
        "가격대": price,
        "만족도": score,
        "운영시작": start,
        "운영종료": end,
        "혼잡도": crowd
    }
    place_list.append(new_place)

def place_search_by_number_total(result_input,key,min,jump,max):
    mode = st.radio(key + " 검색 기준을 선택하세요", ["전부", "기준 이상", "기준 이하"])
    if mode != "전부":
        if max == 0:
            value = st.number_input(key + "을(를) 입력하세요",min_value=min, step=jump)
        else:
            value = st.number_input(key + "을(를) 입력하세요",min_value=min, step=jump,max_value=max)
        result = place_search_by_number(result_input,key,value,mode)
        return result
    else:
        return result_input

st.title("강원생활도우미앱")

menu = st.selectbox("기능을 선택하세요", ["전체 보기", "추천 받기", "장소 추가"])

if menu == "전체 보기":
    st.subheader("전체 결과")
    place_output(st.session_state.places)

elif menu == "추천 받기":
    indoor = st.selectbox("실내여부를 선택하세요", ["전부", "실내", "실외"])
    result = place_search_by_category(st.session_state.places,"실내여부",indoor)
    result = place_search_by_number_total(result,"가격대",0,1000,0)
    result = place_search_by_number_total(result,"만족도",0.0,0.1,5.0)

    time_mode = st.radio("방문 시간 검색 방식을 선택하세요", ["전부", "선택"])

    if time_mode != "전부":
        time = st.number_input("방문 시각을 입력하세요",min_value=0, step=1,max_value=24)
        result = place_search_by_number(result,"운영시작",time,"기준 이하")
        result = place_search_by_number(result,"운영종료",time,"기준 이상")

    result = place_search_by_number_total(result,"혼잡도",0,1000,0)

    st.subheader("추천 결과")
    place_output(result)

elif menu == "장소 추가":
    name = st.text_input("장소 이름을 입력하세요")
    indoor = st.selectbox("실내/실외를 선택하세요", ["실내", "실외"])
    price = st.number_input("새 장소의 가격대를 입력하세요", min_value=0, step=1000)
    score = st.number_input("새 장소의 만족도를 입력하세요", min_value=0.0, step=0.1, max_value=5.0)
    start = st.number_input("새 장소의 운영시작 시간을 입력하세요", min_value=0, step=1, max_value=24)
    end = st.number_input("새 장소의 운영종료 시간을 입력하세요", min_value=0, step=1, max_value=24)
    crowd = st.number_input("새 장소의 혼잡도를 입력하세요", min_value=0, step=1000)

    if st.button("장소 추가"):
        place_add(st.session_state.places,name,indoor,price,score,start,end,crowd)
        st.success("새 장소가 추가되었습니다")
