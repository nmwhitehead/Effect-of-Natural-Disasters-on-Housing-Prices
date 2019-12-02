from flask import Flask, render_template, url_for, redirect
from flask import request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Importing the dataset which will be used later
data = pd.read_csv('./datasets/Sale_Prices_Zip.csv')
fema = pd.read_csv('./datasets/Disasters By Zip Code')
data.rename(columns={'RegionName':'zip'}, inplace=True)
dates= data.iloc[:, 5:-1]
dates.insert(0,'Zip', data['zip'], True)
dates.set_index("Zip", inplace=True)
fema.rename(columns={'Zip Code':'zipcode'}, inplace=True)
fema.set_index('zipcode', inplace=True)

#instantiating app
@app.route('/form')
def form():
    return render_template('form.html')

#creating output page

@app.route('/submit')
def submit():
    user_input = request.args

    zipcode = (user_input['zipcode'])
    print(*user_input, sep='\n')
    # if zipcode == '':
    #     error_message = 'Error: There is no information about that zipcode.'
    #     return render_template('form.html', error_message=error_message

    zipcode = int(zipcode)

    check= zipcode in dates.index
    if not check:
        error_message = 'Error: There is no information about that zipcode.'
        return render_template('form.html', error_message=(error_message))


    #______________________________________________________________________________
    zipcode = int(zipcode)
    imagefilename3="GRAPH3.png"

    fig3 = plt.figure(figsize=(15,10));


    plt.title((f"Price changes for households in zipcode: {zipcode}"), fontsize=30);
    plt.xlabel('Years', fontsize=20);
    plt.ylabel('Average Market Price of Houses', fontsize=20);

        #plt.xticks([6, 18, 30, 42, 54, 66, 78, 90], ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']);
        #data.loc[data['zip'].isin([zipcode])]
        #for index, row in dates.iterrows():
        #ax.set_xticks(ax.get_xticks()[::2])
    plt.xticks(rotation=90)
    plt.xticks(np.arange(0, 1000, step=6))
    plt.plot(dates.loc[zipcode, '2010-01':'2019-09'])
    #plt.axvline(46, label='Unnamed Storm/Flood', linestyle='dashdot', c='b')

    plt.axvline('2016-09', label='Hurricane Mathew', linestyle='dashed', c='r')
    plt.axvline('2017-09', label='Hurricane Irma', linestyle='dashed', c='m')
    plt.axvline('2018-09', label='Hurricane Florence', linestyle='dashed', c='g')
    z= (100*((dates.loc[zipcode, '2010-01':'2019-09'].pct_change(axis=0).abs().max())))
    plt.legend()

    new_graph_name3 = "graph3"
    plt.savefig('static/graph3')
    plt.savefig('static/GRAPH3')

    #return plt.figure


    url= 'https://image.freepik.com/free-vector/elegant-white-background-with-shiny-lines_1017-17580.jpg'
    #'https://i.pinimg.com/originals/a0/f4/33/a0f433603c8a62e9df3d7d25d3b3649e.png'

    photo='https://clipart.info/images/ccovers/1526524316real-madrid-club-de-futbol-png-logo.png'
    photo2='http://pngimg.com/uploads/football/football_PNG52775.png'

    dates_pct = dates.pct_change(axis=1)
    pct = 100*(dates_pct.loc[zipcode, :].abs().max())
    pct= round(pct, 3) #.pct_change().abs().max()

    zip_all_pct = dates_pct.loc[zipcode,:]
    date_pct = zip_all_pct.abs().argmax()

    # FEMA DATASET

    if pd.DataFrame(fema.loc[(fema.index == zipcode)]).empty:
        fema_data = 'There are no natural disasters recorded for this zipcode'
    else:
        fema_data= pd.DataFrame(fema.loc[(fema.index == zipcode)])
        fema_data = fema_data.head().to_html()
        #fema_data= fema_data.head(1).to_html()

    # Descriptive Statistics
    des_stats = pd.DataFrame(data.loc[(data.zip == zipcode), '2019-08'] ).describe().to_html()


    # return render_template('results.html', graph1=new_graph_name1, graph2=new_graph_name2, graph3=new_graph_name3, url=url, pct=pct, zipcode=zipcode)

    return render_template('results.html', graph3=new_graph_name3, url=url, pct=pct, date_pct=date_pct, zipcode=zipcode, fema_table=fema_data, des_stats=des_stats)

    #______________________________________________________________________________

if __name__== '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)
