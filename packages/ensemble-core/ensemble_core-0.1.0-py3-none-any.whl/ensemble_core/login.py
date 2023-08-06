import requests
import json
import torch
import requests
import io
from botocore.exceptions import NoCredentialsError
import boto3


class User:
    logged_in = False
    paid = None
    aws_access_key_id = None
    aws_secret_access_key = None
    aws_session_token = None
    @classmethod
    def login(cls, username, password):
        url = "https://of9ijssfd7.execute-api.us-west-2.amazonaws.com/Dev/cognito"
        headers = {"Content-Type": "application/json"}
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_data = response.json()

        if response_data.get('statusCode') == 200:
            cls.logged_in = True
            cls.paid = response_data['paid']
            cls.aws_access_key_id = response_data['aws_access_key_id']
            cls.aws_secret_access_key = response_data['aws_secret_access_key']
            cls.aws_session_token = response_data['aws_session_token']
        else:
            cls.logged_in = False


# class LinearRegression:
#     def __init__(self): 
#         if User.logged_in and (User.paid=='linear' or User.paid=='paid'):
#             self.__lr = _LinearRegression()
#         else:
#             print("Cannot create LinesarRegression instance because login failed.")
        
            
#     def fit(self, X, y):
#         try:
#             self.__lr.fit(X,y)
#             print('Success fit linear regression')
#         except:
#             print('Issues in fitting linear regression')

#     def predict(self, X):
#         return self.__lr.predict(X)
    


# class _LinearRegression:
#     def __init__(self):
#         self.coefficient = None
#         self.intercept = None

#     def fit(self, X, y):
#         # Calculate the means of X and y
#         x_mean = sum(X) / len(X)
#         y_mean = sum(y) / len(y)

#         # Calculate the terms needed for the numerator and denominator of beta
#         num = sum([(X[i] - x_mean) * (y[i] - y_mean) for i in range(len(X))])
#         den = sum([(X[i] - x_mean) ** 2 for i in range(len(X))])

#         # Calculate beta and alpha
#         self.coefficient = num / den
#         self.intercept = y_mean - self.coefficient * x_mean

#     def predict(self, X):
#         if self.coefficient is None or self.intercept is None:
#             raise Exception("You must call `fit` before `predict`")

#         return [self.coefficient * x + self.intercept for x in X]


class DNN:
    def __init__(self):
        if User.logged_in and (User.paid=='linear' or User.paid=='paid'):
            self.model = self.__download_model()
        else:
            print("Cannot create DNN instance because login failed.")

    def __download_model(self):
        try:
            s3 = boto3.client('s3', 
                              aws_access_key_id=User.aws_access_key_id, 
                              aws_secret_access_key=User.aws_secret_access_key,
                              aws_session_token = User.aws_session_token)
            
            bucket_name = 'model-ensamble'
            object_name = 'scripted_model.pt'
            obj = s3.get_object(Bucket=bucket_name, Key=object_name)
            bytestream = io.BytesIO(obj['Body'].read())
            
            # Load the model into PyTorch
            model = torch.jit.load(bytestream)
            return model
        except NoCredentialsError:
            print("AWS credentials not found.")
            return None
        
    def save(self, name='model.pt'):
        torch.save(self.model.state_dict(), name)

    def predict(self, x):
        return self.model(x)
        
    def fit(self, x, y):
        # Download fit function from S3
        fit_func = self.__download_fit_function()
        # Call the downloaded fit function
        fit_func(self, x, y)

    def __download_fit_function(self):
        try:
            s3 = boto3.client('s3', 
                    aws_access_key_id=User.aws_access_key_id, 
                    aws_secret_access_key=User.aws_secret_access_key,
                    aws_session_token = User.aws_session_token)
            bucket_name = 'model-ensamble'  # Replace with your bucket name
            key = 'fit.py'  # Replace with your key
            obj = s3.get_object(Bucket=bucket_name, Key=key)
            file_content = obj['Body'].read().decode()
            # Execute the script and make the fit function available
            exec(file_content, globals())
            return fit  # fit is expected to be defined in your fit_function.py file
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
                return None
