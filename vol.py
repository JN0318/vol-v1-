import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import matplotlib.font_manager as fm
import os

# =================================================================
# 0. 環境配置與字體設置 (修正路徑：直接從根目錄讀取字體檔案)
# =================================================================

st.set_page_config(layout="wide")
st.title("🏐 SV.LEAGUE 男排球員個人數據與歷史分析 (2023-2025 賽季)")
st.markdown("---")

# --- 中文字體設置 ---
font_path = './NotoSansCJKtc-Regular.otf' 

try:
    if os.path.exists(font_path):
        
        # 清理 Matplotlib 緩存
        cache_dir = fm.get_cachedir()
        for file in os.listdir(cache_dir):
            if file.startswith('fontlist-'):
                try:
                    os.remove(os.path.join(cache_dir, file))
                except:
                    pass
        
        # 註冊並使用新字體
        fm.fontManager.addfont(font_path)
        plt.rcParams['font.family'] = 'Noto Sans CJK TC' 
        plt.rcParams['axes.unicode_minus'] = False 
        st.sidebar.success("🎉 中文字體已成功加載！")
        
    else:
        st.sidebar.error(f"🚨 找不到字體文件於: {font_path}。請確保檔案已上傳到GitHub根目錄。")
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial'] 
        plt.rcParams['axes.unicode_minus'] = False
        
except Exception as e:
    st.sidebar.error(f"🚨 字體加載過程中發生錯誤: {e}")
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial'] 
    plt.rcParams['axes.unicode_minus'] = False


# =================================================================
# 1. 數據定義與載入 (包含所有 10 支隊伍 & 2023-2025 歷史數據)
# =================================================================

