import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import matplotlib.font_manager as fm

# =================================================================
# 0. 環境配置與字體設置
# =================================================================

st.set_page_config(layout="wide")
st.title("🏐 SV.LEAGUE 男排球員個人數據與歷史分析")
st.markdown("---")

# --- 中文字體設置 ---
font_path = './fonts/NotoSansCJKtc-Regular.otf' 
try:
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = 'Noto Sans CJK TC' 
    plt.rcParams['axes.unicode_minus'] = False 
except Exception:
    st.sidebar.warning("⚠️ 找不到指定字體。圖表中文可能顯示為方塊。")
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial'] 
    plt.rcParams['axes.unicode_minus'] = False


# =================================================================
# 1. 數據定義與載入 (模擬數據)
# =================================================================

@st.cache_data
def load_data():
    # --- 1.1 球員個人數據 (已修正，包含舉球員的總舉球次數) ---
    data = {
        '姓名': ['Lopez, M.', 'Muserskiy, D.', 'Nimir, A.', '高橋藍', '西田有志', '蔡沛彰', '柳田将洋', '水町泰杜', '清水邦広', '関田誠大', '古賀太一郎', '深津英臣', '大宅真樹', '山内晶大'],
        '位置': ['OH', 'OP', 'OP', 'OH', 'OP', 'MB', 'OH', 'OP', 'OP', 'S', 'L', 'S', 'S', 'MB'],
        '隊伍': [
            'OSAKA BLUTEON', 'SUNTORY SUNBIRDS', 'WOLFDOGS NAGOYA', 'SUNTORY SUNBIRDS', 'PANTHERS', 'NIPPON STEEL SAKAI', 'TOKYO GREAT BEARS', 'WOLFDOGS NAGOYA', 'PANTHERS', 'JTEKT STINGS',
            'TOKYO GREAT BEARS', 'WOLFDOGS NAGOYA', 'JTEKT STINGS', 'PANTHERS'
        ],
        '總得分': [550, 600, 580, 450, 400, 300, 350, 420, 380, 150, 0, 120, 140, 280],
        '總進攻次數': [950, 1000, 980, 750, 700, 450, 720, 780, 700, 100, 0, 90, 110, 400],
        '成功扣球數': [500, 520, 490, 380, 350, 240, 300, 380, 320, 80, 0, 70, 80, 220],
        '接發球總次數': [450, 50, 40, 600, 30, 5, 550, 80, 20, 10, 800, 5, 8, 5],
        '接發球成功次數': [250, 25, 15, 300, 10, 0, 280, 40, 5, 5, 450, 2, 3, 0],
        '發球得分': [30, 40, 50, 25, 35, 10, 20, 30, 20, 10, 0, 25, 30, 15],
        '攔網得分': [20, 40, 40, 45, 15, 50, 30, 10, 25, 50, 0, 15, 20, 45],
        # 舉球員核心數據（S位置在索引 9, 11, 12）
        '總舉球次數': [0, 0, 0, 0, 0, 0, 0, 0, 0, 2000, 0, 2500, 2200, 0],
        '舉球成功次數': [0, 0, 0, 0, 0, 0, 0, 0, 0, 850, 0, 1100, 950, 0],
        # 體型與紀錄數據
        '身高 (cm)': [190, 218, 200, 188, 186, 195, 188, 187, 190, 182, 170, 183, 178, 201],
        '體重 (kg)': [85, 105, 95, 78, 80, 88, 77, 75, 82, 75, 68, 77, 73, 90],
        '獲獎紀錄': [
            'V. MVP, Best 6', 'V. MVP, Best 6', 'V. MVP, Best Server', 'Best 6, 最佳接發', 
            'V. Score King', '亞洲錦標賽最佳MB', '奧運代表', '無', '天皇杯MVP', 'V. Best Setter', 
            '亞洲最佳自由球員', 'V. Best Setter', '無', 'V. Best 6, 攔網王'
        ]
    }
    df = pd.DataFrame(data)

    # --- 1.2 模擬歷年球隊比賽成績 (歷史數據) ---
    historical_data = {
        '年份': [2022, 2023, 2024, 2022, 2023, 2024, 2022, 2023, 2024],
        '隊伍': ['SUNTORY SUNBIRDS', 'SUNTORY SUNBIRDS', 'SUNTORY SUNBIRDS', 'WOLFDOGS NAGOYA', 'WOLFDOGS NAGOYA', 'WOLFDOGS NAGOYA', 'PANTHERS', 'PANTHERS', 'PANTHERS'],
        '聯賽排名': [1, 3, 2, 2, 1, 3, 4, 2, 1],
        '總決賽結果': ['冠軍', '四強', '亞軍', '亞軍', '冠軍', '四強', '無緣', '亞軍', '冠軍']
    }
    df_history = pd.DataFrame(historical_data)

    # --- 1.3 指標計算 (新增舉球效率) ---
    df['進攻決定率'] = np.where(df['總進攻次數'] > 0, (df['成功扣球數'] / df['總進攻次數']) * 100, 0)
    df['接發球成功率'] = np.where(df['接發球總次數'] > 0, (df['接發球成功次數'] / df['接發球總次數']) * 100, 0)
    df['舉球效率'] = np.where(df['總舉球次數'] > 0, (df['舉球成功次數'] / df['總舉球次數']) * 100, 0)
    df['扣球得分'] = df['總得分'] - df['發球得分'] - df['攔網得分']
    
    return df, df_history

