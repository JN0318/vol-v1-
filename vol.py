import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 創建模擬數據集 (使用中文變數名稱方便理解)
data = {
    '姓名': ['Lopez, M.', 'Muserskiy, D.', 'Nimir, A.', '高橋藍', '西田有志', '蔡沛彰'],
    '位置': ['OH', 'OP', 'OP', 'OH', 'OP', 'MB'],
    '隊伍': ['大阪B', 'SUNTORY', 'WD名古屋', 'SUNTORY', 'PANTHERS', '日鉄堺BZ'],
    '總得分': [550, 600, 580, 450, 400, 300],
    '總進攻次數': [950, 1000, 980, 750, 700, 450],
    '成功扣球數': [500, 520, 490, 380, 350, 240],
    '接發球總次數': [450, 50, 40, 600, 30, 5],
    '接發球成功次數': [250, 25, 15, 300, 10, 0],
    '發球得分': [30, 40, 50, 25, 35, 10],
    '攔網得分': [20, 40, 40, 45, 15, 50]
}

df = pd.DataFrame(data)

# 2. 數據清洗與指標計算
# 進攻決定率 (Attack Kill Percentage): 成功扣球數 / 總進攻次數
df['進攻決定率'] = (df['成功扣球數'] / df['總進攻次數']) * 100

# 接發球效率/成功率 (Reception Success Rate): 接發球成功次數 / 接發球總次數
# 由於MB/OP的接發球次數很低，我們設定一個小的容錯值防止除以零
df['接發球成功率'] = df.apply(
    lambda row: (row['接發球成功次數'] / row['接發球總次數']) * 100 
    if row['接發球總次數'] > 0 else 0, 
    axis=1
)

# 攻擊佔比 (Attack Ratio): 成功扣球得分 / 總得分
df['攻擊佔比'] = ((df['總得分'] - df['發球得分'] - df['攔網得分']) / df['總得分']) * 100
df.loc[df['總得分'] == 0, '攻擊佔比'] = 0 # 避免除以零

# 3. 數據分析與展示
print("--- 數據總覽 (新增效率指標) ---")
print(df[['姓名', '位置', '進攻決定率', '接發球成功率', '發球得分', '攔網得分']].sort_values(by='進攻決定率', ascending=False))

# 4. 數據可視化：進攻效率 vs 接發球效率 (散點圖)
# 主要關注主攻手 (OH) 和接應 (OP)
df_oh_op = df[df['位置'].isin(['OH', 'OP'])].copy()

plt.figure(figsize=(10, 7))
sns.scatterplot(
    data=df_oh_op, 
    x='進攻決定率', 
    y='接發球成功率', 
    hue='位置', 
    size='總得分',  # 用總得分的大小來表示球員的影響力
    sizes=(50, 500), 
    style='位置',
    palette={'OH': 'blue', 'OP': 'red'}
)

# 為每個點標註球員名稱
for i in range(df_oh_op.shape[0]):
    plt.text(
        df_oh_op['進攻決定率'].iloc[i] + 0.5, 
        df_oh_op['接發球成功率'].iloc[i], 
        df_oh_op['姓名'].iloc[i], 
        fontsize=9
    )

plt.title('V1 男排攻擊與接發球效率散點分析 (OH & OP)')
plt.xlabel('進攻決定率 (%)')
plt.ylabel('接發球成功率 (%)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title='位置')
plt.show()

# 5. 數據可視化：得分結構比較 (柱狀圖)
# 比較不同球員的得分構成
df_score_structure = df[['姓名', '成功扣球數', '發球得分', '攔網得分']]
df_score_structure['成功扣球得分'] = df_score_structure['成功扣球數']

# 為了繪製堆疊柱狀圖，需要先將數據轉換格式 (melt)
df_melted = df_score_structure.melt(
    id_vars='姓名', 
    value_vars=['成功扣球得分', '發球得分', '攔網得分'],
    var_name='得分類型', 
    value_name='得分數'
)

plt.figure(figsize=(12, 6))
sns.barplot(
    data=df_melted, 
    x='姓名', 
    y='得分數', 
    hue='得分類型', 
    dodge=False,  # 堆疊柱狀圖
    palette=['#FF5733', '#33FF57', '#3357FF']
)

plt.title('V1 男排球員得分結構分析 (堆疊柱狀圖)')
plt.xlabel('球員姓名')
plt.ylabel('得分數')
plt.legend(title='得分類型')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
