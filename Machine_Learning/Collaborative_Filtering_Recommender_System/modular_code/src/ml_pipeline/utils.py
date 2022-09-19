import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import random


# Function to read excel file
def read_data(filepath):
    try:
        df = pd.read_excel(filepath)
    except Exception as e:
        print(e)
    else:
        return df


# Function to find k similar users
def similar_users(user_id, similarity_df, k = 5):

    try:
        # separating df rows for the entered user id
        user = similarity_df[similarity_df.index == user_id]
    
        # df of all other users
        other_users = similarity_df[similarity_df.index != user_id]
    
        # calc cosine similarity between user and each other user
        similarities = cosine_similarity(user,other_users)[0].tolist()
    
        # create list of indices of these users
        indices = other_users.index.tolist()
    
        # create key/values pairs of user index and their similarity
        index_similarity = dict(zip(indices, similarities))
    
        # sort by similarity
        index_similarity_sorted = sorted(index_similarity.items(),reverse=True)
    
        # grab k users off the top
        top_users_similarities = index_similarity_sorted[:k]
        users = [u[0] for u in top_users_similarities]
    
    except Exception as e:
        print(e)
    else:
        return users



# Function to make recommendations using purchases of similar users.
def similar_user_recommendation(user_id, similarity_df, data, custid, productid):
    
    try:
        similar_user = similar_users(user_id, similarity_df)
        
        # obtaining all the items bought by similar users
        simu_rec = []
        for j in similar_user:
            desc = data[data[custid]==j][productid].to_list()
            simu_rec.append(desc)
    
        # this gives us multi-dimensional list
        # we need to flatten it
        flat_list = []
        for sublist in simu_rec:
            for item in sublist:
                flat_list.append(item)
        final_list = list(dict.fromkeys(flat_list))
    
        # storing 10 random recommendations in a list
        ten_recs = random.sample(final_list, 10)
        
        

    except Exception as e:
        print(e)
    else:
        # returning 10 random recommendations
        return ten_recs


# Function to find k similar items
def similar_items(item_id, similarity_df, k = 5):

    try:
        # separating df rows of the selected item
        item = similarity_df[similarity_df.index == item_id]
    
        # a df of all other items
        other_items = similarity_df
    
        # calc cosine similarity between selected item with other items
        similarities = cosine_similarity(item,other_items)[0].tolist()
    
        # create list of indices of these items
        indices = other_items.index.tolist()
    
        # create key/values pairs of item index and their similarity
        index_similarity = dict(zip(indices, similarities))
        index_similarity = list(index_similarity.keys())

        # grab k items from the top
        top_item_similarities = index_similarity[:k]

        

    except Exception as e:
        print(e)
    else:
        return top_item_similarities
    

# Function to find similar users using knn
def similar_users_knn(model, purchase ,query_index):
    
    try:
        simu_knn=[]
        # Storing the distance and index of nearest neighors
        distances, indices = model.kneighbors(purchase.iloc[query_index,:].values.reshape(1, -1), n_neighbors = 5)
        for i in range(0, len(distances.flatten())):
            if i == 0:
                print('Recommendations for {0}:\n'.format(purchase.index[query_index]))
            else:
                print('{0}: {1}, with distance of {2}:'.format(i, purchase.index[indices.flatten()[i]], distances.flatten()[i]))
                simu_knn.append(purchase.index[indices.flatten()[i]]) 

    except Exception as e:
        print(e)
    else:
        return simu_knn

# Function to make recommendations using purchases of similar users
def similar_user_recommendation_knn(model, purchase, query_index, data, custid, productid):
    
    try:
        # Finding similar users
        simu_knn = similar_users_knn(model, purchase ,query_index)

        #obtaining all the items bought by similar users
        simu_rec = []
        for j in simu_knn:
            desc = data[data[custid]==j][productid].to_list()
            simu_rec.append(desc)
    
        #this gives us multi-dimensional list
        # we need to flatten it
        flat_list = []
        for sublist in simu_rec:
            for item in sublist:
                flat_list.append(item)
        final_list = list(dict.fromkeys(flat_list))
    
        # storing 10 random recommendations in a list
        ten_recs = random.sample(final_list, 10)
    
    except Exception as e:
        print(e)
    else:
        #returning 10 random recommendations
        return ten_recs


# Function to get best and worst predictions of model
def get_best_worst_predictions_by_model(prediction, trainset, col_list):

    # Function to get item orders
    def get_item_orders(uid):
        try:
            return len(trainset.ur[trainset.to_inner_uid(uid)]) # returns the number of orders made for that item
        except ValueError: # user was not part of the trainset
            return 0
    
    # Function to get customer orders
    def get_customer_orders(iid):
        try: 
            return len(trainset.ir[trainset.to_inner_iid(iid)]) # returns the number of orders made by that customers
        except ValueError: # item was not part of the trainset
            return 0

    try:
        predictions_df = pd.DataFrame(prediction, columns=col_list)
        predictions_df['item_orders'] = predictions_df.item.apply(get_item_orders)
        predictions_df['customer_orders'] = predictions_df.customer.apply(get_customer_orders)
        predictions_df['err'] = abs(predictions_df.est - predictions_df.quantity)
        best_predictions = predictions_df.sort_values(by='err')[:10]
        worst_predictions = predictions_df.sort_values(by='err')[-10:]

    except Exception as e:
        print(e)
    else:
        return best_predictions, worst_predictions



# Function to find cosine similarity of a matrix
def find_cosine_similarity(dataframe):
    try:
        similarity = cosine_similarity(dataframe)
        
    except Exception as e:
        print(e)

    else:
        return similarity