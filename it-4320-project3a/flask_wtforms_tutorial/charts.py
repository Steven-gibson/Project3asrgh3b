'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
from tracemalloc import start
import requests
import logging
#import lxml
import pygal
from datetime import datetime
from datetime import date
from datetime import timedelta
#from datetime import date
import sys
import math
# from dateutil.relativedelta import relativedelta
from json import JSONDecodeError
from flask import Flask, request, render_template


#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()


def getDateRange(start, end, time_series):
        if time_series == "1":
            #time_series = "INTRADAY"
            start_date = str(start).split("-")
            end_date = str(end).split("-")
            start_date = datetime(int(start_date[0]), int(start_date[1]), int(start_date[2]), 0, 0, 0)
            end_date = datetime(int(end_date[0]), int(end_date[1]), int(end_date[2]), 20, 0, 0)
            dateRange = []
            delta = timedelta(minutes=5)
            while (start_date <= end_date):
                day = str(start_date.year) +'-'+str(start_date.month)+'-'+str(start_date.day) + " " + str(start_date.hour) +":"+ str(start_date.minute) + ":00"
                dateRange.append(day)
                start_date += delta
            return dateRange

        start_date = str(start).split("-")
        end_date = str(end).split("-")
        start_date = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
        end_date = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
        dateRange = []
        delta = timedelta(days=1)
        while (start_date <= end_date):
            day = str(start_date.year) +'-'+str(start_date.month)+'-'+str(start_date.day)
            dateRange.append(day)
            start_date += delta
        return dateRange

#Query the api
def apiCall(time_series,symbol):
    if time_series == "1":
        timeSeries = "INTRADAY"
        #https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=GOOGL&interval=5min&outputsize=full&apikey=TJ5UI0CUVXDLAV9K
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_' + timeSeries + '&symbol='+ symbol +'&outputsize=full&interval=5min&apikey=TJ5UI0CUVXDLAV9K'
        r = requests.get(url)
        data = r.json()
        return data

    if time_series == "2":
        timeSeries = "DAILY_ADJUSTED"
        # https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=GOOGL&outputsize=full&apikey=TJ5UI0CUVXDLAV9K
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_' + timeSeries + '&symbol='+ symbol +'&outputsize=full&interval=5min&apikey=TJ5UI0CUVXDLAV9K'
        r = requests.get(url)
        data = r.json()
        return data

    if time_series == "3":
        timeSeries = "WEEKLY"
        #url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=GOOGL&outputsize=full&apikey=TJ5UI0CUVXDLAV9K'
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_' + timeSeries + '&symbol='+ symbol +'&outputsize=full&interval=5min&apikey=TJ5UI0CUVXDLAV9K'
        r = requests.get(url)
        data = r.json()
        return data

    if time_series == "4":
        timeSeries = "MONTHLY"
        # https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=GOOGL&outputsize=full&apikey=TJ5UI0CUVXDLAV9K
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_' + timeSeries + '&symbol='+ symbol +'&outputsize=full&interval=5min&apikey=TJ5UI0CUVXDLAV9K'
        r = requests.get(url)
        data = r.json()
        return data

#process for data
def parseJSON(rawJSON, time_series, dateRange):
        jsonDateRange = []
        xLabels = []

        if time_series == "1":
            #time_series = "INTRADAY"
            for date in dateRange:
                try:
                    splitEntry = date.split(' ')
                    splitTime = splitEntry[1].split(':')
                    hour = splitTime[0].zfill(2)
                    minute = splitTime[1].zfill(2)
                    second = splitTime[2].zfill(2)
                    splitDate = splitEntry[0].split('-')
                    month = splitDate[1].zfill(2)
                    day = splitDate[2].zfill(2)
                    date = splitDate[0] + '-' + month + '-' + day
                    date = date + " " + hour + ":" + minute + ":" + second
                    #print("\n",date)
                    jsonDateRange.append(rawJSON['Time Series (5min)'][date])
                    xLabels.append(date)
                except KeyError:
                    continue
            buildGraph={"jsonDateRange":jsonDateRange, "xLabels":xLabels}

            return buildGraph

        if time_series == "2":
            #time_series = "DAILY_ADJUSTED"
            for date in dateRange:
                try:
                    splitDate = date.split('-')
                    day = date.split('-')[2].zfill(2)
                    date = splitDate[0] +'-'+splitDate[1].zfill(2)+'-'+ day
                    jsonDateRange.append(rawJSON['Time Series (Daily)'][date])
                    xLabels.append(date)
                except KeyError:
                    continue
            buildGraph = {"jsonDateRange":jsonDateRange, "xLabels":xLabels}

            return buildGraph

        if time_series == "3":
            #timeSeries == "WEEKLY"
            for date in dateRange:
                try:
                    splitDate = date.split('-')
                    day = date.split('-')[2].zfill(2)
                    date = splitDate[0] +'-'+splitDate[1].zfill(2)+'-'+ day
                    jsonDateRange.append(rawJSON['Weekly Time Series'][date])
                    xLabels.append(date)
                except KeyError:
                    continue
            buildGraph = {"jsonDateRange":jsonDateRange, "xLabels":xLabels}
            return buildGraph

        if time_series == "4":
            #timeSeries == "MONTHLY"
            for date in dateRange:
                try:
                    splitDate = date.split('-')
                    day = date.split('-')[2].zfill(2)
                    date = splitDate[0] +'-'+splitDate[1].zfill(2)+'-'+ day
                    jsonDateRange.append(rawJSON['Monthly Time Series'][date])
                    xLabels.append(date)
                except KeyError:
                    continue
            buildGraph = {"jsonDateRange":jsonDateRange, "xLabels":xLabels}
            return buildGraph


