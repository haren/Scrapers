import urllib
import csv
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
        data = urllib.urlencode({"ticker":ticker, "p":type,"t": t,"o":run})        
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
files_path = 'C:\Users\lukas_000\Dropbox\TZ&LH&JR exchange\Gambler\Money_pl_notowania'

request_url = "http://www.money.pl/ajax/gielda/finanse/"

importer = MoneyPlImporter(request_url)
parser = MoneyPlHtmlParser()


#scrape
counter = 0
while True:
    htmlData = []
    
    parser.feed(importer.get_company_data("KPX", "Y", "t", counter))
    
    if (len (htmlData) < 50):
        break
    else:
        
        #parse 
        index = 0

        #find report dates, check how many reports on page and prepare objects for reports
        for i in range(4):
            if 'th' in htmlData:
                index = htmlData.index('th')   
                htmlData.pop(index)
                quarterly_reports.append(FinancialReport())
                quarterly_reports[counter + i].date = htmlData[index]
                print htmlData[index]
                index = htmlData.index('th')   
                htmlData.pop(index)
            else:
                break

        reports_on_page = i + 1 if i == 3 else i
        
        #revenue_from_sale_of_merchandise_and_raw_materials
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].revenue_from_sale_of_merchandise_and_raw_materials = ''.join(htmlData[index].strip().split())
            index = htmlData.index('td')
            htmlData.pop(index)

        #profit_from_operating_activities
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].profit_from_operating_activities = ''.join(htmlData[index].strip().split())    
            index = htmlData.index('td')
            htmlData.pop(index)

        #gross_profit
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].gross_profit = ''.join(htmlData[index].strip().split()) 
            index = htmlData.index('td')
            htmlData.pop(index)

        #net_profit
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].net_profit = ''.join(htmlData[index].strip().split())    
            index = htmlData.index('td')
            htmlData.pop(index)

        #net_flow
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].net_flow = ''.join(htmlData[index].strip().split())  
            index = htmlData.index('td')
            htmlData.pop(index)

        #net_operating_flow
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].net_operating_flow = ''.join(htmlData[index].strip().split())
            index = htmlData.index('td')
            htmlData.pop(index)

        #net_investments_flow
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].net_investments_flow = ''.join(htmlData[index].strip().split())
            index = htmlData.index('td')
            htmlData.pop(index)

        #net_financial_flow
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].net_financial_flow = ''.join(htmlData[index].strip().split())
            index = htmlData.index('td')
            htmlData.pop(index)

        #assets
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].assets = ''.join(htmlData[index].strip().split())
            index = htmlData.index('td')
            htmlData.pop(index)

        #liabilities_and_provision_for_liabilities
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].liabilities_and_provision_for_liabilities = ''.join(htmlData[index].strip().split())
            index = htmlData.index('td')
            htmlData.pop(index)

        #non_current_liabilities
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].non_current_liabilities = ''.join(htmlData[index].strip().split())
            index = htmlData.index('td')
            htmlData.pop(index)

        #current_liabilities
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].current_liabilities = ''.join(htmlData[index].strip().split())
            index = htmlData.index('td')
            htmlData.pop(index)

        #owners_equity
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].owners_equity = ''.join(htmlData[index].strip().split())
            index = htmlData.index('td')
            htmlData.pop(index)

        #share_capital
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].share_capital = ''.join(htmlData[index].strip().split())
            index = htmlData.index('td')
            htmlData.pop(index)

        #number_of_shares
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].number_of_shares = ''.join(htmlData[index].strip().split())
            index = htmlData.index('td')
            htmlData.pop(index)

        #book_worth_per_share        
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].book_worth_per_share = ''.join(htmlData[index].strip().split())
            index = htmlData.index('td')
            htmlData.pop(index)

        #profit_per_share
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].profit_per_share = ''.join(htmlData[index].strip().split())
            index = htmlData.index('td')
            htmlData.pop(index)

        #diluted_number_of_shares
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].diluted_number_of_shares = ''.join(htmlData[index].strip().split())
            index = htmlData.index('td')
            htmlData.pop(index)

        #diluted_book_worth_per_share
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].diluted_book_worth_per_share = ''.join(htmlData[index].strip().split())
            index = htmlData.index('td')
            htmlData.pop(index)

        #diluted_profit_per_share
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].diluted_profit_per_share = ''.join(htmlData[index].strip().split())
            index = htmlData.index('td')
            htmlData.pop(index)

        #dividend_per_share
        for i in range(reports_on_page):
            index = htmlData.index('td')       
            htmlData.pop(index)
            if Helper.isReal(htmlData[index]):
                quarterly_reports[counter + i].dividend_per_share = ''.join(htmlData[index].strip().split())
            index = htmlData.index('td')
            htmlData.pop(index)

        counter += 4

#save to csv file
try:
    with open(r'C:\Users\lukas_000\Dropbox\TZ&LH&JR exchange\Gambler\Money_pl_notowania\KOPEX_Q.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter = ';', quotechar='|', quoting = csv.QUOTE_MINIMAL)

        writer.writerow([quarterly_reports[i].date for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].revenue_from_sale_of_merchandise_and_raw_materials 
                         if quarterly_reports[i].revenue_from_sale_of_merchandise_and_raw_materials != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].profit_from_operating_activities 
                         if quarterly_reports[i].profit_from_operating_activities != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].gross_profit 
                         if quarterly_reports[i].gross_profit != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].net_profit 
                         if quarterly_reports[i].net_profit != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].net_flow 
                         if quarterly_reports[i].net_flow != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].net_operating_flow 
                         if quarterly_reports[i].net_operating_flow != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].net_investments_flow 
                         if quarterly_reports[i].net_investments_flow != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].net_financial_flow 
                         if quarterly_reports[i].net_financial_flow != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].assets 
                         if quarterly_reports[i].assets != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].liabilities_and_provision_for_liabilities 
                         if quarterly_reports[i].liabilities_and_provision_for_liabilities != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].non_current_liabilities 
                         if quarterly_reports[i].non_current_liabilities != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].current_liabilities 
                         if quarterly_reports[i].current_liabilities != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].owners_equity 
                         if quarterly_reports[i].owners_equity != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].share_capital 
                         if quarterly_reports[i].share_capital != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].current_liabilities 
                         if quarterly_reports[i].current_liabilities != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].number_of_shares 
                         if quarterly_reports[i].number_of_shares != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].book_worth_per_share 
                         if quarterly_reports[i].book_worth_per_share != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].profit_per_share 
                         if quarterly_reports[i].profit_per_share != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].diluted_number_of_shares 
                         if quarterly_reports[i].diluted_number_of_shares != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].diluted_book_worth_per_share 
                         if quarterly_reports[i].diluted_book_worth_per_share != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].diluted_profit_per_share 
                         if quarterly_reports[i].diluted_profit_per_share != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        writer.writerow([quarterly_reports[i].dividend_per_share 
                         if quarterly_reports[i].dividend_per_share != FinancialReport.DEFAULT_VALUE else '' for i in range(len(quarterly_reports))])
        
except:
    print "Failed to open file: KOPEX_Q.csv"

raw_input()

#save