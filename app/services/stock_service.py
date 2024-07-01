import yfinance as yf
import pandas as pd
import typing
import pprint
import urllib.parse
import os
from urllib.error import URLError
from requests import HTTPError

def get_stock_list(target:str):
  old_file = 'data_jpx.csv'
  if os.path.exists(old_file):
    os.remove(old_file)
  jpx_df = pd.read_csv(target, dtype=str, encoding='utf8')
  jpx_df['symbol'] = jpx_df['コード'] + '.T'
  jpx_df = jpx_df[(
      (jpx_df['市場・商品区分'] == 'プライム（内国株式）') |
      (jpx_df['市場・商品区分'] == 'スタンダード（内国株式）' ) |
      (jpx_df['市場・商品区分'] == 'グロース（内国株式）')
    )].copy()
  ticker_df = get_ticker_list(jpx_df)
  ticker_df.to_csv('data_jpx.csv', header=True, index=False)

def get_ticker_list(symbol_df: pd.DataFrame, start_index:int=0, limit_size:int=0):
  ticker_df = None

  count = 0
  for index, data in symbol_df.iterrows():
    if start_index > 0 and index < start_index:
      continue
    df = get_ticker(data.symbol, data.銘柄名)
    count += 1

    if df is None:
      continue
    if ticker_df is None:
      ticker_df = df
      continue
    ticker_df = pd.concat([ticker_df, df])
    if limit_size > 0 and count >= limit_size:
      break
  return ticker_df

