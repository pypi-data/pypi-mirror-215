import os
import unittest
from unittest import mock
import pandas as pd
from raga import TestSession,Dataset,  initialize, model_ab_test, MAX_RETRIES, RETRY_DELAY
from raga.utils.dataset_util import FileUploadError
from raga import Dataset, StringElement, AggregationLevelElement, ModelABTestRules, ModelABTestTypeElement, FloatElement
from unittest.mock import MagicMock, patch, Mock, call
import requests

class TestABTestTestCase(unittest.TestCase):

    def setUp(self):
        self.test_session = TestSession("project_name", "run_name", u_test=True)
        self.test_session.project_id = "project_id"
        self.test_session.token = "token"
        self.dataset_name = "my_dataset"
        self.test_session.experiment_id = "experiment_id"
        self.dataset_creds = None
        self.dataset = Dataset(self.test_session, self.dataset_name, self.dataset_creds, u_test=True)
        self.dataset.dataset_id = "12345"

    # def test_valid_test_case(self):
    #     modelA = StringElement("modelA")
    #     modelB = StringElement("modelB")
    #     gt = StringElement("GT")
    #     type = ModelABTestTypeElement("unlabelled")
    #     aggregation_level = AggregationLevelElement()
    #     aggregation_level.add(StringElement("weather"))
    #     aggregation_level.add(StringElement("scene"))
    #     aggregation_level.add(StringElement("time_of_day"))
    #     rules = ModelABTestRules()
    #     rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))
    #     rules.add(metric = StringElement("‘difference_count’"), IoU = FloatElement(0.5), _class = StringElement("‘vehicle’"), threshold = FloatElement(0.05))

    #     result = initialize(self.dataset, modelA, modelB, type, aggregation_level, rules, gt)
    #     self.assertIsNotNone(result)

    def test_invalid_test_ds_parameter(self):
        modelA = StringElement("modelA")
        modelB = StringElement("modelB")
        gt = StringElement("GT")
        type = ModelABTestTypeElement("unlabelled")
        aggregation_level = AggregationLevelElement()
        aggregation_level.add(StringElement("weather"))
        aggregation_level.add(StringElement("scene"))
        aggregation_level.add(StringElement("time_of_day"))
        rules = ModelABTestRules()
        rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))
        rules.add(metric = StringElement("‘difference_count’"), IoU = FloatElement(0.5), _class = StringElement("‘vehicle’"), threshold = FloatElement(0.05))

        with self.assertRaises(TypeError) as context:
            initialize("invalid_test_ds", modelA, modelB, type, aggregation_level, rules, gt)
        self.assertEqual(str(context.exception), f"test_ds must be an instance of the Dataset class.") 

    def test_missing_model_a_parameter(self):
        modelA = StringElement("")
        modelB = StringElement("modelB")
        gt = StringElement("GT")
        type = ModelABTestTypeElement("unlabelled")
        aggregation_level = AggregationLevelElement()
        aggregation_level.add(StringElement("weather"))
        aggregation_level.add(StringElement("scene"))
        aggregation_level.add(StringElement("time_of_day"))
        rules = ModelABTestRules()
        rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))
        rules.add(metric = StringElement("‘difference_count’"), IoU = FloatElement(0.5), _class = StringElement("‘vehicle’"), threshold = FloatElement(0.05))

        with self.assertRaises(ValueError) as context:
            initialize(self.dataset, modelA, modelB, type, aggregation_level, rules, gt)
        self.assertEqual(str(context.exception), 'modelA is required.')

    def test_missing_model_b_parameter(self):
        modelA = StringElement("modelA")
        modelB = StringElement("")
        gt = StringElement("GT")
        type = ModelABTestTypeElement("unlabelled")
        aggregation_level = AggregationLevelElement()
        aggregation_level.add(StringElement("weather"))
        aggregation_level.add(StringElement("scene"))
        aggregation_level.add(StringElement("time_of_day"))
        rules = ModelABTestRules()
        rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))
        rules.add(metric = StringElement("‘difference_count’"), IoU = FloatElement(0.5), _class = StringElement("‘vehicle’"), threshold = FloatElement(0.05))

        with self.assertRaises(ValueError) as context:
            initialize(self.dataset, modelA, modelB, type, aggregation_level, rules, gt)
        self.assertEqual(str(context.exception), 'modelB is required.')



    def test_missing_aggregation_level_parameter(self):
        modelA = StringElement("modelA")
        modelB = StringElement("modelB")
        gt = StringElement("GT")
        type = ModelABTestTypeElement("unlabelled")
        aggregation_level = AggregationLevelElement()
        rules = ModelABTestRules()
        rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))
        rules.add(metric = StringElement("‘difference_count’"), IoU = FloatElement(0.5), _class = StringElement("‘vehicle’"), threshold = FloatElement(0.05))

        with self.assertRaises(ValueError) as context:
            initialize(self.dataset, modelA, modelB, type, aggregation_level, rules, gt)
        self.assertEqual(str(context.exception), "aggregation_level is required.")

    def test_invalid_aggregation_level_data_type(self):
        modelA = StringElement("modelA")
        modelB = StringElement("modelB")
        gt = StringElement("GT")
        type = ModelABTestTypeElement("unlabelled")
        aggregation_level = "invalid"
        rules = ModelABTestRules()
        rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))
        rules.add(metric = StringElement("‘difference_count’"), IoU = FloatElement(0.5), _class = StringElement("‘vehicle’"), threshold = FloatElement(0.05))

        with self.assertRaises(TypeError) as context:
            initialize(self.dataset, modelA, modelB, type, aggregation_level, rules, gt)
        self.assertEqual(str(context.exception), "aggregation_level must be an instance of the AggregationLevelElement class.")

    def test_missing_rules_parameter(self):
        modelA = StringElement("modelA")
        modelB = StringElement("modelB")
        gt = StringElement("GT")
        type = ModelABTestTypeElement("unlabelled")
        aggregation_level = AggregationLevelElement()
        aggregation_level.add(StringElement("weather"))
        aggregation_level.add(StringElement("scene"))
        aggregation_level.add(StringElement("time_of_day"))
        rules = ModelABTestRules()

        with self.assertRaises(ValueError) as context:
            initialize(self.dataset, modelA, modelB, type, aggregation_level, rules, gt)
        self.assertEqual(str(context.exception), "rules is required.")

    def test_invalid_rules_data_type(self):
        modelA = StringElement("modelA")
        modelB = StringElement("modelB")
        gt = StringElement("GT")
        type = ModelABTestTypeElement("unlabelled")
        aggregation_level = AggregationLevelElement()
        aggregation_level.add(StringElement("weather"))
        aggregation_level.add(StringElement("scene"))
        aggregation_level.add(StringElement("time_of_day"))
        rules = "invalid"

        with self.assertRaises(TypeError) as context:
            initialize(self.dataset, modelA, modelB, type, aggregation_level, rules, gt)
        self.assertEqual(str(context.exception), "rules must be an instance of the StringElement class.")

    def test_missing_gt_on_labelled_type(self):
        modelA = StringElement("modelA")
        modelB = StringElement("modelB")
        gt = StringElement("")
        type = ModelABTestTypeElement("labelled")
        aggregation_level = AggregationLevelElement()
        aggregation_level.add(StringElement("weather"))
        aggregation_level.add(StringElement("scene"))
        aggregation_level.add(StringElement("time_of_day"))
        rules = ModelABTestRules()
        rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))
        rules.add(metric = StringElement("‘difference_count’"), IoU = FloatElement(0.5), _class = StringElement("‘vehicle’"), threshold = FloatElement(0.05))

        with self.assertRaises(ValueError) as context:
            initialize(self.dataset, modelA, modelB, type, aggregation_level, rules, gt)
        self.assertEqual(str(context.exception), f"gt is required on labelled type.")

    def test_model_ab_test_network_error(self):
        mock_initialize = MagicMock(side_effect=requests.exceptions.RequestException("Network error"))
        mock_create_ab_test = MagicMock()

        # Patch the initialize and create_ab_test functions
        with patch('raga.initialize', side_effect=mock_initialize), \
            patch('raga.create_ab_test', side_effect=mock_create_ab_test):
            modelA = StringElement("modelA")
            modelB = StringElement("modelB")
            gt = StringElement("Ground Truth")
            type = ModelABTestTypeElement("labelled")
            aggregation_level = AggregationLevelElement()
            aggregation_level.add(StringElement("weather"))
            aggregation_level.add(StringElement("scene"))
            aggregation_level.add(StringElement("time_of_day"))
            rules = ModelABTestRules()
            rules.add(metric=StringElement("precision_diff"), IoU=FloatElement(0.5), _class=StringElement("all"), threshold=FloatElement(0.05))
            rules.add(metric=StringElement("difference_count"), IoU=FloatElement(0.5), _class=StringElement("vehicle"), threshold=FloatElement(0.05))

            # Call the method
            with patch('builtins.print') as mock_print:
                # Set the MAX_RETRIES to 3 for testing
                MAX_RETRIES = 3
                model_ab_test(self.dataset, modelA=modelA, modelB=modelB, gt=gt, type=type, aggregation_level=aggregation_level, rules=rules)
                # Assert the expected prints and retries
                expected_calls = [
                    call('Network error occurred: Network error'),
                    call(f'Retrying in {RETRY_DELAY} second(s)...'),
                    call('Network error occurred: Network error'),
                    call(f'Retrying in {RETRY_DELAY} second(s)...'),
                    call('Network error occurred: Network error')
                ]
                mock_print.assert_has_calls(expected_calls)
                self.assertEqual(mock_print.call_count, len(expected_calls))
                self.assertEqual(mock_initialize.call_count, MAX_RETRIES)
                self.assertEqual(mock_create_ab_test.call_count, 0)


    

if __name__ == "__main__":
    unittest.main()



