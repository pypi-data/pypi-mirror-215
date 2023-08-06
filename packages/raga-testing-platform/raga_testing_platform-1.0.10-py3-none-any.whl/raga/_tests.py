import json
from typing import Optional
from raga import Dataset, StringElement, AggregationLevelElement, ModelABTestRules, ModelABTestTypeElement
import sys
import time
import requests

MAX_RETRIES = 3
RETRY_DELAY = 1


def model_ab_test(test_ds:Dataset, testName:StringElement, modelA:StringElement , modelB:StringElement , type:ModelABTestTypeElement, aggregation_level:AggregationLevelElement, rules:ModelABTestRules, gt:Optional[StringElement]=StringElement(""), filter:Optional[StringElement]=StringElement("")):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            initialize(test_ds, testName, modelA, modelB, type, aggregation_level, rules, gt, filter)
            print("Test created successful!")
            break  # Exit the loop if initialization succeeds
        except requests.exceptions.RequestException as e:
            print(f"Network error occurred: {str(e)}")
            retries += 1
            if retries < MAX_RETRIES:
                print(f"Retrying in {RETRY_DELAY} second(s)...")
                time.sleep(RETRY_DELAY)
        except KeyError as e:
            print(f"Key error occurred: {str(e)}")
            sys.exit()# No need to retry if a KeyError occurs 
        except ValueError as e:
            print(f"Value error occurred: {str(e)}")
            sys.exit() # No need to retry if a ValueError occurs
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            sys.exit() # No need to retry if an unexpected error occurs

def initialize(test_ds:Dataset, testName:StringElement, modelA:StringElement , modelB:StringElement , type:ModelABTestTypeElement, aggregation_level:AggregationLevelElement, rules:ModelABTestRules, gt:Optional[StringElement]=StringElement(""), filter:Optional[StringElement]=StringElement("")):
    validation(test_ds, testName, modelA, modelB, type, aggregation_level, rules, gt)
    create_ab_test(test_ds, testName, modelA, modelB, type, aggregation_level, rules, gt, filter)
    return True

def create_ab_test(test_ds:Dataset, testName:StringElement, modelA:StringElement , modelB:StringElement , type:ModelABTestTypeElement, aggregation_level:AggregationLevelElement, rules:ModelABTestRules, gt:Optional[StringElement]=StringElement(""), filter:Optional[StringElement]=StringElement("")):
    payload = {
        "datasetId": test_ds.dataset_id,
        "experimentId": test_ds.test_session.experiment_id,
        "name": testName.get(),
        "filter": filter.get(),
        "modelA": modelA.get(),
        "modelB": modelB.get(),
        "gt":gt.get(),
        "type": type.get(),
        "aggregationLevels": aggregation_level.get(),
        "rules":rules.get()
        }
    
    res_data = test_ds.test_session.http_client.post(
            "api/experiment/test",payload,
            {"Authorization": f'Bearer {test_ds.test_session.token}'},
        )

    if not isinstance(res_data, dict):
        raise ValueError("Invalid response data. Expected a dictionary.")

    return True

def validation(test_ds: Dataset, testName:StringElement, modelA: StringElement, modelB: StringElement, type: ModelABTestTypeElement, aggregation_level: AggregationLevelElement, rules: ModelABTestRules, gt: Optional[StringElement] = StringElement("")):
    if not isinstance(test_ds, Dataset):
        raise TypeError("test_ds must be an instance of the Dataset class.")

    if not isinstance(testName, StringElement) or not testName.get():
        raise ValueError("testName is required and must be an instance of the StringElement class.")
    
    if not isinstance(modelA, StringElement) or not modelA.get():
        raise ValueError("modelA is required and must be an instance of the StringElement class.")

    if not isinstance(modelB, StringElement) or not modelB.get():
        raise ValueError("modelB is required and must be an instance of the StringElement class.")

    if not isinstance(type, ModelABTestTypeElement):
        raise TypeError("type must be an instance of the ModelABTestTypeElement class.")

    if not isinstance(aggregation_level, AggregationLevelElement) or not aggregation_level.get():
        raise ValueError("aggregation_level is required and must be an instance of the AggregationLevelElement class.")

    if not isinstance(rules, ModelABTestRules) or not rules.get():
        raise ValueError("rules is required and must be an instance of the ModelABTestRules class.")

    if type.get() == "labelled":
        if not isinstance(gt, StringElement) or not gt.get():
            raise ValueError("gt is required on labelled type and must be an instance of the StringElement class.")

    return True

        

