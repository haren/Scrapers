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

    def import_data_from_gpw(self, url, date_from, date_to, path):
        for single_date in date_range(date_from, date_to):
            html_data = self.read_single_page(url, single_date.strftime('%Y-%m-%d'))
            self.save_html_data_to_file(html_data, 
                                        path, single_date.strftime('%Y-%m-%d'))

    def read_single_page(self, url, date):
        url = url + date
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
        #self.parser = parser

    def import_company_data(self, parser, files_path, company_name, ticker, type, t):
        self.get_company_data(parser, ticker, type, t)
        self.save_data_to_csv(files_path, company_name, type)  

    def import_company_list(self, parser, list_url):
        print "Started company list import."
        page_data = self.scrape_comany_list(list_url)
        list = self.get_company_list(parser, page_data)
        print "Finished company list import."
        return list

    def scrape_comany_list(self, list_url):
        return urllib.urlopen(list_url).read()

    def scrape_company_data(self, ticker, type, t, run):
        data = urllib.urlencode({"ticker":ticker, "p":type,"t": t,"o":run})        
        result = urllib.urlopen("http://www.money.pl/ajax/gielda/finanse/",data).read()        
        return result
    
    def get_company_data(self, parser, ticker, type, t):
        global htmlData

        counter = 0

        print "Started scraping for ", ticker, " ", type
                
        while True:
            htmlData = []
    
            # parser should be a composition in this class, doesn't work though
            parser.feed(self.scrape_company_data(ticker, type, t, counter))
            
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
                        reports.append(FinancialReport())
                        reports[counter + i].date = htmlData[index]
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
                        reports[counter + i].revenue_from_sale_of_merchandise_and_raw_materials = ''.join(htmlData[index].strip().split())
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #profit_from_operating_activities
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].profit_from_operating_activities = ''.join(htmlData[index].strip().split())    
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #gross_profit
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].gross_profit = ''.join(htmlData[index].strip().split()) 
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #net_profit
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].net_profit = ''.join(htmlData[index].strip().split())    
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #net_flow
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].net_flow = ''.join(htmlData[index].strip().split())  
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #net_operating_flow
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].net_operating_flow = ''.join(htmlData[index].strip().split())
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #net_investments_flow
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].net_investments_flow = ''.join(htmlData[index].strip().split())
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #net_financial_flow
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].net_financial_flow = ''.join(htmlData[index].strip().split())
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #assets
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].assets = ''.join(htmlData[index].strip().split())
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #liabilities_and_provision_for_liabilities
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].liabilities_and_provision_for_liabilities = ''.join(htmlData[index].strip().split())
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #non_current_liabilities
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].non_current_liabilities = ''.join(htmlData[index].strip().split())
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #current_liabilities
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].current_liabilities = ''.join(htmlData[index].strip().split())
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #owners_equity
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].owners_equity = ''.join(htmlData[index].strip().split())
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #share_capital
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].share_capital = ''.join(htmlData[index].strip().split())
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #number_of_shares
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].number_of_shares = ''.join(htmlData[index].strip().split())
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #book_worth_per_share        
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].book_worth_per_share = ''.join(htmlData[index].strip().split())
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #profit_per_share
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].profit_per_share = ''.join(htmlData[index].strip().split())
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #diluted_number_of_shares
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].diluted_number_of_shares = ''.join(htmlData[index].strip().split())
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #diluted_book_worth_per_share
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].diluted_book_worth_per_share = ''.join(htmlData[index].strip().split())
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #diluted_profit_per_share
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].diluted_profit_per_share = ''.join(htmlData[index].strip().split())
                    index = htmlData.index('td')
                    htmlData.pop(index)

                #dividend_per_share
                for i in range(reports_on_page):
                    index = htmlData.index('td')       
                    htmlData.pop(index)
                    if Helper.isReal(htmlData[index]):
                        reports[counter + i].dividend_per_share = ''.join(htmlData[index].strip().split())
                    index = htmlData.index('td')
                    htmlData.pop(index)

                counter += 4

        print "Finished scraping successfully for ", ticker, " ", type

    def get_company_list(self, parser, page_data):
        global htmlData
        parser.feed(page_data)      
  
        company_tickers = []
        company_names = []

        while htmlData:
            single_cell = htmlData.pop(0)
            if single_cell == 'a':
                single_cell = htmlData.pop(0)
                if htmlData:
                    if single_cell and isinstance(single_cell, list):                        
                        if isinstance(single_cell[0], tuple):
                          if single_cell[0][0] == 'class':
                              if single_cell[0][1] == 'link':
                                company_names.append(htmlData.pop(0))
            elif single_cell == 'td':
                single_cell = htmlData.pop(0)
                if htmlData:
                    if single_cell and isinstance(single_cell, list):                        
                        if isinstance(single_cell[0], tuple):
                          if single_cell[0][0] == 'class':
                              if single_cell[0][1] == 'al':
                                  single_cell = htmlData.pop(0)
                                  if len(single_cell) == 3 and single_cell != 'GNB': # getin noble bank screwed up on webpage, unimportant anyway for now
                                    company_tickers.append(single_cell)

        htmlData = []
        return zip(company_names, company_tickers)
        
    def save_data_to_csv(self, path, company_name, type):
        global reports
        try:
            print "Started saving for ", company_name, " ", type

            full_path = path + company_name + '_' + type + '.csv'
            
            with open(full_path, 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter = ';', quotechar='|', quoting = csv.QUOTE_MINIMAL)

                writer.writerow([reports[i].date for i in range(len(reports))])
                writer.writerow([reports[i].revenue_from_sale_of_merchandise_and_raw_materials 
                                 if reports[i].revenue_from_sale_of_merchandise_and_raw_materials != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].profit_from_operating_activities 
                                 if reports[i].profit_from_operating_activities != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].gross_profit 
                                 if reports[i].gross_profit != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].net_profit 
                                 if reports[i].net_profit != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].net_flow 
                                 if reports[i].net_flow != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].net_operating_flow 
                                 if reports[i].net_operating_flow != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].net_investments_flow 
                                 if reports[i].net_investments_flow != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].net_financial_flow 
                                 if reports[i].net_financial_flow != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].assets 
                                 if reports[i].assets != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].liabilities_and_provision_for_liabilities 
                                 if reports[i].liabilities_and_provision_for_liabilities != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].non_current_liabilities 
                                 if reports[i].non_current_liabilities != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].current_liabilities 
                                 if reports[i].current_liabilities != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].owners_equity 
                                 if reports[i].owners_equity != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].share_capital 
                                 if reports[i].share_capital != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].current_liabilities 
                                 if reports[i].current_liabilities != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].number_of_shares 
                                 if reports[i].number_of_shares != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].book_worth_per_share 
                                 if reports[i].book_worth_per_share != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].profit_per_share 
                                 if reports[i].profit_per_share != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].diluted_number_of_shares 
                                 if reports[i].diluted_number_of_shares != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].diluted_book_worth_per_share 
                                 if reports[i].diluted_book_worth_per_share != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].diluted_profit_per_share 
                                 if reports[i].diluted_profit_per_share != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])
                writer.writerow([reports[i].dividend_per_share 
                                 if reports[i].dividend_per_share != FinancialReport.DEFAULT_VALUE else '' for i in range(len(reports))])    
            
            reports = []
            print "Finished saving for ", company_name, " ", type

        except:
            print "Error while saving to file: ", full_path
           