df, df_history = load_data()
all_teams = sorted(df['隊伍'].unique())

# =================================================================
# 2. 互動式篩選器 (側邊欄)
# =================================================================

st.sidebar.header("🎯 選擇球員")

# 步驟 1: 選擇隊伍
selected_team = st.sidebar.selectbox(
    "1. 選擇服務隊伍:",
    options=[''] + all_teams,
    index=0
)

# 步驟 2: 選擇球員 (只有選了隊伍才顯示)
selected_player_name = ''
if selected_team:
    players_in_team = df[df['隊伍'] == selected_team]['姓名'].unique()
    selected_player_name = st.sidebar.selectbox(
        "2. 選擇球員:",
        options=players_in_team
    )

st.sidebar.markdown("---")


# =================================================================
# 3. 主頁面：球員個人檔案顯示
# =================================================================

if not selected_player_name:
    st.info("請在側邊欄選擇一支隊伍和一位球員，以查看個人分析報告。")
else:
    # 獲取選定球員的數據
    player_data = df[df['姓名'] == selected_player_name].iloc[0]
    
    st.header(f"👤 {selected_player_name} - 個人表現報告")
    st.subheader(f"目前服務隊伍：{player_data['隊伍']} ({player_data['位置']})")
    
    # 創建 Tabs
    tab1, tab2 = st.tabs(["📊 數據與資料", "📜 球隊歷史成績"])

    with tab1:
        st.subheader("1. 基礎數據與體型資料")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("身高", f"{player_data['身高 (cm)']} cm")
        col2.metric("體重", f"{player_data['體重 (kg)']} kg")
        col3.metric("位置", player_data['位置'])
        
        st.markdown(f"**🏅 過往獲獎紀錄：** {player_data['獲獎紀錄']}")
        st.markdown("---")

        st.subheader("2. 賽季核心表現 (2024-25 模擬數據)")
        
        # 顯示核心效率指標 (更新為 4 欄位，新增舉球效率)
        colA, colB, colC, colD = st.columns(4)
        colA.metric("總得分", f"{player_data['總得分']} 分")
        colB.metric("進攻決定率", f"{player_data['進攻決定率']:.1f} %", help="成功扣球數 / 總進攻次數")
        colC.metric("接發球成功率", f"{player_data['接發球成功率']:.1f} %", help="成功接發次數 / 總接發次數")
        colD.metric("舉球效率", f"{player_data['舉球效率']:.1f} %", help="舉球成功次數 / 總舉球次數。非舉球員會顯示 0.0 %。")

        st.subheader("3. 得分構成分析圖")

        # 繪製單一球員的得分構成圓餅圖
        score_data = pd.Series({
            '扣球得分': player_data['扣球得分'],
            '發球得分': player_data['發球得分'],
            '攔網得分': player_data['攔網得分']
        })
        
        # 繪製圓餅圖
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(score_data, 
               labels=score_data.index, 
               autopct='%1.1f%%', 
               startangle=90, 
               colors=['#FF5733', '#33FF57', '#3357FF'])
        ax.axis('equal') # 確保圓餅圖是圓的
        ax.set_title(f"{selected_player_name} 得分來源分佈")
        st.pyplot(fig)


    with tab2:
        st.subheader(f"📜 {player_data['隊伍']} 歷年比賽成績 (聯賽排名)")
        
        team_history = df_history[df_history['隊伍'] == player_data['隊伍']].sort_values(by='年份', ascending=False)
        
        if team_history.empty:
             st.warning(f"🚨 模擬歷史數據中沒有找到 {player_data['隊伍']} 的紀錄。")
        else:
            st.dataframe(
                team_history.rename(columns={'聯賽排名': '賽季排名'}),
                use_container_width=True
            )
            
            # 繪製歷史排名趨勢圖
            plt.figure(figsize=(10, 5))
            sns.lineplot(data=team_history, x='年份', y='聯賽排名', marker='o')
            plt.gca().invert_yaxis() # 排名越小越好，所以Y軸反轉
            plt.yticks(team_history['聯賽排名'].unique())
            plt.title(f"{player_data['隊伍']} 聯賽排名趨勢")
            plt.xlabel('年份')
            plt.ylabel('聯賽排名 (數字越小越好)')
            st.pyplot(plt.gcf())
            
st.markdown("---")
st.caption("數據來源：模擬 SV.LEAGUE 2024-25 賽季數據與歷史戰績。")
