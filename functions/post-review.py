from cloudant.client import Cloudant
from cloudant.error import CloudantException


# main() will be run automatically when this action is invoked in IBM Cloud
def main(dict):
    """
    Posts a review to the external Cloudant database
    """
    
    secret = {
        "URL": "https://b69568f1-7faa-40da-a28a-905167584d3d-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY": "uFeWPUC_w6Qg79y295QN_8TS6Pd8WBAoj9QvIFbSPFBC",
        "USER_NAME": "b69568f1-7faa-40da-a28a-905167584d3d-bluemix",
    }

    client = Cloudant.iam(
        account_name=secret["USER_NAME"], 
        api_key=secret["IAM_API_KEY"],
        url=secret["URL"],
        connect=True, 
    )
    
    db = client["reviews"]
    new_review = db.create_document(dict["review"])   
    
    if new_review.exists():
        result = {
            "headers": {"Content-Type": "application/json"},
            "body": {"message": "Review published successfully."}
        }
    
        print(new_review)
        return result
        
    else: 
        error_json = {
            "statusCode": 500,
            "message": "Could not publish review due to internal server error."
        }
        return error_json