import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

# =================================================================
# 1. 環境配置與數據準備
# =================================================================

# 設置 Streamlit 頁面標題
st.set_page_config(layout="wide")
st.title("🏐 日本 V1/SV.LEAGUE 男排球員互動式分析")
st.markdown("---")


# ----------------------------------------------------
# ⭐ 中文字體設置 (解決 Matplotlib 亂碼問題) ⭐
try:
    plt.rcParams['font.family'] = ['Arial Unicode MS', 'sans-serif'] 
except:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial'] 
    plt.rcParams['axes.unicode_minus'] = False 
# ----------------------------------------------------


# 創建模擬數據集 (加入更多球員和隊伍，使篩選更有意義)
data = {
    '姓名': ['Lopez, M.', 'Muserskiy, D.', 'Nimir, A.', '高橋藍', '西田有志', '蔡沛彰', '柳田将洋', '水町泰杜', '清水邦広', '関田誠大'],
    '位置': ['OH', 'OP', 'OP', 'OH', 'OP', 'MB', 'OH', 'OP', 'OP', 'S'],
    '隊伍': ['大阪B', 'SUNTORY', 'WD名古屋', 'SUNTORY', 'PANTHERS', '日鉄堺BZ', '東京GB', 'WD名古屋', 'PANTHERS', '捷太格特'],
    '總得分': [550, 600, 580, 450, 400, 300, 350, 420, 380, 150],
    '總進攻次數': [950, 1000, 980, 750, 700, 450, 720, 780, 700, 100],
    '成功扣球數': [500, 520, 490, 380, 350, 240, 300, 380, 320, 80],
    '失誤扣球數': [50, 60, 50, 40, 30, 20, 40, 35, 30, 5],
    '接發球總次數': [450, 50, 40, 600, 30, 5, 550, 80, 20, 10],
    '接發球成功次數': [250, 25, 15, 300, 10, 0, 280, 40, 5, 5],
    '發球得分': [30, 40, 50, 25, 35, 10, 20, 30, 20, 10],
    '攔網得分': [20, 40, 40, 45, 15, 50, 30, 10, 25, 50]
}

df = pd.DataFrame(data)

# =================================================================
# 2. 數據清洗與指標計算
# =================================================================

df['進攻決定率'] = (df['成功扣球數'] / df['總進攻次數']) * 100
df['進攻效率'] = ((df['成功扣球數'] - df['失誤扣球數']) / df['總進攻次數']) * 100
df['接發球成功率'] = df.apply(
    lambda row: (row['接發球成功次數'] / row['接發球總次數']) * 100 
    if row['接發球總次數'] > 0 else 0, 
    axis=1
)

# =================================================================
# 3. 互動式篩選器 (側邊欄)
# =================================================================

st.sidebar.header("🔍 分析篩選器")

# 獲取所有球隊名稱
all_teams = sorted(df['隊伍'].unique())
selected_teams = st.sidebar.multiselect(
    "選擇要分析的球隊 (可多選):",
    options=all_teams,
    default=all_teams # 預設選擇所有球隊
)

# 獲取所有位置
all_positions = sorted(df['位置'].unique())
selected_positions = st.sidebar.multiselect(
    "選擇要分析的位置 (可多選):",
    options=all_positions,
    default=all_positions
)

# 球員名稱搜尋
player_query = st.sidebar.text_input(
    "🔎 輸入球員名稱 (部分或全部):",
    value=""
)

# 應用篩選
df_filtered = df[
    (df['隊伍'].isin(selected_teams)) &
    (df['位置'].isin(selected_positions)) &
    (df['姓名'].str.contains(player_query, case=False, na=False))
]

if df_filtered.empty:
    st.error("🚨 根據您的篩選條件，沒有找到符合的球員數據。請調整篩選器。")
    st.stop() # 停止執行後續的圖表和數據

# =================================================================
# 4. 數據分析與可視化 (基於 df_filtered)
# =================================================================

