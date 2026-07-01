import streamlit as st
import datetime

def generate_advanced_densuke_dates(start_date, end_date, selected_weekdays, time_slots, excluded_dates):
    """
    指定した期間，曜日，時間帯，および除外日の条件に合わせて，伝助用の日付リストを生成する関数．

    Parameters:
        start_date (datetime.date): 開始日
        end_date (datetime.date): 終了日
        selected_weekdays (list of int): 出力対象とする曜日のインデックスリスト（0:月 〜 6:日）
        time_slots (list of str): 各日付に追加する時間帯文字列のリスト．空の場合は時間帯なし．
        excluded_dates (list of datetime.date): 候補から除外する特定の日付のリスト．
        
    Returns:
        list: 条件に合わせて生成されたスケジュール文字列のリスト
    """
    weekdays_str = ['月', '火', '水', '木', '金', '土', '日']
    date_list = []
    
    current_date = start_date
    while current_date <= end_date:
        # 除外日に指定されておらず，かつ選択された曜日に含まれているかチェック
        if current_date not in excluded_dates and current_date.weekday() in selected_weekdays:
            date_str = f"{current_date.month}/{current_date.day}({weekdays_str[current_date.weekday()]})"
            
            # 時間帯の指定がある場合は，日付と時間を掛け合わせて出力
            if time_slots:
                for slot in time_slots:
                    if slot.strip(): # 空白行を無視
                        date_list.append(f"{date_str} {slot.strip()}")
            else:
                # 時間帯の指定がない場合は日付のみ出力
                date_list.append(date_str)
                
        current_date += datetime.timedelta(days=1)
        
    return date_list

# ==========================================
# UI構築部分
# ==========================================
st.set_page_config(page_title="伝助ジェネレータ", page_icon="📅", layout="centered")

st.title("📅 伝助 日程ジェネレータ")
st.write("伝助用の候補日リストを，指定した条件で自動生成します．")

st.divider()

# --- 1. 期間の指定 ---
st.subheader("1. 期間を指定")
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("開始日", datetime.date.today())
with col2:
    default_end = datetime.date.today() + datetime.timedelta(days=14)
    end_date = st.date_input("終了日", default_end)

# --- 2. 曜日の絞り込み ---
st.subheader("2. 曜日を絞り込む")
st.write("出力したい曜日にチェックを入れてください．")
weekdays_label = ['月', '火', '水', '木', '金', '土', '日']
cols = st.columns(7)
selected_weekdays = []

# 各曜日のチェックボックスを横に並べる
for i, col in enumerate(cols):
    with col:
        # デフォルトは全てチェック入り
        if st.checkbox(weekdays_label[i], value=True):
            selected_weekdays.append(i)

# --- 3. 除外日の指定 ---
st.subheader("3. 特定の日付を除外する")
st.write("候補から外したい特定の日にち（すでに予定が埋まっている日など）があれば選択してください．")

# 開始日から終了日までの日付リストを生成
date_options = []
temp_date = start_date
while temp_date <= end_date:
    date_options.append(temp_date)
    temp_date += datetime.timedelta(days=1)

# セレクトボックスで表示するためのフォーマット関数
def format_date(d):
    weekdays = ['月', '火', '水', '木', '金', '土', '日']
    return f"{d.month}/{d.day}({weekdays[d.weekday()]})"

excluded_dates = st.multiselect("除外する日付を選択:", options=date_options, format_func=format_date)

# --- 4. 時間帯の追加（オプション） ---
st.subheader("4. 時間帯を追加 (オプション)")
st.write("1日の中で複数の時間を指定したい場合は，改行して入力してください．不要な場合は空欄のままでOKです．")
time_input = st.text_area(
    "入力例: 18:00〜 / 20:00〜", 
    placeholder="18:00〜\n20:00〜",
    height=100
)

st.divider()

# --- 5. 生成ボタンと結果表示 ---
if st.button("✨ 日程リストを生成する", type="primary", use_container_width=True):
    if start_date > end_date:
        st.error("※開始日は終了日より前の日付を指定してください．")
    elif not selected_weekdays:
        st.error("※少なくとも1つの曜日を選択してください．")
    else:
        # 入力された時間帯テキストを改行で分割してリスト化
        time_slots = [t for t in time_input.split('\n') if t.strip()]
        
        # 関数を呼び出して結果を生成
        result_dates = generate_advanced_densuke_dates(start_date, end_date, selected_weekdays, time_slots, excluded_dates)
        result_text = "\n".join(result_dates)
        
        if result_text:
            st.success(f"生成完了！ ({len(result_dates)}件の候補日) 右上のボタンからコピーして伝助に貼り付けてください．")
            st.code(result_text, language="text")
        else:
            st.warning("指定された期間内に，選択された曜日の日付がありません．")
