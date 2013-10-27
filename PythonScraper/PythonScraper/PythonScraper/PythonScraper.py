from datetime import date, timedelta
from time import strftime

from gpw_importer import GpwImporter
from money_pl_importer import MoneyPlImporter, MoneyPlReportParser, MoneyPlCompanyListParser

if __name__ == '__main__':        
    # Scraping gwp
    #files_path = 'C:\Users\lukas_000\Dropbox\TZ&LH&JR exchange\Gambler\GPW_notowania_archiwalne'
    #gpw_url = 'http://www.gpw.pl/notowania_archiwalne_full?type=10&date='
    #start_date = date(2013,9,2)
    #end_date = date(2013,10,22)

    #importer = GpwImporter()
    #importer.import_data_from_gpw(gpw_url, start_date, end_date, files_path)


    # Scraping money pl 
    # todo - gpw vs money pl as input param    
    company_list = []
    failed = []
    files_path = r"C:\Users\lukas_000\Dropbox\TZ&LH&JR exchange\Gambler\Money_pl_notowania\\"
    money_pl_request_url = "http://www.money.pl/ajax/gielda/finanse/"
    money_pl_company_list_url = "http://www.money.pl/gielda/gpw/akcje/"

    report_parser = MoneyPlReportParser()
    list_parser = MoneyPlCompanyListParser()
    importer = MoneyPlImporter(money_pl_request_url)

    scraped_companies = importer.get_scraped_companies(files_path)
    
    company_list = importer.import_company_list(list_parser, money_pl_company_list_url)
    
    for company in company_list:    
        # if company[0] not in scraped_companies:
        try:   
            # todo: spawn a new thread for each import, kill after n seconds
            importer.import_company_data(report_parser, files_path, company[0], company[1], "Q", "t")
            importer.import_company_data(report_parser, files_path, company[0], company[1], "Y", "t")
        except Exception, e:
            print ("Failed for " + company[0])
            print e
            print ("Trying jednostkowe instead ;)")
            try:
                importer.import_company_data(report_parser, files_path, company[0], company[1], "Q", "f")
                importer.import_company_data(report_parser, files_path, company[0], company[1], "Y", "f")
            except Exception, e:
                print ("Failed miserable for company " + company[0])
                print e
                failed.append(company) 
                 
    importer.save_missing_comapnies_to_csv(files_path, failed)
    raw_input()