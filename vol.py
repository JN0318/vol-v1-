import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import matplotlib.font_manager as fm

# =================================================================
# 1. 環境配置與數據準備
# =================================================================

st.set_page_config(layout="wide")
st.title("🏐 SV.LEAGUE 男排進階互動分析（位置專區與體型數據）")
st.markdown("---")

# ----------------------------------------------------
# ⭐ 中文字體設置 ⭐
# ----------------------------------------------------
font_path = './fonts/NotoSansCJKtc-Regular.otf' 
try:
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = 'Noto Sans CJK TC' 
    plt.rcParams['axes.unicode_minus'] = False 
except Exception:
    st.sidebar.warning("⚠️ 找不到指定字體。圖表中文可能顯示為方塊。")
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial'] 
    plt.rcParams['axes.unicode_minus'] = False


# ----------------------------------------------------
# 💡 數據集擴充：加入身高、體重、獲獎紀錄
# ----------------------------------------------------
data = {
    '姓名': ['Lopez, M.', 'Muserskiy, D.', 'Nimir, A.', '高橋藍', '西田有志', '蔡沛彰', '柳田将洋', '水町泰杜', '清水邦広', '関田誠大', '武田大周', '秦耕介', '外崎航平', '小野寺太志', '古賀太一郎', '深津英臣', '大宅真樹'],
    '位置': ['OH', 'OP', 'OP', 'OH', 'OP', 'MB', 'OH', 'OP', 'OP', 'S', 'OH', 'MB', 'OH', 'MB', 'L', 'S', 'S'],
    '隊伍': [
        'OSAKA BLUTEON (大阪B)', 'SUNTORY SUNBIRDS 大阪 (SUNTORY)', 'WOLFDOGS NAGOYA (WD名古屋)', 'SUNTORY SUNBIRDS 大阪 (SUNTORY)', 'PANTHERS (PANTHERS)', 'NIPPON STEEL SAKAI BLAZERS (日鉄堺BZ)', 'TOKYO GREAT BEARS (東京GB)', 'WOLFDOGS NAGOYA (WD名古屋)', 'PANTHERS (PANTHERS)', 'JTEKT STINGS (捷太格特)',
        'TORAY ARROWS SHIZUOKA (東レ静岡)', 'VC FUKUOKA (福岡)', 'VOLEAS HOKKAIDO (北海道)', 'SUNTORY SUNBIRDS 大阪 (SUNTORY)', 'TOKYO GREAT BEARS (東京GB)', 'WOLFDOGS NAGOYA (WD名古屋)', 'JTEKT STINGS (捷太格特)'
    ],
    '總得分': [550, 600, 580, 450, 400, 300, 350, 420, 380, 150, 280, 200, 310, 250, 0, 120, 140],
    '總進攻次數': [950, 1000, 980, 750, 700, 450, 720, 780, 700, 100, 500, 350, 600, 400, 0, 90, 110],
    '成功扣球數': [500, 520, 490, 380, 350, 240, 300, 380, 320, 80, 250, 180, 280, 220, 0, 70, 80],
    '失誤扣球數': [50, 60, 50, 40, 30, 20, 40, 35, 30, 5, 25, 15, 30, 10, 0, 10, 15],
    '接發球總次數': [450, 50, 40, 600, 30, 5, 550, 80, 20, 10, 400, 10, 500, 5, 800, 5, 8],
    '接發球成功次數': [250, 25, 15, 300, 10, 0, 280, 40, 5, 5, 220, 0, 240, 0, 450, 2, 3],
    '發球得分': [30, 40, 50, 25, 35, 10, 20, 30, 20, 10, 10, 5, 15, 5, 0, 25, 30],
    '攔網得分': [20, 40, 40, 45, 15, 50, 30, 10, 25, 50, 5, 30, 5, 25, 0, 15, 20],
    '總舉球次數': [0, 0, 0, 0, 0, 0, 0, 0, 0, 2000, 0, 0, 0, 0, 0, 2500, 2200],
    '舉球成功次數': [0, 0, 0, 0, 0, 0, 0, 0, 0, 850, 0, 0, 0, 0, 0, 1100, 950],
    # 新增數據欄位
    '身高 (cm)': [190, 218, 200, 188, 186, 195, 188, 187, 190, 182, 187, 192, 185, 198, 170, 183, 178],
    '體重 (kg)': [85, 105, 95, 78, 80, 88, 77, 75, 82, 75, 76, 89, 74, 92, 68, 77, 73],
    '獲獎紀錄': [
        'V. MVP, Best 6', 'V. MVP, Best 6', 'V. MVP, Best Server', 'Best 6, 最佳接發', 
        'V. Score King', '亞洲錦標賽最佳MB', '奧運代表', '無', '天皇杯MVP', 'V. Best Setter', 
        '無', '無', '無', '無', '亞洲最佳自由球員', 'V. Best Setter', '無'
    ]
}

