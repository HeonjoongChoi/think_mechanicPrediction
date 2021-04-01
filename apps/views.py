import pandas as pd
from sklearn.cluster import KMeans
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from apps.serializers import TextSerializer


from django.http.request import QueryDict
from pytilhan.utils import log_util


class ClusteringView(APIView):
    
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, req, *args, **kwargs):
        
        new_data = req.data.dict()
               
        brand = req.data['brand']
        mileage = req.data['mileage']
        date = req.data['date']
        part = req.data['part']
        car_model = req.data['model']
        unit_price = req.data['unit_price']
                
        # not to migrate additionally, did not change TextModel format
        
        new_data['category_id'] = brand+'/'+mileage+'/'+date+'/'+part+'/'+car_model+'/'+unit_price
        
        new_query_dict = QueryDict('', mutable=True)
        new_query_dict.update(new_data)
        
        text_serializer = TextSerializer(data = new_query_dict)
        if text_serializer.is_valid():
            
            #dataset = pd.read_csv(r"C:\Users\thinkforbl\Desktop\donghwa\Data\donghwa_preprocessing_parts.csv", header=0, encoding='unicode_escape')
            dataset = pd.read_csv("/usr/src/app/donghwa_preprocessing_parts.csv", header=0, encoding='unicode_escape')
            dataset=dataset.fillna(0)
            dataset= dataset[dataset['part'] != 0]
            dataset.head()
            
            df = dataset[['part', 'car_code', 'unit_price']]           
            df['part']=df['part'].fillna('0')
            ip_addresses = df.part.unique()
            ip_dict = dict(zip(ip_addresses, range(len(ip_addresses))))
            df=df.replace({'part':ip_dict})
            df=df.fillna(0)
            
            clusters =10
            kmeans = KMeans(n_clusters = clusters) 
            kmeans.fit(df) 
            
            input_data = pd.DataFrame({'part': [part], 'car_code': [car_model], 'unit_price': [unit_price]}, columns=['part', 'car_code', 'unit_price'])
            input_float = input_data.astype({'part':'int'})            
            input_float = input_data.astype({'unit_price':'float', 'car_code':'float'})
            #input_float = input_data.astype({'car_code':'float'})
                    
             #Input data Attend to DataFrame 
            #cluster_df = pd.read_csv(r'C:\Users\thinkforbl\Desktop\donghwa\Data\Donghwa_Cluster_file.csv', header=0, encoding='unicode_escape')
           
            #y_test= cluster_df.drop('Mechanic_level',axis=1)           
           
            #new_raw_data = y_test.append(input_float,ignore_index=True)
            
            y_pred = kmeans.predict(input_float)
            
            
            #y_test['Prediction Level']= y_test           
            #print("Predicted values for the given inputs : " ,y_pred[-1])            
            
                      
            def resultmodule():
                return {"Brand": brand,
                "Model": car_model,
                "Mileage": "{}km".format(mileage),
                "Date": date,
                "Predicted Mechanic Level": y_pred[-1]}
            text_serializer.save() 
            
            
            results = resultmodule()
                 
            return Response(results, status=status.HTTP_200_OK)
        else:
            
            log_util.error(__name__ , text_serializer.errors)
            return Response(text_serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
