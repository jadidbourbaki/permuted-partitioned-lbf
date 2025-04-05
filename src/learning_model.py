from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import pandas as pd
import feature_extraction as fe
import joblib
import os
import numpy as np
import preprocess

def get_global_dataset() -> str:
    return "/tmp/malicious_urls.csv"

def model_size(model) -> int:
    temp_file = "/tmp/permuted_partitioned_learning_model.joblib"
    joblib.dump(model, temp_file)
    size = os.path.getsize(temp_file) 
    print(f"Learning Model size: {np.round(size / 1024 / 1024, 2) } MB ({size * 8} bits)")
    os.remove(temp_file)
    return size

class learning_model:
    # in bytes
    def memory_used(self) -> int:
        return model_size(self.model)
    
    def __init__(self, classifier: any, cache_preprocessed_data: bool = True, clear_cache: bool = False) -> None:
        if cache_preprocessed_data:
            if not os.path.exists(get_global_dataset()) or clear_cache:
                print("Preprocessing Data (will be cached next time)")
                preprocess.generate_data()
        else:
                print("Preprocessing Data (will not be cached)")
                preprocess.generate_data()

        print("Loading data")        
        self.data = pd.read_csv(get_global_dataset())
        X = self.data.drop(['url', 'type'], axis=1)
        y = self.data[['type']]

        print("Splitting data")

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        print("Training model")

        model = classifier
        model.fit(X_train, y_train)

        print("Size of model")

        model_size(model)

        self.model = model

        # Make predictions on the test data
        y_pred = model.predict(X_test)

        # Calculate the accuracy of the classifier
        accuracy = model.score(X_test, y_test)
        print("Accuracy:", accuracy)

        if not cache_preprocessed_data:
            print("Removing preprocessed data")
            self.destroy()

    def query(self, element: any) -> bool:
        pred = self.model.predict(pd.DataFrame([fe.generate_fields(element, 'ANY')[1:-1]], columns=fe.feature_names()[1:-1]))
        return pred[0] == 1
    
    def destroy(self) -> None:
        preprocess.remove_data()

