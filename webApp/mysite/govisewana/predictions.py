from math import sqrt
import numpy as np
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

from pandas import read_csv
from keras.models import load_model
import plotly.plotly as py
import plotly.graph_objs as go

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

class predictions:
    ########################## Demand ############################################
    #Function to predict demand
    def demandPrediction():
        # load data
        def parse(x):
            return datetime.strptime(x, '%Y')
        dataset = read_csv('data/demand_raw.csv',  parse_dates = ['year'], index_col=0, date_parser=parse)

        # manually specify column names
        dataset.columns = ['population','income','substitute','consumption']
        dataset.index.name = 'year'

        # mark all NA values with 0
        dataset['consumption'].fillna(0, inplace=True)

        # summarize first 5 rows
        print(dataset.head(5))

        # save to file
        dataset.to_csv('data/demand.csv')
        #----------------------------------------------------

        # convert series to supervised learning
        def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
            n_vars = 1 if type(data) is list else data.shape[1]
            df = DataFrame(data)
            cols, names = list(), list()
            # input sequence (t-n, ... t-1)
            for i in range(n_in, 0, -1):
                cols.append(df.shift(i))
                names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
            # forecast sequence (t, t+1, ... t+n)
            for i in range(0, n_out):
                cols.append(df.shift(-i))
                if i == 0:
                    names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
                else:
                    names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
            # put it all together
            agg = concat(cols, axis=1)
            agg.columns = names
            # drop rows with NaN values
            if dropnan:
                agg.dropna(inplace=True)
        
            return agg
        

        # load dataset
        # dataset = read_csv('demand.csv', header=0, index_col=0)
        dataset = read_csv('data/demand.csv', header=0, index_col=0)
        values = dataset.values

        # ensure all data is float
        values = values.astype('float32')

        #varibles to reconstruct original data Y
        mean_of_array = np.mean(values[:,3])
        std_of_array = np.std(values[:,3])
        print(".....values here.......")
        print(values[:,3])
        print(".....mean  here.......")
        print(mean_of_array)
        print(".....std  here.......")
        print(std_of_array)


        # normalize features
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled = scaler.fit_transform(values)

        # frame as supervised learning
        reframed = series_to_supervised(scaled,10,3)

        # split into train and test sets
        values = reframed.values
        train = values

        # split into input and outputs
        train_X, train_y = train[:, :-1], train[:, -1]

        # reshape input to be 3D [samples, timesteps, features]
        train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))

        yhat_X=train_X
        yhat_Y=train_y

        # design network
        model = Sequential()
        model.add(LSTM(100, input_shape=(train_X.shape[1], train_X.shape[2])))
        model.add(Dense(1))
        # model.compile(loss='mae', optimizer='adam',metrics=['mse', 'mae', 'mape', 'cosine'])
        model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['mse', 'mae'])

        # fit network
        history = model.fit(train_X, train_y, validation_split=0.33, epochs=90, batch_size=10, verbose=0)


        # save model to single file
        model.save('lstm_model_d.h5')

        #--------------------------------------

        # make predictions
        from keras.models import load_model
        model = load_model('lstm_model_d.h5')
        yhat = model.predict(yhat_X, verbose=0)
        # print("Original output..")
        # print(yhat_Y)
        # print("preictions here...")
        # print(yhat)

        PredictionScore = model.evaluate(yhat_X, yhat_Y, verbose=0)
        count=0
        for i in model.metrics_names:
            print("\n%s: %.2f%%" % (model.metrics_names[count], PredictionScore[count]*100))
            count+=1

        # #reconstruct original data
        yhat = (yhat * std_of_array) + mean_of_array  
        yhat_Y= (yhat_Y * std_of_array) + mean_of_array      

        # plot prediction
        pyplot.plot(yhat, label='prediction-data')
        pyplot.plot(yhat_Y, label='original-data')
        pyplot.legend()
        pyplot.show()

        # plot prediction-2
        # import plotly
        # plotly.offline.init_notebook_mode(connected=True)
        # import plotly.offline as py
        # import plotly.plotly as py
        # import plotly.graph_objs as go 
        X=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
        # X=[1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,2000,20001,20002,20003,20004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
        # Create traces
        trace0 = go.Scatter(
            x = X,
            y = yhat,
            mode = 'lines',
            name = 'prediction-data'
        )   

        trace1 = go.Scatter(
            x = X,
            y = yhat_Y,
            mode = 'lines',
            name = 'original-data'
        )  

        data = [trace0, trace1]
        # py.plot(data, filename='line-mode-demand')   

        layout = go.Layout(
            title='Demand Prediction',
            xaxis=dict(
                title='Year',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='Demand for rice (Mt)',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            )
        )
        fig = go.Figure(data=data, layout=layout)
        # py.plot(fig, filename='line-mode-demand-1')

        #return predicted value
        print((yhat))
        d=[yhat.size-1,-1]
        print("Predicted value------------")
        print(np.take(yhat,d)[0])
        return str(np.take(yhat,d)[0]) + " Mt"

    
##########################Harvest############################################

