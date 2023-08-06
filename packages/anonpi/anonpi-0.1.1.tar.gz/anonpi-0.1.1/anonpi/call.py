from flask import Flask, request, jsonify , make_response


class anonapi:
    def __init__(self,token:str):
        self.token = token
    
    
    def create_call(to_number:str,from_number:str, callback_url:str, post_method:str):
        data = {
            "from": from_number,
            "to": to_number,
            "callback_url": callback_url,
            "post_method": post_method
        }
        return data
        


print(anonapi.Call.create("123","123","123","123"))