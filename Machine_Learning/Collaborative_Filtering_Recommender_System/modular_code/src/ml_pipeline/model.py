from sklearn.neighbors import NearestNeighbors
from surprise import accuracy
from surprise.model_selection import cross_validate


# Function to create KNN model
def create_knn_model(data):
    try:
        # Creating KNN Model with metric parameter as euclidean distance
        model_knn = NearestNeighbors(metric = 'euclidean', algorithm = 'brute')

        # Fitting the model on purchase_matrix
        model_knn.fit(data)

    except Exception as e:
        print(e)
    else:
        return model_knn

# Function to create and evaluate model
def create_and_evaluate_model(model, train, test):
    try:
        model = model.fit(train)
        prediction = model.test(test)
        rmse = accuracy.rmse(prediction)
        mae = accuracy.mae(prediction)
        
    except Exception as e:
        print(e)
    else:
        return model,prediction,rmse,mae


# Function to calculate cross validation
def calculate_cross_validation(model,data):
    try:
        result = cross_validate(model, data, verbose=True)
    except Exception as e:
        print(e)
    else:
        return result