@st.cache_data
def load_data():
    # --- SV.LEAGUE 10 支隊伍列表 ---
    SVL_TEAMS = [
        'SUNTORY SUNBIRDS', 'WOLFDOGS NAGOYA', 'PANTHERS', 'JTEKT STINGS', 
        'OSAKA BLUTEON', 'NIPPON STEEL SAKAI', 'TOKYO GREAT BEARS', 
        'TORAY ARROWS SHIZUOKA', 'VC FUKUOKA', 'VOLEAS HOKKAIDO'
    ]
    
    # --- 1.1 球員個人數據 (2025 賽季模擬數據) ---
    data = {
        '姓名': ['Lopez, M.', 'Muserskiy, D.', 'Nimir, A.', '高橋藍', '西田有志', '蔡沛彰', '柳田将洋', '水町泰杜', '清水邦広', '関田誠大', '古賀太一郎', '深津英臣', '大宅真樹', '山内晶大', '宮浦健人', '彭世坤', '井上航'],
        '位置': ['OH', 'OP', 'OP', 'OH', 'OP', 'MB', 'OH', 'OP', 'OP', 'S', 'L', 'S', 'S', 'MB', 'OP', 'MB', 'L'],
        '隊伍': [
            'OSAKA BLUTEON', 'SUNTORY SUNBIRDS', 'WOLFDOGS NAGOYA', 'SUNTORY SUNBIRDS', 'PANTHERS', 'NIPPON STEEL SAKAI', 'TOKYO GREAT BEARS', 'WOLFDOGS NAGOYA', 'PANTHERS', 'JTEKT STINGS',
            'TOKYO GREAT BEARS', 'WOLFDOGS NAGOYA', 'JTEKT STINGS', 'PANTHERS', 
            'TORAY ARROWS SHIZUOKA', 'VC FUKUOKA', 'VOLEAS HOKKAIDO'
        ],
        '總得分': [550, 600, 580, 450, 400, 300, 350, 420, 380, 150, 0, 120, 140, 280, 410, 220, 0],
        '總進攻次數': [950, 1000, 980, 750, 700, 450, 720, 780, 700, 100, 0, 90, 110, 400, 700, 380, 0],
        '成功扣球數': [500, 520, 490, 380, 350, 240, 300, 380, 320, 80, 0, 70, 80, 220, 350, 190, 0],
        '接發球總次數': [450, 50, 40, 600, 30, 5, 550, 80, 20, 10, 800, 5, 8, 5, 40, 10, 750],
        '接發球成功次數': [250, 25, 15, 300, 10, 0, 280, 40, 5, 5, 450, 2, 3, 0, 15, 0, 400],
        '發球得分': [30, 40, 50, 25, 35, 10, 20, 30, 20, 10, 0, 25, 30, 15, 20, 10, 0],
        '攔網得分': [20, 40, 40, 45, 15, 50, 30, 10, 25, 50, 0, 15, 20, 45, 30, 20, 0],
        '總舉球次數': [0, 0, 0, 0, 0, 0, 0, 0, 0, 2000, 0, 2500, 2200, 0, 0, 0, 0],
        '舉球成功次數': [0, 0, 0, 0, 0, 0, 0, 0, 0, 850, 0, 1100, 950, 0, 0, 0, 0],
        '身高 (cm)': [190, 218, 200, 188, 186, 195, 188, 187, 190, 182, 170, 183, 178, 201, 195, 200, 178],
        '體重 (kg)': [85, 105, 95, 78, 80, 88, 77, 75, 82, 75, 68, 77, 73, 90, 88, 95, 72],
        '獲獎紀錄': [
            'V. MVP, Best 6', 'V. MVP, Best 6', 'V. MVP, Best Server', 'Best 6, 最佳接發', 
            'V. Score King', '亞洲錦標賽最佳MB', '奧運代表', '無', '天皇杯MVP', 'V. Best Setter', 
            '亞洲最佳自由球員', 'V. Best Setter', '無', 'V. Best 6, 攔網王', '無', '無', '無'
        ]
    }
    df = pd.DataFrame(data)

    # --- 1.2 模擬歷年球隊比賽成績 (2023-2025 賽季歷史數據) ---
    historical_data = {
        '年份': [2025, 2024, 2023, 2025, 2024, 2023, 2025, 2024, 2023, 2024, 2023, 2024, 2023],
        '隊伍': [
            'SUNTORY SUNBIRDS', 'SUNTORY SUNBIRDS', 'SUNTORY SUNBIRDS', 
            'WOLFDOGS NAGOYA', 'WOLFDOGS NAGOYA', 'WOLFDOGS NAGOYA', 
            'PANTHERS', 'PANTHERS', 'PANTHERS',
            'JTEKT STINGS', 'JTEKT STINGS',
            'OSAKA BLUTEON', 'OSAKA BLUTEON'
        ],
        '聯賽排名': [1, 2, 3, 3, 1, 2, 2, 3, 1, 4, 5, 6, 7],
        '總決賽結果': ['冠軍', '亞軍', '四強', '四強', '冠軍', '亞軍', '亞軍', '四強', '冠軍', '無緣', '無緣', '無緣', '無緣']
    }
    df_history = pd.DataFrame(historical_data)

    # --- 1.3 指標計算 ---
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

        st.subheader("2. 賽季核心表現 (2025 模擬數據)")
        
        # 顯示核心效率指標 
        colA, colB, colC, colD = st.columns(4)
        colA.metric("總得分", f"{player_data['總得分']} 分")
        # --- 修正後的第 174 行 ---
        colB.metric("進攻決定率", f"{player_data['進攻決定率']:.1f} %", help="成功扣球數 / 總進攻次數")
        # ------------------------
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
        wedges, texts, autotexts = ax.pie(score_data, 
                                          labels=score_data.index,
                                          autopct='%1.1f%%', 
                                          startangle=90, 
                                          colors=['#FF5733', '#33FF57', '#3357FF'])
        
        ax.axis('equal') 
        ax.set_title(f"{selected_player_name} 得分來源分佈")
        fig.tight_layout()
        st.pyplot(fig)


    with tab2:
        st.subheader(f"📜 {player_data['隊伍']} 歷年比賽成績 (2023-2025 聯賽排名)")
        
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
            sns.lineplot(data=team_history.sort_values(by='年份'), x='年份', y='聯賽排名', marker='o')
            plt.gca().invert_yaxis() 
            plt.yticks(team_history['聯賽排名'].unique())
            plt.xticks(team_history['年份'].unique()) 
            plt.title(f"{player_data['隊伍']} 聯賽排名趨勢")
            plt.xlabel('年份')
            plt.ylabel('聯賽排名 (數字越小越好)')
            st.pyplot(plt.gcf())
            
st.markdown("---")
st.caption("數據來源：模擬 SV.LEAGUE 2025 賽季個人數據與 2023-2025 歷史戰績。")
