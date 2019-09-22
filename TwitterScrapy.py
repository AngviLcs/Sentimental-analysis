
from twitterscraper import query_tweets
from datetime import datetime
import xlrd
import xlwt
from xlutils.copy import copy
from time import time



def scrapyTweets(keywords,book_name_xls,sheet_name_xls,datanumber,startdate):
    start = time()
    totalNum = 0
    data = []
    value_title = [["username", "fullname", "user_id", "tweet_id", "tweet_url","text","timestamp", "replies", "retweets","is_retweet","retweeter_username", "retweet_id"],]
    write_excel_xls(book_name_xls, sheet_name_xls, value_title)
    for tweet in query_tweets(keywords,datanumber)[:datanumber]:
        tempList = []
        if(checkTime(str(tweet.timestamp),startdate)):
            totalNum = totalNum + 1
            appendToList(tweet, tempList)
            data.append(tempList)
        if(len(data)>5000):
            write_excel_xls_append(book_name_xls, data)
            data = []
        
    
    write_excel_xls_append(book_name_xls, data)
    
    end = time()
    totalTime = end - start        
    
    return totalNum,totalTime
    
    
def appendToList(tweet,list):
    list.append(str(tweet.username))
    list.append(str(tweet.fullname))
    list.append(str(tweet.user_id))
    list.append(str(tweet.tweet_id))
    list.append(str(tweet.tweet_url))
    list.append(str(tweet.text))
    list.append(str(tweet.timestamp))
    list.append(str(tweet.replies))
    list.append(str(tweet.retweets))
    list.append(str(tweet.is_retweet))
    list.append(str(tweet.retweeter_username))
    list.append(str(tweet.retweet_id))
    

def checkTime(timestamp,startdate):
    startdate = startdate + " 00:00:00"
    time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    startday = datetime.strptime(startdate, '%Y-%m-%d %H:%M:%S')
    if (time>=startday):
        return True
    else:
        return False


# coding=UTF-8
def write_excel_xls(path, sheet_name, value):
    index = len(value)  
    workbook = xlwt.Workbook()  
    sheet = workbook.add_sheet(sheet_name)  
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  
    workbook.save(path)  
    print("Successfully create")
 
 
def write_excel_xls_append(path, value):
    index = len(value)  
    workbook = xlrd.open_workbook(path) 
    sheets = workbook.sheet_names()  
    worksheet = workbook.sheet_by_name(sheets[0])  
    rows_old = worksheet.nrows  
    new_workbook = copy(workbook) 
    new_worksheet = new_workbook.get_sheet(0)  
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i+rows_old, j, value[i][j])  
    new_workbook.save(path)  
    print("Successfully append")

def searchFile(fileAdd,sheet_name_xls,datanumber,startdate,sourceFile):
    workbook = xlrd.open_workbook(sourceFile)  
    sheets = workbook.sheet_names() 
    worksheet = workbook.sheet_by_name(sheets[0])
    for i in range(0, worksheet.nrows):
        if(i==0):
            print("******"*50)
        else:
            for j in range(0, worksheet.ncols):
                keyword = str(worksheet.cell_value(i, j))
                print(keyword)
                if(j==0):
                    book_name_xls = fileAdd+"Article__"+str(i)+'.xls'
                elif(j==1):
                    book_name_xls = fileAdd+"URL__"+str(i)+'.xls'
                num1,time1 = scrapyTweets(keyword,book_name_xls,sheet_name_xls,datanumber,startdate)