def get_ticker(ticker_cd: str, ticker_nm: str) -> pd.DataFrame:
  ticker_df = None
  try:
    print(f"対象の銘柄:{ticker_cd}")
    modules = ['summaryProfile', 'financialData', 'quoteType', 'defaultKeyStatistics', 'assetProfile', 'summaryDetail']
    urllib.parse.urlencode([('ssl', 'true')] + [('module', m) for m in modules])
    
    ## データを取得
    ticker = yf.Ticker(ticker_cd)

    # 基本情報（概要） - marketCap(時価総額), sharesOutstanding(発行株数), forwardPE(予測PER), dividendYield(配当利回り), profitMargins(純利益比率)
    info = ticker.info
    # 財務諸表（直近４年分）- Total Revenue(売上高), Operating Income(営業利益), Net Income(当期純利益)
    financials = ticker.financials    
    # 貸借対照表（直近４年分）- Total Assets(総資産), Total Liab(総負債), Common Stock Equity(自己資本)
    balance_sheet = ticker.balance_sheet
    # 貸借対照表（直近４期分）
    quarterly_balance_sheet = ticker.quarterly_balance_sheet
    # キャッシュフロー（直近４年分）- Total Cashflows From Operating Activities(営業キャッシュフロー),  Total Cashflows From Financing Activities(財務キャッシュフロー), Total Cashflows From Investing Activities(投資キャッシュフロー)
    cashflow = ticker.cashflow
    # キャッシュフロー（直近４期分）
    quarterly_cashflow = ticker.quarterly_cashflow
    # 株価データ
    history = ticker.history(period="max")
    # 配当金
    dividends = ticker.dividends
    # 株式分割数
    splits = ticker.splits
    # 株式保有割合 - 全内部関係者の持ち株比率, 機関投資家の株式保有比率, 機関投資家の浮動株保有率, 所有機関数
    # major_holders = ticker.major_holders
    # ニュース
    news = ticker.news

    # info
    ticker_dict:typing.Dict[str, str] = {}
    ticker_dict["symbol"] = ticker_cd
    ticker_dict["name"] = ticker_nm # 会社名
    ticker_dict["eng_name"] = "" # 会社名(英語名)
    ticker_dict["sector"] = "" # セクター
    ticker_dict["industry"] = "" # 事業
    ticker_dict["currency"] = "" #通貨
    ticker_dict["price"] = "0.00" # 現在価格
    ticker_dict['forwardPE'] = "0.0" # forwardPE(予測PER)
    ticker_dict['trailingPegRatio'] = "0.0" # trailingPegRatio(実績PER)
    ticker_dict["targetHighPrice"] = "0.0"
    ticker_dict["targetLowPrice"] = "0.0"
    ticker_dict["targetMeanPrice"] = "0.0"
    ticker_dict["target_price"] = "0.0"
    ticker_dict["marketCap"] = "0.0" # 時価総額（億）
    ticker_dict["employee"] = "0" # 従業員数
    ticker_dict["person"] = "" # 代表者
    ticker_dict["dividend_yield"] = "0.0" # 年間配当利回り（%）
    ticker_dict["enterpriseValue"] = "0.0" # 企業価値
    ticker_dict["profitMargins"] = "0.0" # 利益率
    ticker_dict["floatShares"] = "0.0" # 浮動株
    ticker_dict["sharesOutstanding"] = "0.0" # 発行済株式数
    ticker_dict["heldPercentInsiders"] = "0.0" # 保有比率インサイダー
    ticker_dict["heldPercentInstitutions"] = "0.0" # 保有比率機関投資家
    ticker_dict["impliedSharesOutstanding"] = "0.0" # 発行済株式数
    ticker_dict["bookValue"] = "0.0" # 簿価
    ticker_dict["priceToBook"] = "0.0" # 帳簿価格
    ticker_dict["netIncomeToCommon"] = "0.0" # 純利益
    ticker_dict["trailingEps"] = "0.0" # トレーリングEPS
    ticker_dict["forwardEps"] = "0.0" # フォワードEps
    ticker_dict["pegRatio"] = "0.0" # ペッグレシオ
    ticker_dict["lastSplitFactor"] = "" # 最終分割日
    ticker_dict["lastSplitDate"] = "" # 最終分割日
    ticker_dict["enterpriseToRevenue"] = "0.0" # 企業収益
    ticker_dict["enterpriseToEbitda"] = "0.0" # 企業対売上高
    ticker_dict["totalCash"] = "0.0" # 現金総額
    ticker_dict["totalCashPerShare"] = "0.0" # 現金総額
    ticker_dict["ebitda"] = "0.0" # 平均株価
    ticker_dict["totalDebt"] = "0.0" # 総負債
    ticker_dict["quickRatio"] = "0.0" # クイックレシオ
    ticker_dict["currentRatio"] = "0.0" # 現在の比率
    ticker_dict["totalRevenue"] = "0.0" # 総収入
    ticker_dict["debtToEquity"] = "0.0" # 負債資本比率
    ticker_dict["revenuePerShare"] = "0.0" # 一株当たり収益
    ticker_dict["ROA"] = "0.0" # 資産利益率(ROA)
    ticker_dict["ROE"] = "0.0" # 株主資本利益率(ROE)
    ticker_dict["freeCashflow"] = "0.0" # フリーキャッシュフロー
    ticker_dict["operatingCashflow"] = "0.0" # 営業キャッシュフロー
    ticker_dict["earningsGrowth"] = "0.0" # 収益成長率
    ticker_dict["revenueGrowth"] = "0.0" # 収益成長率
    ticker_dict["grossMargins"] = "0.0" # 総利益
    ticker_dict["ebitdaMargins"] = "0.0" # 営業利益
    ticker_dict["operatingMargins"] = "0.0" # 営業利益
    ticker_dict["trailingPegRatio"] = "0.0" # 末尾ペッグレシ
    ticker_dict["netAssetsPerShare"] = "0.0"

    if "symbol" in info:
      ticker_dict["symbol"] = info["symbol"]
    if "shortName" in info:
      ticker_dict["eng_name"] = info["shortName"] # 会社名
    if "sector" in info:
      ticker_dict["sector"] = info["sector"] # セクター
    if "industry" in info:
      ticker_dict["industry"] = info["industry"] # 事業
    if "financialCurrency" in info:
      ticker_dict["currency"] = info["financialCurrency"] #通貨
    if "currentPrice" in info:
      ticker_dict["price"] = f"{info['currentPrice']:.2f}" # 現在価格
    if 'forwardPE' in info:
      ticker_dict['forwardPE'] = info['forwardPE'] # forwardPE(予測PER)
    if 'trailingPegRatio' in info:
      ticker_dict['trailingPegRatio'] = info['trailingPegRatio'] # trailingPegRatio(実績PER)
    if "targetHighPrice" in info:
      ticker_dict["targetHighPrice"] = f"{info['targetHighPrice']:.2f}"
    if "targetLowPrice" in info:
      ticker_dict["targetLowPrice"] = f"{info['targetLowPrice']:.2f}"
    if "targetMeanPrice" in info:
      ticker_dict["targetMeanPrice"] = f"{info['targetMeanPrice']:.2f}"
    if "targetMedianPrice" in info:
      ticker_dict["target_price"] = f"{info['targetMedianPrice']:.2f}"
    if "marketCap" in info:
      ticker_dict["marketCap"] = f"{info['marketCap'] / 100000000:.2f}" # 時価総額（億）
    if "fullTimeEmployees" in info:
      ticker_dict["employee"] = info['fullTimeEmployees'] # 従業員数
    if "companyOfficers" in info:
      ticker_dict["person"] = f"{info['companyOfficers'][0]['title']} {info['companyOfficers'][0]['name']}" # 代表者
    if "trailingAnnualDividendYield" in info:
      ticker_dict["dividend_yield"] = f"{round(info['trailingAnnualDividendYield'] * 100, 2):.2f}" # 年間配当利回り（%）
    if "enterpriseValue" in info:
      ticker_dict["enterpriseValue"] = info["enterpriseValue"] # 企業価値
    if "profitMargins" in info:
      ticker_dict["profitMargins"] = info["profitMargins"] # 利益率
    if "floatShares" in info:
      ticker_dict["floatShares"] = info["floatShares"] # 浮動株
    if "sharesOutstanding" in info:
      ticker_dict["sharesOutstanding"] = info["sharesOutstanding"] # 発行済株式数
    if "heldPercentInsiders" in info:
      ticker_dict["heldPercentInsiders"] = info["heldPercentInsiders"] # 保有比率インサイダー
    if "heldPercentInstitutions" in info:
      ticker_dict["heldPercentInstitutions"] = info["heldPercentInstitutions"] # 保有比率機関投資家
    if "impliedSharesOutstanding" in info:
      ticker_dict["impliedSharesOutstanding"] = info["impliedSharesOutstanding"] # 発行済株式数
    if "bookValue" in info:
      ticker_dict["bookValue"] = info["bookValue"] # 簿価
    if "priceToBook" in info:
      ticker_dict["priceToBook"] = info["priceToBook"] # 帳簿価格
    if "netIncomeToCommon" in info:
      ticker_dict["netIncomeToCommon"] = info["netIncomeToCommon"] # 純利益
    if "trailingEps" in info:
      ticker_dict["trailingEps"] = info["trailingEps"] # トレーリングEPS
    if "forwardEps" in info:
      ticker_dict["forwardEps"] = info["forwardEps"] # フォワードEPs
    if "pegRatio" in info:
      ticker_dict["pegRatio"] = info["pegRatio"] # ペッグレシオ
    if "lastSplitFactor" in info:
      ticker_dict["lastSplitFactor"] = info["lastSplitFactor"] # 最終分割日
    if "lastSplitDate" in info:
      ticker_dict["lastSplitDate"] = info["lastSplitDate"] # 最終分割日
    if "enterpriseToRevenue" in info:
      ticker_dict["enterpriseToRevenue"] = info["enterpriseToRevenue"] # 企業収益
    if "enterpriseToEbitda" in info:
      ticker_dict["enterpriseToEbitda"] = info["enterpriseToEbitda"] # 企業対売上高
    if "totalCash" in info:
      ticker_dict["totalCash"] = info["totalCash"] # 現金総額
    if "totalCashPerShare" in info:
      ticker_dict["totalCashPerShare"] = info["totalCashPerShare"] # 現金総額
    if "ebitda" in info:
      ticker_dict["ebitda"] = info["ebitda"] # 平均株価
    if "totalDebt" in info:
      ticker_dict["totalDebt"] = info["totalDebt"] # 総負債
    if "quickRatio" in info:
      ticker_dict["quickRatio"] = info["quickRatio"] # クイックレシオ
    if "currentRatio" in info:
      ticker_dict["currentRatio"] = info["currentRatio"] # 現在の比率
    if "totalRevenue" in info:
      ticker_dict["totalRevenue"] = info["totalRevenue"] # 総収入
    if "debtToEquity" in info:
      ticker_dict["debtToEquity"] = info["debtToEquity"] # 負債資本比率
    if "revenuePerShare" in info:
      ticker_dict["revenuePerShare"] = info["revenuePerShare"] # 一株当たり収益
    if "returnOnAssets" in info:
      ticker_dict["ROA"] = info["returnOnAssets"] # 資産利益率(ROA)
    if "returnOnEquity" in info:
      ticker_dict["ROE"] = info["returnOnEquity"] # 株主資本利益率(ROE)
    if "freeCashflow" in info:
      ticker_dict["freeCashflow"] = info["freeCashflow"] # フリーキャッシュフロー
    if "operatingCashflow" in info:
      ticker_dict["operatingCashflow"] = info["operatingCashflow"] # 営業キャッシュフロー
    if "earningsGrowth" in info:
      ticker_dict["earningsGrowth"] = info["earningsGrowth"] # 収益成長率
    if "revenueGrowth" in info:
      ticker_dict["revenueGrowth"] = info["revenueGrowth"] # 収益成長率
    if "grossMargins" in info:
      ticker_dict["grossMargins"] = info["grossMargins"] # 総利益
    if "ebitdaMargins" in info:
      ticker_dict["ebitdaMargins"] = info["ebitdaMargins"] # 営業利益
    if "operatingMargins" in info:
      ticker_dict["operatingMargins"] = info["operatingMargins"] # 営業利益
    if "trailingPegRatio" in info:
      ticker_dict["trailingPegRatio"] = info["trailingPegRatio"] # 末尾ペッグレシオ

    # financials
    if (len(financials) > 0 and 
      'Basic EPS' in financials.index and
      'Diluted EPS' in financials.index and
      'Basic Average Shares' in financials.index and
      'Total Revenue' in financials.index and
      'Net Income' in financials.index
    ):
      if (len(balance_sheet) > 0 and
        'Common Stock Equity' in balance_sheet.index and
        'Total Assets' in balance_sheet.index
      ):
        basic_eps_list = financials.loc['Basic EPS']
        diluted_eps_list = financials.loc['Diluted EPS']
        shares_list = financials.loc['Basic Average Shares']
        revenue_list =  financials.loc['Total Revenue']
        earnings_list = financials.loc['Net Income']
        equity_list = balance_sheet.loc['Common Stock Equity']
        assets_list = balance_sheet.loc['Total Assets']
        len_nums = [len(diluted_eps_list), len(diluted_eps_list), len(shares_list), len(revenue_list), len(earnings_list), len(equity_list), len(assets_list)]
        min_len = min(len_nums)
        for i in range(min_len):
          shares = shares_list.iloc[i]
          revenue = revenue_list.iloc[i]
          earnings = earnings_list.iloc[i]
          equity = equity_list.iloc[i]
          assets = assets_list.iloc[i]
          basic_eps = basic_eps_list.iloc[i]
          diluted_eps = diluted_eps_list.iloc[i]
          # ROE（Return on Equity）自己資本利益率
          # ROE = Net Income / Shareholder Equity
          # 投下した資本に対して企業がどれだけの利潤を上げられるのか、10〜20％程度で優良企業
          roe = 0.00
          if equity > 0:
            roe= round(earnings / equity * 100, 2)
          # ROA（Return On Asset）総資産利益率
          # ROA = Net Income / Average Total Assets
          # 会社が持っている総資産を利用して、どの程度の利益を上げているか、5%が超えていると優良企業
          roa = 0.00
          if assets > 0:
            roa = round(earnings / assets * 100, 2)
            # EPS（Earnings Per Share）1株当たり純利益
            eps = earnings / shares
            # print(f"{i} ROE={roe:.2f}% ROA={roa:.2f}% EPS={diluted_eps}")
            ticker_dict[f"revenue{i}"] = f"{revenue / 100000000:.2f}" # 売上高（億）
            ticker_dict[f"earnings_{i}"] = f"{earnings / 100000000:.2f}" # 純利益（億）
            ticker_dict[f"equity_{i}"] = f"{equity / 100000000:.2f}" # 純資産
            ticker_dict[f"assets_{i}"] = f"{assets / 100000000:.2f}" # 総資産
            ticker_dict[f"ROE_{i}"] = f"{roe:.2f}"
            ticker_dict[f"ROA_{i}"] = f"{roa:.2f}"
            ticker_dict[f"EPS_{i}"] = f"{diluted_eps}"
            if "price" in ticker_dict and 'trailingEps' in ticker_dict:
              # PER（Price Earnings Ratio）株価収益率 P/E
              # PER ＝ 株価  / 1株あたりの当期純利益（EPS）
              # 企業の純利益と株価の関係を示す指標
              ticker_dict["PER"] = '0.00'
              if  float(ticker_dict['trailingEps']) > 0.0:
                ticker_dict["PER"] = f"{float(ticker_dict['price']) / float(ticker_dict['trailingEps']):.2f}"
            if "price" in ticker_dict and 'sharesOutstanding' in ticker_dict and 'equity_0' in ticker_dict:
              # PBR（Price Book-value Ratio）　株価純資産倍率 P/B
              # PBR ＝ 株価 / 1株あたりの純資産（BPS）
              # 企業の純資産と株価との関係を示す指標
              ticker_dict["PBR"] = '0.00'
              if float(ticker_dict['sharesOutstanding']) > 0.0:
                ticker_dict["netAssetsPerShare"] = f"{float(ticker_dict['equity_0']) * 100000000 / float(ticker_dict['sharesOutstanding'])}"
              # 1株あたりの純資産(純資産額を発行済み株式総数で割る)
              if float(ticker_dict['netAssetsPerShare']) > 0.0:
                ticker_dict["PBR"] = f"{float(ticker_dict['price']) / float(ticker_dict['netAssetsPerShare']):.2f}"
                ticker_df = pd.DataFrame([ticker_dict])
                dir(ticker_df)
  except HTTPError as e:
      print("これはエラーです。")
      print(f"{ticker_cd} エラー : {e}")
      print("これはエラーです。")
      return None
  except URLError as e:
    print("これはエラーです。")
    print(f"{ticker_cd} エラー : {e}")
    print("これはエラーです。")
    return None
  return ticker_df

def get_filtered_stock_list(target:str):
  analysis_df = pd.read_csv(target, dtype=str, encoding='utf8')
  jpx_stock_df = pd.read_csv('data_jpx.csv', dtype=str, encoding='utf8')
  
  # 条件抽出用に特定のデータのみとする
  analysis_df = analysis_df[['symbol', 'price', 'target_price', 'dividend_yield', 'employee', 'marketCap','PBR', 'PER', 'ROE', 'ROA', 'EPS_0', 'EPS_1']]
  
  # 欠損値を0.0で置換
  analysis_df.fillna('0.0', inplace=True)
  
  # EPS 今期がない場合は、1期前を取得する
  analysis_df['EPS'] = analysis_df["EPS_0"]
  analysis_df.loc[analysis_df['EPS'] == '0.0', 'EPS'] = analysis_df['EPS_1']
  analysis_df.drop(['EPS_0', 'EPS_1'], axis=1, inplace=True)
  
  analysis_df['コード'] = analysis_df['symbol'].str.split('.').str[0]
  merged_df = pd.merge(analysis_df, jpx_stock_df, on='コード', how='left')
  merged_df.to_csv('filtered_data_jpx.csv', header=True, index=False)