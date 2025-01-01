import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib as mpl
import seaborn as sns

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 設定日期範圍（過去一年）
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

# 股票代碼列表
tickers = ['GOOGL', 'AMZN', 'NVDA', 'MSFT', 'AAPL', 'META']

# 獲取股票數據
stock_data = {}
for ticker in tickers:
    stock_data[ticker] = yf.download(ticker, start=start_date, end=end_date)

# 計算年度收益率
returns_data = []
for ticker in tickers:
    start_price = float(stock_data[ticker]['Close'].iloc[0].item())
    end_price = float(stock_data[ticker]['Close'].iloc[-1].item())
    annual_return = ((end_price - start_price) / start_price * 100)
    returns_data.append((ticker, annual_return))

# 排序收益率
returns_data.sort(key=lambda x: x[1], reverse=True)

# 創建價格走勢圖
plt.figure(figsize=(15, 8))
for ticker in tickers:
    # 將價格標準化為起始價格的百分比變化
    normalized_price = stock_data[ticker]['Close'] / stock_data[ticker]['Close'].iloc[0] * 100
    plt.plot(stock_data[ticker].index, normalized_price, label=ticker)

plt.title('主要科技股價格走勢比較 (過去一年)', fontsize=14)
plt.xlabel('日期')
plt.ylabel('價格變化 (%)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('tech_stocks_price.png', dpi=300, bbox_inches='tight')
plt.close()

# 計算每日回報率
returns_data_df = pd.DataFrame()
for ticker in tickers:
    returns_data_df[ticker] = stock_data[ticker]['Close'].pct_change()

# 計算年化波動率
volatility = returns_data_df.std() * np.sqrt(252) * 100
volatility = volatility.sort_values(ascending=False)

# 創建波動率圖表
plt.figure(figsize=(10, 6))
volatility.plot(kind='bar')
plt.title('各股票年化波動率', fontsize=14)
plt.xlabel('股票')
plt.ylabel('年化波動率 (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('volatility_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# 計算相關性矩陣
correlation_matrix = returns_data_df.corr()

# 找出最高和最低相關性
corr_matrix = correlation_matrix.values
np.fill_diagonal(corr_matrix, np.nan)
max_corr = np.nanmax(corr_matrix)
min_corr = np.nanmin(corr_matrix)

# 找出對應的股票對
max_corr_idx = np.where(correlation_matrix == max_corr)
min_corr_idx = np.where(correlation_matrix == min_corr)
max_corr_pair = (correlation_matrix.index[max_corr_idx[0][0]], correlation_matrix.columns[max_corr_idx[1][0]])
min_corr_pair = (correlation_matrix.index[min_corr_idx[0][0]], correlation_matrix.columns[min_corr_idx[1][0]])

# 創建相關性熱圖
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('股票回報率相關性矩陣', fontsize=14)
plt.tight_layout()
plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
plt.close()

report = f"""# 科技股票市場分析報告
## 更新時間：{datetime.now().strftime('%Y-%m-%d')}

### 1. 價格走勢分析
![價格走勢比較](tech_stocks_price.png)

過去一年中，主要科技股的表現各有差異：

#### 年度收益率排名：
"""

# 添加年度收益率數據到報告
for ticker, ret in returns_data:
    report += f"- {ticker}: {ret:.1f}%\n"

report += f"""
從價格走勢圖可以觀察到：
1. 表現最佳的股票是 {returns_data[0][0]}，年度收益率達到 {returns_data[0][1]:.1f}%
2. 表現最差的股票是 {returns_data[-1][0]}，年度收益率為 {returns_data[-1][1]:.1f}%

### 2. 風險分析

#### 波動率分析
![波動率分析](volatility_analysis.png)

各股票的年化波動率排名：
"""

# 添加波動率數據到報告
for ticker, vol in volatility.items():
    report += f"- {ticker}: {vol:.1f}%\n"

report += f"""
主要觀察：
1. {volatility.index[0]} 顯示最高波動率 ({volatility.iloc[0]:.1f}%)，表示價格波動最大
2. {volatility.index[-1]} 顯示最低波動率 ({volatility.iloc[-1]:.1f}%)，表示相對穩定

#### 相關性分析
![相關性矩陣](correlation_matrix.png)

從相關性熱圖中可以觀察到：
1. 最高相關性：{max_corr_pair[0]} 和 {max_corr_pair[1]} (相關係數: {max_corr:.2f})
   - 這表示這兩支股票的價格走勢高度相關，可能受相似的市場因素影響
2. 最低相關性：{min_corr_pair[0]} 和 {min_corr_pair[1]} (相關係數: {min_corr:.2f})
   - 這兩支股票的價格走勢相關性最低，適合用於投資組合分散風險

### 3. 投資建議

基於上述分析，我們可以得出以下投資建議：

1. 高增長機會：
   - {returns_data[0][0]} 和 {returns_data[1][0]} 在過去一年表現最佳，可能適合追求高報酬的投資者
   
2. 風險控制：
   - {volatility.index[-1]} 波動率最低，適合風險規避型投資者
   - 建議將 {min_corr_pair[0]} 和 {min_corr_pair[1]} 納入投資組合，以達到風險分散的效果

3. 投資組合建議：
   - 保守型投資者：以 {volatility.index[-1]} 為主，搭配少量高成長股票
   - 積極型投資者：可以配置更多 {returns_data[0][0]} 和 {returns_data[1][0]}，但需要承受較高波動風險
   - 平衡型投資者：綜合配置，並特別注意利用低相關性股票來分散風險
"""

# 保存報告
with open('tech_stocks_analysis.md', 'w', encoding='utf-8') as f:
    f.write(report) 