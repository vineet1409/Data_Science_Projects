import pandas as pd
from scipy.sparse import csr_matrix
from collections import Counter
from surprise import Reader, Dataset
from surprise.model_selection import train_test_split


# Function to clean data if it contains any null value and negative quantities.
def drop_null(dataframe):
    try:
        df1 = dataframe.dropna()
        df1 = df1[df1.Quantity > 0]
    except Exception as e:
        print(e)
    else:
        return df1


# Function to filter data
def filter_data(dataframe, column, value):
    try:
        df1 = dataframe[dataframe[column] > value]
    except Exception as e:
        print(e)
    else:
        return df1


# Function to rename column name
def col_rename(dataframe,oldname,newname):
    try:
        dataframe.rename(columns={oldname:newname},inplace=True)
    except Exception as e:
        print(e)
    else:
        return dataframe



# Function to encode quantity
def encode_units(x):
    try:
        if x < 1: # If the quantity is less than 1
            return 0 # Not purchased
        if x >= 1: # If the quantity is greater than 1
            return 1 # Purchased
    except Exception as e:
        print(e)


# Function to create matrix
def create_matrix(dataframe,groupby_1,groupby_2,aggr_measure,set_index_by):
    try:
        user_purchase = (dataframe.groupby([groupby_1,groupby_2])[aggr_measure].sum().unstack().reset_index().fillna(0).set_index(set_index_by))
    except Exception as e:
        print(e)
    else:
        return user_purchase


# Function to merge dataframes
def merge_dataframes(dataframe1, dataframe2, on_col):
    try:
        dataframe = pd.merge(dataframe1, dataframe2, on=on_col, how="inner")
    except Exception as e:
        print(e)
    else:
        return dataframe
        

# Function to create dataframe of similarity score
def similarity_score_dataframe(similarity_df, dataframe):
    try:
        similarity_df = pd.DataFrame(similarity_df, index=dataframe.index, columns=dataframe.index)
    except Exception as e:
        print(e)
    else:
        return similarity_df


# Function to create CSR matrix
def create_csr_matrix(dataframe):
    try:
        purchase_matrix = csr_matrix(dataframe.values)
    except Exception as e:
        print(e)
    else:
        return purchase_matrix

# Function to prepare data for matrix factorization
def data_prep_matrix_factorization(item_purchase):
    try:
        df = item_purchase.stack().to_frame()
        df.reset_index(inplace=True)
    except Exception as e:
        print(e)
    else:
        return df



# Function to shortlist customer on the basis of orders
def shortlisting_cust(data,data_matrix_fact,custid,productid):

    try:
        # Storing all customer ids in customers
        customers = data[custid]

        # Storing all item descriptions in items
        items = data[productid]

        # counting no. of orders made by each customer
        count1 = Counter(customers)

        # storing the count and customer id in a dataframe
        countdf1 = pd.DataFrame.from_dict(count1, orient='index').reset_index()

        # dropping all customer ids with less than 120 orders
        countdf1 = countdf1[countdf1[0]>120]

        # renaming the index column as CustomerID for inner join
        countdf1.rename(columns={'index':custid},inplace=True)

        # counting no. of times an item was ordered
        count2 = Counter(items)

        # storing the count and item description in a dataframe
        countdf2 = pd.DataFrame.from_dict(count2, orient='index').reset_index()

        # dropping all items which were ordered less than 120 times
        countdf2 = countdf2[countdf2[0]>120]

        # renaming the index column as Description for inner join
        countdf2 = col_rename(countdf2,'index',productid)

        # applying inner join

        df = merge_dataframes(data_matrix_fact, countdf2, productid)
        df = merge_dataframes(df, countdf1, custid)

        # dropping columns which are not necessary
        df.drop(['0_y','0_x'],axis=1,inplace=True)

        # reading the data in a format supported by surprise library.
        reader = Reader(rating_scale=(0,5946))
        # the range has been set as 0,5946 as the maximum value of quantity is 5946.

        # loading Dataset in a format supported by surprise library.
        df = Dataset.load_from_df(df, reader)

    except Exception as e:
        print(e)

    else:
        return df


# Function to split data into train and test
def splitting_data(data):
    try:
        # performing train test split on the dataset
        trainset, testset = train_test_split(data, test_size= 0.2)
    except Exception as e:
        print(e)
    else:
        return trainset, testset