df = pd.DataFrame(data)

# ----------------------------------------------------
# 2. 數據清洗與指標計算
# ----------------------------------------------------

df['進攻決定率'] = np.where(df['總進攻次數'] > 0, (df['成功扣球數'] / df['總進攻次數']) * 100, 0)
df['進攻效率'] = np.where(df['總進攻次數'] > 0, ((df['成功扣球數'] - df['失誤扣球數']) / df['總進攻次數']) * 100, 0)
df['接發球成功率'] = np.where(df['接發球總次數'] > 0, (df['接發球成功次數'] / df['接發球總次數']) * 100, 0)
df['舉球效率'] = np.where(df['總舉球次數'] > 0, (df['舉球成功次數'] / df['總舉球次數']) * 100, 0)


# =================================================================
# 3. 互動式篩選器 (側邊欄)
# =================================================================

st.sidebar.header("🔍 全局數據篩選")

all_teams_in_data = sorted(df['隊伍'].unique())
selected_teams = st.sidebar.multiselect(
    "選擇要分析的球隊:",
    options=all_teams_in_data, 
    default=all_teams_in_data 
)

# 專用於全局篩選，以便在所有圖表中進行過濾
all_positions = sorted(df['位置'].unique())
selected_positions_global = st.sidebar.multiselect(
    "選擇要分析的位置:",
    options=all_positions,
    default=all_positions
)

player_query = st.sidebar.text_input(
    "🔎 輸入球員名稱:",
    value=""
)

# 應用全局篩選
df_filtered = df[
    (df['隊伍'].isin(selected_teams)) &
    (df['位置'].isin(selected_positions_global)) &
    (df['姓名'].str.contains(player_query, case=False, na=False))
]

if df_filtered.empty:
    st.error("🚨 根據您的篩選條件，沒有找到符合的球員數據。請調整篩選器。")
    st.stop() 

st.sidebar.markdown("---")
# ----------------------------------------------------
# 📌 新增：單一位置分析選擇器
# ----------------------------------------------------
st.sidebar.header("🎯 單一位置深度分析")
position_options = ['OH', 'OP', 'MB', 'S', 'L']
selected_single_position = st.sidebar.radio(
    "選擇一個位置進行專屬分析:",
    options=['無'] + position_options, # 預設為 '無'
    index=0
)


# =================================================================
# 4. 數據分析與可視化 (基於 df_filtered)
# =================================================================

# --- 4.1 單一位置專區 (動態內容) ---
if selected_single_position != '無':
    st.header(f"1. 🔬 {selected_single_position} 位置深度分析")
    
    df_pos = df_filtered[df_filtered['位置'] == selected_single_position].copy()
    if df_pos.empty:
        st.warning(f"當前篩選器中沒有找到 {selected_single_position} 位置的球員。")
    else:
        st.subheader(f"1.1 {selected_single_position} 體型與紀錄總覽")
        
        # 體型和獲獎紀錄表格
        body_records_cols = ['姓名', '隊伍', '身高 (cm)', '體重 (kg)', '獲獎紀錄']
        st.dataframe(
            df_pos[body_records_cols].sort_values(by='身高 (cm)', ascending=False).set_index('姓名'),
            use_container_width=True
        )

        st.subheader(f"1.2 {selected_single_position} 關鍵指標比較")
        
        # 根據位置顯示不同的圖表
        
        if selected_single_position in ['OH', 'OP']:
            # OH/OP 關鍵圖表：進攻效率 vs 體重
            plt.figure(figsize=(10, 6))
            sns.scatterplot(
                data=df_pos, x='體重 (kg)', y='進攻效率', size='總得分', sizes=(100, 700), hue='姓名',
                palette='coolwarm', legend=False
            )
            for i in range(df_pos.shape[0]):
                plt.text(df_pos['體重 (kg)'].iloc[i] + 0.5, df_pos['進攻效率'].iloc[i], 
                         df_pos['姓名'].iloc[i], fontsize=9)
            plt.title(f"{selected_single_position}：進攻效率 vs 體重")
            plt.xlabel('體重 (kg)')
            plt.ylabel('進攻效率 (%)')
            st.pyplot(plt.gcf())
            
        elif selected_single_position == 'MB':
            # MB 關鍵圖表：攔網得分 vs 身高
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df_pos.sort_values(by='攔網得分', ascending=False), 
                        x='姓名', y='攔網得分', hue='身高 (cm)', dodge=False, palette='crest')
            plt.title("攔中 (MB)：攔網得分排名與身高")
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('攔網得分')
            plt.xlabel('姓名')
            st.pyplot(plt.gcf())
            
        elif selected_single_position == 'S':
            # S 關鍵圖表：舉球效率 vs 攔網得分
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=df_pos, x='舉球效率', y='攔網得分', size='發球得分', sizes=(100, 700), hue='姓名')
            for i in range(df_pos.shape[0]):
                plt.text(df_pos['舉球效率'].iloc[i] + 0.5, df_pos['攔網得分'].iloc[i], 
                         df_pos['姓名'].iloc[i], fontsize=9)
            plt.title("舉球員 (S)：舉球效率 vs 攔網威脅")
            plt.xlabel('舉球效率 (%)')
            plt.ylabel('攔網得分')
            st.pyplot(plt.gcf())
            
        elif selected_single_position == 'L':
            # L 關鍵圖表：接發球效率 vs 體重
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df_pos.sort_values(by='接發球成功率', ascending=False), 
                        x='姓名', y='接發球成功率', hue='體重 (kg)', dodge=False, palette='magma')
            plt.title("自由球員 (L)：接發球成功率排名")
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('接發球成功率 (%)')
            st.pyplot(plt.gcf())
        
    st.markdown("---")


