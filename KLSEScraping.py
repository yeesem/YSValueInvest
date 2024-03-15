from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import requests

class KLSE:

    def __init__(self,symbol):
        self.symbol = symbol
    
    def scrap_stock_web_page(self):
        headers = {
          "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
        }
        url = "https://www.klsescreener.com/v2/stocks/view/" + self.symbol
        page = requests.get(url, headers=headers)
        html = page.content
        soup = BeautifulSoup(html)
        return soup
    
    def get_tables_html(self):
        soup = self.scrap_stock_web_page()

        all_table = soup.find_all("table",class_ = "table table-hover table-theme")

        return all_table
    
    def get_stock_basic_info(self):
        soup = self.scrap_stock_web_page()

        price = soup.find('span',id = 'price')['data-value']

        price_diff = soup.find('span',id = 'priceDiff')
        price_diff = price_diff.text.split(" ")
        price_diff_percentage = price_diff[1].replace('(','').replace(')','')
        price_diff = price_diff[0]  

        company_summary = soup.find('div',class_ = 'modal-body').text.strip()
        
        div = soup.find('div',class_ = 'modal-body')
        website_link = div.find('a').text
        company_summary = div.text.strip().split("  ")[0]

        scrap_company_name = soup.find('title').text.strip().split("|")
        scrap_company_name = scrap_company_name[0].split(":")
        company_short_name = scrap_company_name[0]
        company_name = scrap_company_name[1][1:-8]
        company_symbol = scrap_company_name[1][-7:-1]

        company_sector = soup.find_all("span",class_ = "text-muted")[0].text.strip()

        stock_basic_info = {
        'short name' : company_short_name,
        'full name' : company_name,
        'symbol' : company_symbol,
        'price' : price,
        'different price' : price_diff,
        'different price in percentage' : price_diff_percentage,
        'company summary' : company_summary,
        'company sector' : company_sector,
        'company link' : website_link
        }

        return stock_basic_info
    
    def get_stock_summary(self):
        soup = self.scrap_stock_web_page()
        table = soup.find('table',class_ = "stock_details table table-hover table-striped table-theme")
        
        incomplete_titles = table.find_all("tr")
        titles = [title.text.strip() for title in incomplete_titles]

        stock_info = []

        titles = [item.split('\n') for item in titles]

        title = []
        value = []
        for item in titles:
          if len(item) == 2:
             title.append(item[0])
             value.append(item[1])

        stock_info = pd.DataFrame(value,title)
        stock_info = stock_info.transpose()

        drop_col = ["Volume (B/S)","RPS","Volume"]
        stock_info.drop(drop_col,axis = 1,inplace = True)

        stock_info.rename(columns = {'52w' : '52 Weeks Price Range', 'Shares (mil)' : 'Num of Shares (mil)'},inplace = True)

        return stock_info

    def shareholding_changes_table(self):
       
        shareholding_change_table = self.get_tables_html()[4]

        shareholding_change_header = shareholding_change_table.find_all("th")
        shareholding_change_header = [item.text.strip() for item in shareholding_change_header]

        shareholding_change_data = shareholding_change_table.find_all("tr")
        shareholding_change_data = [item.text.strip() for item in shareholding_change_data][1:]

        test = [item.split("\n") for item in shareholding_change_data]
        
        shareholding_change_table = pd.DataFrame(test,columns = shareholding_change_header)
        
        return shareholding_change_table
    
    def capital_changes_table(self):
        capital_changes_table = self.get_tables_html()[2]

        capital_changes_header = capital_changes_table.find_all("th")
        capital_changes_header = [item.text.strip() for item in capital_changes_header][:-1]

        capital_changes_data = capital_changes_table.find_all("tr")
        capital_changes_data = [item.text.strip() for item in capital_changes_data][1:]

        capital_changes_test = [item.split("\n") for item in capital_changes_data]
        capital_changes_test = [[item2 for item2 in item if (item2 != "" and item2!= "View")] for item in capital_changes_test]
        
        capital_changes_test = [item + [""] for item in capital_changes_test if len(item)!=5]
        
        capital_changes_table = pd.DataFrame(capital_changes_test, columns = capital_changes_header)

        return capital_changes_table
    
    def get_annual_financial_data(self):
        table  = self.get_tables_html()[0]
        
        #Get Annual Report Link
        annual_report_list = table.find_all('a')

        annual_report_link = []

        for item in annual_report_list:
          annual_report_link.append("https://www.klsescreener.com" + item['href'])
        annual_report_link.reverse() 

        #Call get_dividend_table()
        dividend_table = self.get_dividend_table()
        
        dividend_summary = pd.DataFrame({
            'Financial Year': dividend_table['Financial Year'],
            'Amount': dividend_table['Amount']
        })

        dividend_summary['Amount'] = dividend_summary['Amount'].astype(float)
        
        dividend_summary = dividend_summary.groupby('Financial Year').sum()
        dividend_summary.index = pd.to_datetime(dividend_summary.index)
        dividend_summary = dividend_summary.sort_index()
      
    
        incompleted_titles = table.find_all('th')[0:10]
        titles = [title.text for title in incompleted_titles]
        incompleted_title = table.find_all('th')
        titles = [title.text.strip() for title in incompleted_title]

        df = pd.DataFrame(columns = titles[:4])
        DP_And_NetInc = titles[7:]

        DP = []
        NetInc = []

        i = 0

        for item in DP_And_NetInc:
          if i % 2 == 0:
            DP.append(item)
          else:
            NetInc.append(item)
          i+=1
   
        column_data = table.find_all('tr')
        annual_data = []
        for row in column_data[1:]:
          row_data = row.find_all('td')
          individual_row_data = [data.text.strip() for data in row_data]
          annual_data.append(individual_row_data)
          length = len(df)
          df.loc[length] = individual_row_data[:4]

        df = df.sort_values(by = 'Financial Year',ascending = True)
        df.columns = ['Financial Year','Revenue','Net Profit','EPS']

        df.set_index('Financial Year',inplace = True)
        DP.reverse()
        df["DP %"] = DP

        NetInc.reverse()
        df["Net Profit Y-o-Y Growth %"] = NetInc

        df['DP %'] = df['DP %'].replace("-","0")
        df['DP %'] = df['DP %'].astype(float)

        while len(df['Revenue']) != len(annual_report_link):
           annual_report_link.append(np.nan)

        df["Annual Report Link"] = annual_report_link

        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        
        ### ERROR
        df = pd.merge(df, dividend_summary, left_index=True, right_index=True)
        df = df.rename(columns = {'Amount' : 'Total Dividend Paid'})

        new_col_sequence = ["Revenue","Net Profit","EPS","DP %","Total Dividend Paid","Net Profit Y-o-Y Growth %","Annual Report Link"]

        df = df[new_col_sequence]
        df["Total Dividend Paid"] = round(df['Total Dividend Paid'],4)

        return df
    
    def get_dividend_table(self):
        dividend_table = self.get_tables_html()[1]
        dividend_table_title = [item.text for item in dividend_table.find_all("th")]

        dividend_table_row = [item.text.strip() for item in dividend_table.find_all("tr")]

        dividend_table_row = dividend_table_row[1:]
        test = dividend_table_row[1].split("  ")
        test = [item.strip() for item in test if item not in ['','\n\n'] ]

        dividend_table_data = []
        for item in dividend_table_row:
          temp = item.split("  ")
          if len(temp) == 1:
            continue
          else:
            temp = [x.strip() for x in temp if x.strip() not in ['','\n\n','\n','Currency','Percentage','View',"RM"]]
            dividend_table_data.append(temp)

        dividend_table = pd.DataFrame(dividend_table_data,columns = dividend_table_title[:6])
      
        return dividend_table

    def get_YoY_and_QoQ_tag(self,quarter_result_html):           
           
        span_tags = quarter_result_html.find_all("span")           
                
        qoq_tag = []           
        yoy_tag = []           
                
        i = 0           
                
        for span_tag in span_tags:           
            class_name = span_tag.get("class")           
            if class_name == None:           
              continue           
            if i%2 == 0:           
              qoq_tag.append(class_name)           
            if i%2 == 1:           
              yoy_tag.append(class_name)           
            i = i + 1           
                
        return qoq_tag,yoy_tag     
    
    def YoY_calculation(self,table,col,yoy_tag):
        for i in range(len(table[col])):
            if yoy_tag[i][1] == "btn-danger":
              table[col][i] = "-" + table[col][i]

        return table[col]      
    
    def QoQ_calculation(self,table,col,compare_col):
        for i in range(1,len(table[col]),1):
            if float(table[compare_col].iloc[i-1][:-1]) < float(table[compare_col].iloc[i][:-1]):
              table[col].iloc[i-1] = "-" + table[col].iloc[i-1]

        return table[col]

    def get_quarter_financial_data(self):
       soup = self.scrap_stock_web_page()
       quarter_result_html = soup.find("table",class_ = "financial_reports table table-hover table-sm table-theme")
       
       quarter_result_header = quarter_result_html.find_all("th")
       quarter_result_header = [item.text.strip() for item in quarter_result_header][:-1]

       quarter_result_data = quarter_result_html.find_all("tr")
       quarter_result_data = [item.text.strip() for item in quarter_result_data][1:]

       quarter_data = []

       for item in quarter_result_data:
          item = item.split("\n")
          if len(item) == 1:
            continue
          else:
            item = [tempt for tempt in item if tempt != 'View'][:-1]
            quarter_data.append(item)

       quarter_result_table = pd.DataFrame(quarter_data,columns = quarter_result_header)
       quarter_result_table = quarter_result_table.rename(columns = {"P/L" : "Net Profit","Q Date":"Quarter Date","QoQ%" : "Net Profit QoQ","YoY%" : "Net Profit YoY"})

       new_col_order = ["EPS","DPS","NTA","ROE","Revenue","Net Profit","Quarter","Quarter Date","Financial Year","Announced","Net Profit QoQ","Net Profit YoY"]
       quarter_result_table = quarter_result_table[new_col_order]

       quarter_result_table["ROE"] = [item.replace("%","") for item in quarter_result_table["ROE"]]

       col = ["EPS","DPS","NTA","ROE"]

       for item in col:
           quarter_result_table[item] = quarter_result_table[item].astype(float)
           quarter_result_table[item] = round(quarter_result_table[item],2)
           
       yoy_tag = self.get_YoY_and_QoQ_tag(quarter_result_html)
       print("Test : ",len(yoy_tag),"\n",yoy_tag)
       yoy_tag = yoy_tag[1]
       
       quarter_result_table["Net Profit YoY"] = self.YoY_calculation(quarter_result_table,"Net Profit YoY",yoy_tag)

       quarter_result_table["Net Profit QoQ"] = self.QoQ_calculation(quarter_result_table,"Net Profit QoQ","Net Profit")

       quarter_result_table.set_index('Quarter Date',inplace = True)
       quarter_result_table.index = pd.to_datetime(quarter_result_table.index)

       quarter_result_table.sort_index(ascending = True,inplace = True)
       
       return quarter_result_table