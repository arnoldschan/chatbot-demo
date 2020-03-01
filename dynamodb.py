import boto3
from datetime import datetime as dt
class DynamoDB:
    def __init__(self,table_name,key_name,sec_key_name,key_type='string',sec_key_type='string',RCU=1,WCU=1):
        self.table_name = table_name
        self.key_name = key_name
        self.key_type = key_type
        self.sec_key_name = sec_key_name
        self.sec_key_type = sec_key_type
        self.RCU = RCU
        self.WCU = WCU
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(self.table_name)
        
    def put(self,key_value, key_list,value_list):
        print(key_list)
        print(value_list)
        now = dt.now().isoformat()
        item = {self.key_name: key_value,
                self.sec_key_name: now}
        add_attributes = dict(zip(key_list,value_list))
        print(add_attributes)
        item.update(add_attributes)
        print(item)
        response = self.table.put_item(
                Item=item
            )
        return response