# --- A. 數據總覽 ---
st.header("1. 球員核心數據總覽")
st.info(f"當前顯示 **{len(df_filtered)}** 位球員數據。")

display_cols = [
    '姓名', '位置', '隊伍', '總得分', 
    '進攻決定率', '進攻效率', '接發球成功率', 
    '發球得分', '攔網得分'
]
st.dataframe(
    df_filtered[display_cols].sort_values(by='總得分', ascending=False).set_index('姓名'),
    use_container_width=True,
    column_config={
        '進攻決定率': st.column_config.ProgressColumn("進攻決定率 (%)", format="%.1f %%", min_value=0, max_value=60),
        '進攻效率': st.column_config.ProgressColumn("進攻效率 (%)", format="%.1f %%", min_value=0, max_value=55),
        '接發球成功率': st.column_config.ProgressColumn("接發球成功率 (%)", format="%.1f %%", min_value=0, max_value=60),
    }
)


# --- B. 散點圖分析 (攻擊 vs. 接發球效率) ---
st.header("2. 攻擊與接發球效率散點圖分析 (OH & OP)")
st.write("此圖比較主攻手和接應手在進攻和防守核心任務上的表現。點越大，代表總得分越高。")

df_oh_op = df_filtered[df_filtered['位置'].isin(['OH', 'OP'])].copy()

if not df_oh_op.empty:
    plt.figure(figsize=(10, 7))
    sns.scatterplot(
        data=df_oh_op, 
        x='進攻效率',
        y='接發球成功率', 
        hue='位置', 
        size='總得分',  
        sizes=(80, 700), 
        style='位置',
        palette={'OH': '#1f77b4', 'OP': '#d62728'}
    )

    for i in range(df_oh_op.shape[0]):
        plt.text(
            df_oh_op['進攻效率'].iloc[i] + 0.3, 
            df_oh_op['接發球成功率'].iloc[i], 
            df_oh_op['姓名'].iloc[i], 
            fontsize=9,
            weight='bold'
        )

    plt.title('V1 男排攻擊效率 vs. 接發球成功率散點圖')
    plt.xlabel('進攻效率 (%)')
    plt.ylabel('接發球成功率 (%)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(title='位置', loc='lower right')
    
    st.pyplot(plt.gcf())
else:
    st.warning("⚠️ 散點圖無數據：當前篩選結果中沒有主攻手 (OH) 或接應手 (OP)。")


# --- C. 得分結構比較 (堆疊柱狀圖) ---
st.header("3. 球員得分結構分析 (堆疊柱狀圖)")

df_score_structure = df_filtered[['姓名', '成功扣球數', '發球得分', '攔網得分']].copy()
df_score_structure['扣球得分'] = df_score_structure['成功扣球數'] 

df_melted = df_score_structure.melt(
    id_vars='姓名', 
    value_vars=['扣球得分', '發球得分', '攔網得分'],
    var_name='得分類型', 
    value_name='得分數'
)

# 確保數據按總得分降序排列
name_order_filtered = df_filtered.sort_values(by='總得分', ascending=False)['姓名'].tolist()
df_melted['姓名'] = pd.Categorical(df_melted['姓名'], categories=name_order_filtered, ordered=True)
df_melted = df_melted.sort_values('姓名')


plt.figure(figsize=(12, 6))
sns.barplot(
    data=df_melted, 
    x='姓名', 
    y='得分數', 
    hue='得分類型', 
    dodge=False,  
    palette={'扣球得分': '#FF5733', '發球得分': '#33FF57', '攔網得分': '#3357FF'}
)

plt.title('V1 男排球員得分結構分析')
plt.xlabel('球員姓名')
plt.ylabel('得分數')
plt.legend(title='得分類型', loc='upper right')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

st.pyplot(plt.gcf())

st.markdown("---")
st.caption("數據來源：模擬 2024-25 賽季 V1/SV.LEAGUE 男排數據。")

# =================================================================
# 程式碼結束
# =================================================================
