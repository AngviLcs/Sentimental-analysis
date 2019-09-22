import tkinter as tk
from TwitterScrapy import scrapyTweets
from TwitterScrapy import searchFile



window = tk.Tk()
window.title("Twitter Scraper")
window.geometry('650x400')
keywords = tk.StringVar()
fileaddress = tk.StringVar()
datanumber = tk.IntVar()
startDate = tk.StringVar()
sourceFile = tk.StringVar()


tk.Label(window,text = "Twitter Scraper").pack()
tk.Label(window,text ='Keyword').pack()
e1 = tk.Entry(window,textvariable = keywords, width = 30).pack()
tk.Label(window,text ='File location').pack()
e2 = tk.Entry(window,textvariable = fileaddress, width = 30).pack()
tk.Label(window,text ='Source file location').pack()
e5 = tk.Entry(window,textvariable = sourceFile, width = 30).pack()
tk.Label(window,text ='Start date, YY-MM-DD').pack()
e4 = tk.Entry(window,textvariable = startDate, width = 8).pack()
tk.Label(window,text ='Maximum Number of Tweets').pack()
e3 = tk.Entry(window,textvariable = datanumber, width = 8).pack()

def action():
    key = keywords.get()
    fileAdd = fileaddress.get()
    number = datanumber.get()
    startdate = startDate.get()
    article = key
    article.replace(":","-")
    article.replace("/","-")
    book_name_xls = fileAdd+article+'.xls'
    sheet_name_xls = "sheet 1"
    t= tk.StringVar() 
    t.set("Running Please Do Not Close...")
    running = tk.Label(window,text=t.get(),font = (16)).pack()
    window.update() 
    total,time = scrapyTweets(key,book_name_xls,sheet_name_xls,number,startdate)
    running.destroy()
    tk.Label(window,text="Successfully! "+str(total)+" tweets appended. "+str(time)+" s",font = (16)).pack()
    print(total)
   
def action1():
    fileAdd = fileaddress.get()
    number = datanumber.get()
    startdate = startDate.get()
    sourcefile = sourceFile.get() 
    sheet_name_xls = "sheet 1"
    t1= tk.StringVar() 
    t1.set("Running Please Do Not Close...")
    running = tk.Label(window,text=t1.get(),font = (16)).pack()
    window.update()
    searchFile(fileAdd,sheet_name_xls, number, startdate, sourcefile)
    running.destroy()
    tk.Label(window,text="Successfully!",font = (16)).pack()
    
    
c = tk.Button(window,text = 'Search Keywords',width = 15,command = action).pack()
c = tk.Button(window,text = 'Search Files',width = 15,command = action1).pack()



window.mainloop()
