import urllib
from datetime import date, timedelta
from time import strftime
from HTMLParser import HTMLParser
from FinancialReport import FinancialReport

class Helper:
    @classmethod
    def isReal(self, txt):
        try:
            txt = ''.join(txt.replace(',','.').strip().split())
            float(txt)
            return True
        except ValueError:
            return False
class Importer:
    pass

class GpwImporter(Importer):
    """A simple importer for gpw.pl archite data"""

    def __init__(self):
        pass

    def import_data_from_gpw(self, date_from, date_to, path):
        for single_date in date_range(date_from, date_to):
            html_data = self.read_single_page(single_date.strftime('%Y-%m-%d'))
            self.save_html_data_to_file(html_data, 
                                        path, single_date.strftime('%Y-%m-%d'))

    def read_single_page(self, date):
        url = 'http://www.gpw.pl/notowania_archiwalne_full?type=10&date=' + date
        page_data = urllib.urlopen(url)
        return page_data.read()

    def save_html_data_to_file(self, html_data, path, file_name):    
        file_path = path + '\\' + file_name + '.html'
        file = open(file_path, 'wb')
        file.writelines(html_data)
        file.close()
        print 'Succesfully saved for ', file_path

    def date_range(self, start_date, end_date):
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(n)

class MoneyPlImporter(Importer):    

    def __init__(self, request_url):
        self.request_url = request_url

    def get_company_data(self, ticker, type, t, run):
        data = urllib.urlencode({"ticker":ticker, "p":type,"t": t,"o":run*4})        
        result = urllib.urlopen("http://www.money.pl/ajax/gielda/finanse/",data).read()        
        return result        

class MoneyPlHtmlParser(HTMLParser):   
   
    def handle_starttag(self, tag, attrs):
        htmlData.append(tag)

    def handle_endtag(self, tag):
        htmlData.append(tag)

    def handle_data(self, data):
        htmlData.append(data)

# Scraping gwp
#files_path = 'C:\Users\lukas_000\Dropbox\TZ&LH&JR exchange\Gambler\GPW_notowania_archiwalne'
#start_date = date(2013,9,2)
#end_date = date(2013,10,22)

#importer = GpwImporter()
#importer.import_data_from_gpw(start_date, end_date, files_path)

htmlData = []
yearly_reports = []
quarterly_reports = []

for i in range(4):
    quarterly_reports.append(FinancialReport())


request_url = "http://www.money.pl/ajax/gielda/finanse/"

importer = MoneyPlImporter(request_url)
parser = MoneyPlHtmlParser()

#scrape
parser.feed(importer.get_company_data("KPX","Q","t",1))

#parse 
index = 0

#find report dates
for i in range(4):
    index = htmlData.index('th')   
    htmlData.pop(index)
    quarterly_reports[i].date = htmlData[index]    
    index = htmlData.index('th')   
    htmlData.pop(index)
   
#revenue_from_sale_of_merchandise_and_raw_materials
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].revenue_from_sale_of_merchandise_and_raw_materials = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].revenue_from_sale_of_merchandise_and_raw_materials    
    index = htmlData.index('td')
    htmlData.pop(index)

#profit_from_operating_activities
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].profit_from_operating_activities = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].profit_from_operating_activities    
    index = htmlData.index('td')
    htmlData.pop(index)

#gross_profit
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].gross_profit = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].gross_profit    
    index = htmlData.index('td')
    htmlData.pop(index)

#net_profit
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].net_profit = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].net_profit    
    index = htmlData.index('td')
    htmlData.pop(index)

#net_flow
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].net_flow = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].net_flow    
    index = htmlData.index('td')
    htmlData.pop(index)

#net_operating_flow
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].net_operating_flow = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].net_operating_flow    
    index = htmlData.index('td')
    htmlData.pop(index)

#net_investments_flow
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].net_investments_flow = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].net_investments_flow    
    index = htmlData.index('td')
    htmlData.pop(index)

#net_financial_flow
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].net_financial_flow = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].net_financial_flow    
    index = htmlData.index('td')
    htmlData.pop(index)

#assets
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].assets = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].assets    
    index = htmlData.index('td')
    htmlData.pop(index)

#liabilities_and_provision_for_liabilities
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].liabilities_and_provision_for_liabilities = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].liabilities_and_provision_for_liabilities    
    index = htmlData.index('td')
    htmlData.pop(index)

#non_current_liabilities
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].non_current_liabilities = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].non_current_liabilities    
    index = htmlData.index('td')
    htmlData.pop(index)

#current_liabilities
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].current_liabilities = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].current_liabilities    
    index = htmlData.index('td')
    htmlData.pop(index)

#owners_equity
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].owners_equity = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].owners_equity    
    index = htmlData.index('td')
    htmlData.pop(index)

#share_capital
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].share_capital = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].share_capital    
    index = htmlData.index('td')
    htmlData.pop(index)

#number_of_shares
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].number_of_shares = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].number_of_shares    
    index = htmlData.index('td')
    htmlData.pop(index)

#book_worth_per_share
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].book_worth_per_share = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].book_worth_per_share    
    index = htmlData.index('td')
    htmlData.pop(index)

#profit_per_share
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].profit_per_share = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].profit_per_share    
    index = htmlData.index('td')
    htmlData.pop(index)

#diluted_number_of_shares
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].diluted_number_of_shares = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].diluted_number_of_shares    
    index = htmlData.index('td')
    htmlData.pop(index)

#diluted_book_worth_per_share
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].diluted_book_worth_per_share = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].diluted_book_worth_per_share    
    index = htmlData.index('td')
    htmlData.pop(index)

#diluted_profit_per_share
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].diluted_profit_per_share = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].diluted_profit_per_share    
    index = htmlData.index('td')
    htmlData.pop(index)

#dividend_per_share
print
for i in range(4):
    index = htmlData.index('td')       
    htmlData.pop(index)
    if Helper.isReal(htmlData[index]):
        quarterly_reports[i].dividend_per_share = ''.join(htmlData[index].strip().split())
    print quarterly_reports[i].dividend_per_share    
    index = htmlData.index('td')
    htmlData.pop(index)

raw_input()

#save