# ----------------------------------------------------
# 📌 恢復：所有球員的綜合分析 (當單選為 '無' 或看全局數據時)
# ----------------------------------------------------
if selected_single_position == '無':
    st.header("2. 所有球員數據總覽")
    st.info(f"當前顯示所有篩選結果中的 **{len(df_filtered)}** 位球員數據。")
    
    # 增加身高體重欄位到總覽
    display_cols = ['姓名', '位置', '隊伍', '總得分', '進攻決定率', '接發球成功率', '攔網得分', '舉球效率', '身高 (cm)', '體重 (kg)', '獲獎紀錄']
    st.dataframe(
        df_filtered[display_cols].sort_values(by='總得分', ascending=False).set_index('姓名'),
        use_container_width=True,
        column_config={
            '進攻決定率': st.column_config.ProgressColumn("進攻決定率 (%)", format="%.1f %%", min_value=0, max_value=60),
            '接發球成功率': st.column_config.ProgressColumn("接發球成功率 (%)", format="%.1f %%", min_value=0, max_value=60),
            '獲獎紀錄': st.column_config.TextColumn("獲獎紀錄", help="球員過往或本賽季的重要個人榮譽")
        }
    )
    
    # --- 4.2 攔網得分專區 (在 '無' 模式下顯示) ---
    st.header("3. 攔網得分（Blocking Points）表現分析")
    df_blocks = df_filtered[df_filtered['攔網得分'] > 0].sort_values(by='攔網得分', ascending=False).copy()
    if not df_blocks.empty:
        st.subheader("3.1 攔網得分排名")
        block_cols = ['姓名', '隊伍', '位置', '攔網得分', '總得分']
        st.dataframe(df_blocks[block_cols].set_index('姓名'), use_container_width=True)
        st.subheader("3.2 攔網得分與總得分關係圖")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df_blocks, x='攔網得分', y='總得分', hue='位置', size='攔網得分', sizes=(100, 800), palette='viridis')
        top_blockers = df_blocks.head(5)
        for i in range(top_blockers.shape[0]):
            plt.text(top_blockers['攔網得分'].iloc[i] + 0.5, top_blockers['總得分'].iloc[i], f"{top_blockers['姓名'].iloc[i]}", fontsize=9, weight='bold')
        plt.title('球員攔網得分與總得分散點圖')
        plt.xlabel('攔網得分')
        plt.ylabel('總得分')
        st.pyplot(plt.gcf())
    
    st.markdown("---")
    st.header("4. 所有球員得分結構分析")
    # 繪製總得分結構圖 (與之前相同)
    df_score_structure = df_filtered[['姓名', '成功扣球數', '發球得分', '攔網得分']].copy()
    df_score_structure['扣球得分'] = df_score_structure['成功扣球數'] 
    df_melted = df_score_structure.melt(id_vars='姓名', value_vars=['扣球得分', '發球得分', '攔網得分'], var_name='得分類型', value_name='得分數')
    name_order_filtered = df_filtered.sort_values(by='總得分', ascending=False)['姓名'].tolist()
    df_melted['姓名'] = pd.Categorical(df_melted['姓名'], categories=name_order_filtered, ordered=True)
    df_melted = df_melted.sort_values('姓名')
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df_melted, x='姓名', y='得分數', hue='得分類型', dodge=False, palette={'扣球得分': '#FF5733', '發球得分': '#33FF57', '攔網得分': '#3357FF'})
    plt.title('V1 男排球員得分結構分析')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt.gcf())

st.markdown("---")
st.caption("數據來源：模擬 2024-25 賽季 SV.LEAGUE 男排數據。")

# =================================================================
# 程式碼結束
# =================================================================
