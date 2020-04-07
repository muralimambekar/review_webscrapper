#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 00:20:14 2020

@author: murali ambekar
"""
# doing necessary imports

from flask import Flask, render_template, request,jsonify
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import csv
from flask import send_file

app = Flask(__name__)

@app.route('/')  # route to display the home page

def homePage():
    return render_template("index.html")

@app.route('/r',methods=['POST','GET']) # route to show the review comments in a web UI

def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "bhgxx2 col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(productLink)
           
            prod_html = bs(prodRes.text, "html.parser")
            print(prod_html)
            commentboxes = prod_html.find_all('div', {'class': "_3nrCtb"})
            
            with open("static/data1.csv","w", newline="") as csvfile:
                fieldnames=["Product","Name", "Rating", "CommentHead","Comment"]
                thewriter=csv.DictWriter(csvfile, fieldnames=fieldnames)
                thewriter.writeheader()
            
            reviews = []
            for commentbox in commentboxes:
                try:
                    
                    name = commentbox.div.div.find_all('p', {'class': '_3LYOAd _3sxSiS'})[0].text

                except:
                    name = 'No Name'

                try:
                    
                    rating = commentbox.div.div.div.div.text


                except:
                    rating = 'No Rating'

                try:
                    
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    
                    custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ",e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                with open("static/data1.csv","a", newline="") as csvfile:
                    thewriter=csv.DictWriter(csvfile, fieldnames=fieldnames)
                    thewriter.writerow(mydict)
               
                reviews.append(mydict)

                    
            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])
            
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    

    else:
        return render_template('index.html')
    
@app.route('/getcsv') # this is a job for GET, not POST
def getcsv():
    return send_file('static/data1.csv',
                     mimetype='text/csv',
                     attachment_filename='data1.csv',
                     as_attachment=True)

if __name__ == "__main__":
  	app.run(debug=True)