#build graph
def createGraph(jsonDateRange, time_series,xLabels, start, end,chart_type):
    # TODO append date range to title as well
    # TODO capture lowest and highest range in the data so can use map()
    logging.error("Eroor 165")
    openList = []
    highList = []
    lowList = []
    closeList = []
    volumeList = []
    #print(jsonDateRange[0])
    logging.error("before list")
    logging.error(""+time_series+"")
    categories = list(jsonDateRange[0].keys())
    logging.error("After list")
    if time_series == "1":
        #if time_series == "1":
        title = "Time Series (Intraday) " + start + " - " + end
    if time_series == "2":
        #if time_series == "2":
        title = "Time Series (Daily) " + start + " - " + end
    if time_series == "3":
        #if time_series == "3":
        title = "Weekly Time Series " + start + " - " + end
    if time_series == "4":
        #if time_series == "4":
        title = "Monthly Time Series " + start + " - " + end
    logging.error("Error 188")
    minimum = 9999999
    maximum = 0
    for entry in jsonDateRange:
        if float(entry['3. low']) < minimum:
            minimum = float(entry['3. low'])
    for entry in jsonDateRange:
        if float(entry['2. high']) > maximum:
            maximum = float(entry['2. high'])
    for i in range(0,len(jsonDateRange)-1):
        openList.append(float(jsonDateRange[i]['1. open']))
        highList.append(float(jsonDateRange[i]['2. high']))
        lowList.append(float(jsonDateRange[i]['3. low']))
        closeList.append(float(jsonDateRange[i]['4. close']))
        #volumeList.append(float(jsonDateRange[i]['5. volume']))
    logging.error("Error 203")
    if chart_type == "1":
        bar_chart = pygal.Bar(x_label_rotation=90)
        bar_chart.title = title
        bar_chart.x_labels = xLabels
            #line_chart.y_labels = map(str, range(math.floor(minimum), math.ceil(maximum)))
        bar_chart.add(categories[0], openList)
        bar_chart.add(categories[1], highList)
        bar_chart.add(categories[2], lowList)
        bar_chart.add(categories[3], closeList)
            #line_chart.add(categories[4], volumeList)
        graph = bar_chart.render_data_uri()
        return graph
    logging.error("Error 216")
    if chart_type == "2":
        line_chart = pygal.Line(x_label_rotation=35)
        line_chart.title = title
        line_chart.x_labels = xLabels
            #line_chart.y_labels = map(str, range(math.floor(minimum), math.ceil(maximum)))
        line_chart.add(categories[0], openList)
        line_chart.add(categories[1], highList)
        line_chart.add(categories[2], lowList)
        line_chart.add(categories[3], closeList)
            #line_chart.add(categories[4], volumeList)
        graph = line_chart.render_data_uri()
        return graph



def generation(time_series, symbol,start_date, end_date,chart_type):
    
    start_date = convert_date(str(start_date))
    end_date = convert_date(str(end_date))
    dateRange = getDateRange(start_date, end_date,time_series)
    data = apiCall(time_series,symbol)

    buildGraph = parseJSON(data, time_series, dateRange)
    jsonDateRange = buildGraph["jsonDateRange"]
    xLabels = buildGraph["xLabels"]

    chart = createGraph(jsonDateRange, time_series,xLabels, str(start_date), str(end_date),chart_type)
    return chart

    #print(data["Monthly Time Series"]["2022-10-20"])