class MoneyPlReportParser(HTMLParser):   
   
    def handle_starttag(self, tag, attrs):
        htmlData.append(tag)

    def handle_endtag(self, tag):
        htmlData.append(tag)

    def handle_data(self, data):
        htmlData.append(data)

class MoneyPlCompanyListParser(HTMLParser):   
   
    def handle_starttag(self, tag, attrs):
        htmlData.append(tag)
        htmlData.append(attrs)

    def handle_endtag(self, tag):
        htmlData.append(tag)

    def handle_data(self, data):
        htmlData.append(data)

# Scraping gwp
#files_path = 'C:\Users\lukas_000\Dropbox\TZ&LH&JR exchange\Gambler\GPW_notowania_archiwalne'
#gpw_url = 'http://www.gpw.pl/notowania_archiwalne_full?type=10&date='
#start_date = date(2013,9,2)
#end_date = date(2013,10,22)

#importer = GpwImporter()
#importer.import_data_from_gpw(gpw_url, start_date, end_date, files_path)

if __name__ == '__main__':
    htmlData = []
    reports = []
    company_list = []
    files_path = r"C:\Users\lukas_000\Dropbox\TZ&LH&JR exchange\Gambler\Money_pl_notowania\\"
    money_pl_request_url = "http://www.money.pl/ajax/gielda/finanse/"
    money_pl_company_list_url = "http://www.money.pl/gielda/gpw/akcje/"

    report_parser = MoneyPlReportParser()
    list_parser = MoneyPlCompanyListParser()
    importer = MoneyPlImporter(money_pl_request_url)

    company_list = importer.import_company_list(list_parser, money_pl_company_list_url)
    for company in company_list:
        importer.import_company_data(report_parser, files_path, company[0], company[1], "Q", "t")
        importer.import_company_data(report_parser, files_path, company[0], company[1], "Y", "t")
      
    raw_input()