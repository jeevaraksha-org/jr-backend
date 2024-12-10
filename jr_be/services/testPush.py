from pyfcm import FCMNotification

push_service = FCMNotification(api_key="REDACTED")

"""
proxy_dict = {
          "http"  : "http://127.0.0.1",
          "https" : "http://127.0.0.1",
        }
push_service = FCMNotification(api_key="<api-key>", proxy_dict=proxy_dict)
"""

registration_id = "REDACTED"
message_title = "Location of emergency"
message_body = "longitude: 78.4867,latitude: 17.3850"
result = push_service.notify_single_device(registration_id=registration_id,
                                           message_title=message_title, message_body=message_body)

print(result)
