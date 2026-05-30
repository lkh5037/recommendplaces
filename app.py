import streamlit as st
import pandas as pd

st.title("강원생활도우미앱 3.0")


def load_data(uploaded_file):
    place_df = pd.read_excel(uploaded_file, sheet_name="장소정보")
    recommend_df = pd.read_excel(uploaded_file, sheet_name="추천정보")
    return place_df, recommend_df


def join_data(place_df, recommend_df):
    merged_df = pd.merge(
        recommend_df,
        place_df,
        on="place_id",
        how="left"
    )

    return merged_df


def show_joined_data(df):
    st.subheader("조인된 데이터")
    st.dataframe(df)

def search_recommendations(df):
    st.subheader("추천 장소 검색")

    selected_region = st.selectbox(
        "지역 선택",
        df["지역"].unique()
    )

    selected_purpose = st.selectbox(
        "추천목적 선택",
        df["추천목적"].unique()
    )

    selected_situation = st.selectbox(
        "추천상황 선택",
        df["추천상황"].unique()
    )

    selected_target = st.selectbox(
        "추천대상 선택",
        df["추천대상"].unique()
    )

    selected_budget = st.number_input(
        "최대 예산",
        min_value=0,
        value=10000,
        step=1000
    )

    result = df[
        (df["지역"] == selected_region) &
        (df["추천목적"] == selected_purpose) &
        (df["추천상황"] == selected_situation) &
        (df["추천대상"] == selected_target) &
        (df["예산"] <= selected_budget)
    ]

    st.subheader("검색 결과")

    if len(result) > 0:
        st.dataframe(result)
    else:
        st.warning("조건에 맞는 추천 장소가 없습니다.")

uploaded_file = st.file_uploader(
    "엑셀 파일을 업로드하세요",
    type=["xlsx"]
)

if uploaded_file is not None:
    place_df, recommend_df = load_data(uploaded_file)
    merged_df = join_data(place_df, recommend_df)
    show_joined_data(merged_df)
import streamlit as st
import pandas as pd

st.title("강원생활도우미앱 3.0")


def load_data(uploaded_file):
    place_df = pd.read_excel(uploaded_file, sheet_name="장소정보")
    recommend_df = pd.read_excel(uploaded_file, sheet_name="추천정보")
    return place_df, recommend_df


def join_data(place_df, recommend_df):
    merged_df = pd.merge(
        recommend_df,
        place_df,
        on="place_id",
        how="left"
    )

    return merged_df


def show_original_data(place_df, recommend_df):
    st.subheader("장소정보 시트")
    st.dataframe(place_df)

    st.subheader("추천정보 시트")
    st.dataframe(recommend_df)


def show_joined_data(df):
    st.subheader("조인된 데이터")
    st.dataframe(df)


def search_recommendations(df):
    st.subheader("추천 장소 검색")

    selected_region = st.selectbox("지역 선택", df["지역"].unique())
    selected_purpose = st.selectbox("추천목적 선택", df["추천목적"].unique())
    selected_situation = st.selectbox("추천상황 선택", df["추천상황"].unique())
    selected_target = st.selectbox("추천대상 선택", df["추천대상"].unique())

    selected_budget = st.number_input(
        "최대 예산",
        min_value=0,
        value=10000,
        step=1000
    )

    result = df[
        (df["지역"] == selected_region) &
        (df["추천목적"] == selected_purpose) &
        (df["추천상황"] == selected_situation) &
        (df["추천대상"] == selected_target) &
        (df["예산"] <= selected_budget)
    ]

    st.subheader("검색 결과")

    if len(result) > 0:
        st.dataframe(result)
    else:
        st.warning("조건에 맞는 추천 장소가 없습니다.")


def show_chart(df):
    st.subheader("데이터 시각화")

    chart_option = st.selectbox(
        "시각화 기준 선택",
        ["지역", "유형", "추천목적", "추천상황", "추천대상", "예약필요"]
    )

    chart_data = df[chart_option].value_counts()

    st.bar_chart(chart_data)


uploaded_file = st.file_uploader(
    "엑셀 파일을 업로드하세요",
    type=["xlsx"]
)

if uploaded_file is not None:
    place_df, recommend_df = load_data(uploaded_file)
    merged_df = join_data(place_df, recommend_df)

    menu = st.sidebar.radio(
        "메뉴 선택",
        ["원본 데이터 보기", "조인 데이터 보기", "추천 검색", "데이터 시각화"]
    )

    if menu == "원본 데이터 보기":
        show_original_data(place_df, recommend_df)

    elif menu == "조인 데이터 보기":
        show_joined_data(merged_df)

    elif menu == "추천 검색":
        search_recommendations(merged_df)

    elif menu == "데이터 시각화":
        show_chart(merged_df)
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

root = tk.Tk()
root.title("강원생활도우미앱 3.0")
root.geometry("700x500")
root.configure(bg="#f5f5f5")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#f5f5f5", font=("Malgun Gothic", 11))
style.configure("Title.TLabel", background="#f5f5f5", font=("Malgun Gothic", 18, "bold"))
style.configure("SubTitle.TLabel", background="#f5f5f5", font=("Malgun Gothic", 14, "bold"))
style.configure("TCombobox", font=("Malgun Gothic", 10))

main_frame = ttk.Frame(root, padding=30, style="TLabel")
main_frame.pack(fill=tk.BOTH, expand=True)

title_label = ttk.Label(main_frame, text="강원생활도우미앱 3.0", style="Title.TLabel")
title_label.pack(anchor="w", pady=(0, 15))

excel_label = ttk.Label(main_frame, text="엑셀 파일")
excel_label.pack(anchor="w", pady=(0, 5))

upload_frame = tk.Frame(main_frame, bg="#e0e0e0", height=60, bd=1, relief="solid")
upload_frame.pack(fill=tk.X, pady=(0, 25))
upload_frame.pack_propagate(False)

file_btn = tk.Button(upload_frame, text="📁", font=("Malgun Gothic", 14), bg="#333333", fg="white", bd=0, width=4, command=lambda: filedialog.askopenfilename())
file_btn.pack(side=tk.LEFT, padx=10, pady=10)

recommend_label = ttk.Label(main_frame, text="추천", style="SubTitle.TLabel")
recommend_label.pack(anchor="w", pady=(0, 15))

def create_dropdown(parent, label_text, default_value):
    label = ttk.Label(parent, text=label_text)
    label.pack(anchor="w", pady=(5, 2))
    
    combo_border = tk.Frame(parent, bg="#cccccc", bd=1)
    combo_border.pack(fill=tk.X, pady=(0, 10))
    
    combo = ttk.Combobox(combo_border, values=[default_value, "옵션 2", "옵션 3"], state="readonly")
    combo.set(default_value)
    combo.pack(fill=tk.X, ipady=4)
    
    combo.configure(background="white")

create_dropdown(main_frame, "지역 선택", "강릉")
create_dropdown(main_frame, "추천목적 선택", "공부")
create_dropdown(main_frame, "추천상황 선택", "비오는날")
