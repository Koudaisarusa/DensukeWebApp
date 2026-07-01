import streamlit as st
import datetime

def generate_densuke_dates(start_date, end_date):
    """
    指定した期間の日付を伝助用のフォーマットで出力する関数．
    """
    weekdays = ['月', '火', '水', '木', '金', '土', '日']
    date_list = []
    
    current_date = start_date
    while current_date <= end_date:
        date_str = f"{current_date.month}/{current_date.day}({weekdays[current_date.weekday()]})"
        date_list.append(date_str)
        current_date += datetime.timedelta(days=1)
        
    return date_list

# ページの設定
st.set_page_config(page_title="伝助ジェネレータ", page_icon="📅")

# タイトルと説明
st.title("伝助 日程ジェネレータ")
st.write("指定した期間の日付リスト（M/D(曜日)）を自動作成します．")

# 入力フォーム（2列に並べる）
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("開始日", datetime.date.today())
with col2:
    # 終了日の初期値は2週間後に設定
    default_end = datetime.date.today() + datetime.timedelta(days=14)
    end_date = st.date_input("終了日", default_end)

# 実行ロジック
if start_date > end_date:
    st.error("※開始日は終了日より前の日付を指定してください．")
else:
    if st.button("日付リストを生成", type="primary"):
        # 日付リストを生成
        result_dates = generate_densuke_dates(start_date, end_date)
        result_text = "\n".join(result_dates)
        
        # 結果の表示（コピーボタン付きのコードブロック）
        st.success("生成完了！以下のテキストをコピーして伝助に貼り付けてください．")
        st.code(result_text, language="text")