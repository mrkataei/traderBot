from client import ClientBinance , Agent
import datetime
from xlwt import Workbook
class Account(ClientBinance):
    __balance = 0
    __name = ""
    __transaction = []
    def __init__(self , balance:float , name:str , api_key:str , api_secret:str):
        super(Account, self).__init__(api_key , api_secret )
        self.__balance = balance
        self.__name = name

    def get_balance(self):
        return self.__balance
    def details_toString(self):

        print("name:" + self.__name + "\n"+ "balance:" + str(self.__balance) + "$")
    def transaction(self , value:float):
        op = '+' if  value > 0 else '-'
        if op=='-' and abs(value) > self.__balance :
            print("not enough money")
            return
        else:
            self.__balance = value + self.__balance
            temp = {'timeStamp':datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") ,'value':value , 'operation': op ,'balance':self.__balance}
            self.__transaction.append(temp)
    def get_transaction(self):
        return self.__transaction
    def export_to_excel(self , filename:str):
        wb = Workbook()
        sheet1 = wb.add_sheet('Demo transaction')
        sheet1.write(0, 0, 'Transaction Time')
        sheet1.write(0, 1, 'Balance')
        sheet1.write(0, 2, 'Value')
        sheet1.write(0, 3, 'Operation')

        for index , item in enumerate(self.__transaction , start=1):
            sheet1.write(index, 0, item['timeStamp'] )
            sheet1.write(index, 1, item['balance'])
            sheet1.write(index, 2, abs(item['value']))
            sheet1.write(index, 3, 'Deposit' if item['operation']== '+' else 'Withdraw')

        wb.save(filename+'.xls')