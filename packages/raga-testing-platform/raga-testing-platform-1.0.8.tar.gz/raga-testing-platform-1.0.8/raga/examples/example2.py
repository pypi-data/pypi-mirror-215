from raga import *
import pandas as pd
import json

ds_json_file = "MA.json"

test_df = []
with open(ds_json_file, 'r') as json_file:
    # Load JSON data
    json_data = json.load(json_file)
    
    # Process the JSON data
    transformed_data = []
    for item in json_data:
        AnnotationsV1 = ImageDetectionObject()
        ROIVectorsM1 = ROIEmbedding()
        ImageVectorsM1 = ImageEmbedding()
        for detection in item["outputs"][0]["detections"]:
            AnnotationsV1.add(ObjectDetection(Id=item["inputs"][0], ClassName=detection['class'], Confidence=detection['confidence'], Format="xywh_normalized"))
            for roi_emb in detection['roi_embedding']:
                ROIVectorsM1.add(Embedding(roi_emb))
        
        attributes_dict = {}
        attributes = item.get("attributes", {})
        for key, value in attributes.items():
            attributes_dict[key] = StringElement(value)

        image_embeddings = item.get("image_embedding", {})
        for value in image_embeddings:
            ImageVectorsM1.add(Embedding(value))

        data_point = {
            'ImageId': StringElement(item["inputs"][0]),
            'TimeOfCapture': TimeStampElement(item["capture_time"]),
            'SourceLink': StringElement(item["source"]),
            'AnnotationsV1': AnnotationsV1,
            'ROIVectorsM1': ROIVectorsM1,
            'ImageVectorsM1': ImageVectorsM1,
        }

        merged_dict = {**data_point, **attributes_dict}

        test_df.append(merged_dict)
        

pd_ds = pd.DataFrame(test_df)

# print(data_frame_extractor(pd_ds).to_csv("MA_new.csv"))
schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement())
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement())
schema.add("SourceLink", FeatureSchemaElement())
schema.add("Resolution", AttributeSchemaElement())
schema.add("Scene", AttributeSchemaElement())
schema.add("AnnotationsV1", InferenceSchemaElement(model="57_baseline"))
schema.add("ImageVectorsM1", ImageEmbeddingSchemaElement(model="57_baseline", ref_col_name=""))
schema.add("ROIVectorsM1", RoiEmbeddingSchemaElement(model="57_baseline", ref_col_name=""))

test_session = TestSession("testingProject", "test_exp_serve_5")

# # # Create an instance of the Dataset class
test_ds = Dataset(test_session, "ServeDataset_5")

test_ds.load(pd_ds, schema)