#Function to predict harvest
    def harvestPrediction():
        # load data
        def parse(x):
            return datetime.strptime(x, '%Y')
        dataset = read_csv('data/harvest_raw.csv',  parse_dates = ['year'], index_col=3, date_parser=parse)
        dataset.drop(['id'], axis=1, inplace=True)
        dataset.drop(['district'], axis=1, inplace=True)
        dataset.drop(['season'], axis=1, inplace=True)

        # manually specify column names
        dataset.columns = ['area', 'rain','product']
        dataset.index.name = 'year'

        # mark all NA values with 0
        dataset['product'].fillna(0, inplace=True)

        # summarize first 5 rows
        print(dataset.head(5))

        # save to file
        dataset.to_csv('data/harvest.csv')

        #convert series to supervised learning
        def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
            n_vars = 1 if type(data) is list else data.shape[1]
            df = DataFrame(data)
            cols, names = list(), list()
            
            #input sequence (t-n, ... t-1)
            for i in range(n_in, 0, -1):
                cols.append(df.shift(i))
                names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
            
            #forecast sequence (t, t+1, ... t+n)
            for i in range(0, n_out):
                cols.append(df.shift(-i))
                if i == 0:
                    names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
                else:
                    names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
            
            #put it all together
            agg = concat(cols, axis=1)
            agg.columns = names
            
            #drop rows with NaN values
            if dropnan:
                agg.dropna(inplace=True)
            return agg
            
        #load dataset
        dataset = read_csv('data/harvest.csv', header=0, index_col=0)
        values = dataset.values

        #integer encode direction
        #encoder = LabelEncoder()
        #values[:,2] = encoder.fit_transform(values[:,2])

        #ensure all data is float
        values = values.astype('float32')

        #varibles to reconstruct original data Y
        mean_of_array = np.mean(values[:,2])
        std_of_array = np.std(values[:,2])
        print(".....values here.......")
        print(values[:,2])
        print(".....mean  here.......")
        print(mean_of_array)
        print(".....std  here.......")
        print(std_of_array)

        #normalize features
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled = scaler.fit_transform(values)

        #frame as supervised learning
        reframed = series_to_supervised(scaled, 1, 1)

        #drop columns we don't want to predict
        reframed.drop(reframed.columns[[4,5]], axis=1, inplace=True)
        print(reframed.head)

        # split into train and test sets
        values = reframed.values
        #n_train_years =2
        #train = values[:n_train_years, :]
        #est = values[n_train_years:, :]

        # split into input and outputs
        train_X, train_y = values[:, :-1], values[:, -1]
        #test_X, test_y = test[:, :-1], test[:, -1]
        print('all train_y values')
        print(train_y)
        # reshape input to be 3D [samples, timesteps, features]
        train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
        #test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
        #print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)
        yhat_X=train_X
        yhat_Y=train_y

        print(yhat_X.shape, yhat_Y.shape)

        # design network
        model = Sequential()
        model.add(LSTM(50, input_shape=(yhat_X.shape[1], yhat_X.shape[2])))
        model.add(Dense(1))
        #compile model
        model.compile(loss='mae', optimizer='adam', metrics=['mse', 'mae'])

        # fit network
        model.fit(yhat_X, yhat_Y, epochs=200, batch_size=72, verbose=2, shuffle=False)

        # save model to single file
        model.save('lstm_model_h.h5')

        # load model from single file
        model = load_model('lstm_model_h.h5')
        # make predictions
        yhat = model.predict(yhat_X, verbose=0)
        print("Original output.....")
        print(yhat_Y)
        print("predicted output.....")
        print(yhat)

        PredictionScore = model.evaluate(yhat_X, yhat_Y, verbose=0)
        count=0
        for i in model.metrics_names:
            print("\n%s: %.2f%%" % (model.metrics_names[count], PredictionScore[count]*100))
            count+=1

        # #reconstruct original data
        yhat = (yhat * std_of_array) + mean_of_array  
        yhat_Y= (yhat_Y * std_of_array) + mean_of_array      


        # plot prediction
        pyplot.plot(yhat, label='prediction-data')
        pyplot.plot(yhat_Y, label='original-data')
        pyplot.legend()
        pyplot.show()

        # X=[2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
        X=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
        # Create traces
        trace0 = go.Scatter(
            x = X,
            y = yhat,
            mode = 'lines',
            name = 'prediction-data'
        )   

        trace1 = go.Scatter(
            x = X,
            y = yhat_Y,
            mode = 'lines',
            name = 'original-data'
        )  

        data = [trace0, trace1]
        # data = [trace0]
        # py.plot(data, filename='line-mode-harvest')

        layout = go.Layout(
            title='Harvest Prediction',
            xaxis=dict(
                title='Year',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='Paddy Production (Mt)',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            )
        )
        fig = go.Figure(data=data, layout=layout)
        # py.plot(fig, filename='line-mode-harvest-1')

        #return predicted value
        print((yhat))
        d=[yhat.size-1,-1]
        print("Predicted value------------")
        print(np.take(yhat,d)[0])
        return str(np.take(yhat,d)[0]) + " Mt"

         
    
            