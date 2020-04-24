
""" A online multi compiler program """

from requests import Session
from sys import argv

class CompileMe():
    def __init__(self):
           """ header for the request """
           self.__header={ "path":"/main.php",
                        "scheme":"https",
                        "accept":"application/json,text/javascript, */*; q=0.01",
                        "accept-encoding":"gzip, deflate, br",
                        "accept-language":"en-US,en;q=0.9,ta-IN;q=0.8,ta;q=0.7",
                        "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
                        "origin":"https://ide.geeksforgeeks.org",
                        "refere":"https://ide.geeksforgeeks.org/",
                        "sec-fetch-dest":"empty",
                        "sec-fetch-mode":"cors",
                        "sec-fetch-site":"same-origin",
                        "user-agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
                        "x-requested-with":"XMLHttpRequest"}
           self.input=""
           self.start()
           
    def langsupport(self):
        print("\nTO compile your code compileme.py  script.(py,c,cpp..) input.txt(optional)\n\nYou can give input  for your program in seperate file(.txt) each input in new line")
        print("\nLanguage Supports \n1.c \n2.c++ \n3.java \n4.python\n5.c# \n6.scala \n7.perl ")
            
    def start(self):
        """ geting and evaluating the cmd line input """
        file_ext=""
        try:
            arg=argv[1]
            file_ext=argv[1].split(".")[1]
        except IndexError as error:
                self.langsupport()
                return 
        lang_ext={"py":"python","c":"c","cpp":"cpp","cs":"Csharp","java":"java","sc":"scala","scala":"scala","pl":"perl"}
        if(lang_ext.get(file_ext,0)):
           self.lang=lang_ext[file_ext]
           
           if(self.open_file(argv[1])):
               self.compileit()
            
        else:
            print("Unable to compile "+file_ext+" type file ")
            self.langsupport()
            
    def open_file(self,filename):
          """ open the src code file and read it """
          try:
              fp=open(filename,"r")
              self.code=fp.read()
          except FileNotFoundError as e:
              print("Source File not found in current working directory")
              return False
          try:
            
              if(len(argv)==3):
                  fp=open(argv[2],"r")
                  self.input=fp.read()
                
          except FileNotFoundError as e:
              print("Input file not found in current working directory")
              return False
          return True
            
    def compileit(self):
        """ compile the progam using geeksforgeeks api """
        se=Session()
        data={"lang":self.lang  ,"code":self.code ,"input":self.input, "save":"false"}     
        try:
            outputid=se.post("https://ide.geeksforgeeks.org/main.php",data=data,headers=self.__header)
            
            """ looping until the status until it sucess"""
            if(outputid.json()["status"]=="SUCCESS"):
                    data2={"sid":outputid.json()["sid"],"requestType":"fetchResults"}
                    output_json=se.post("https://ide.geeksforgeeks.org/submissionResult.php",data=data2)
                    while(output_json.json()['status']== 'IN-QUEUE'):
                       output_json=se.post("https://ide.geeksforgeeks.org/submissionResult.php",data=data2)
        except:
            print("\n \t No Internet Connection")
            return 

        """ output in json fromat"""
        output=output_json.json()
        if(output.get("output",0)):
            print(output["output"])
            if(output.get("warning",0)):
                          print("WARNNING:\n"+output["warning"])
            
        elif(output.get("cmpError",0)):
                    print("CompilerError:\n"+output["cmpError"])                     
        elif(output.get("rntError",0)):
            print("runtimeerror:\n"+output["rntError"])
CompileMe()
