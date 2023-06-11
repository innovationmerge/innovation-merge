import tensorflow as tf
import cv2
import numpy as np
import time
from innovationmerge.configurations.constants import IMAGE_DETECTION_RESPONSE

class cpuObjectDetectionTfLite():
    """
    Object detection using Tensorflow Lite models
    """
    def __init__(self, model_file_path):
        self.interpreter = tf.lite.Interpreter(model_path=model_file_path)
        self.interpreter.allocate_tensors()

        self.input_mean = 127.5
        self.input_std = 127.5

    def detect(self, cv2_image, labels_list, threshold=0.1):

        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        normalize_height = input_details[0]['shape'][1]
        normalize_width = input_details[0]['shape'][2]

        # convert input image to gray scale
        image_rgb = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        input_img_height, input_img_width, _ = image_rgb.shape

        # Resize input image as per the model requirement
        image_resized = cv2.resize(image_rgb, (normalize_width, normalize_height))

        # add N dim
        input_data = np.expand_dims(image_resized, axis=0)

        # check the type of the input tensor
        floating_model = (input_details[0]['dtype'] == np.float32)
        if input_details[0]['dtype'] == type(np.float32(1.0)):
            floating_model = True

        if floating_model:
            input_data = (np.float32(input_data) - self.input_mean) / self.input_std
        
        self.interpreter.set_tensor(input_details[0]['index'], input_data)

        start_time = time.time()
        self.interpreter.invoke()
        stop_time = time.time()

        out_name = output_details[0]['name']
        if ('StatefulPartitionedCall' in out_name): # This is a TF2 model
            boxes_idx, classes_idx, scores_idx = 1, 3, 0
        else: # This is a TF1 model
            boxes_idx, classes_idx, scores_idx = 0, 1, 2

        # Retrieve detection results
        boxes = self.interpreter.get_tensor(output_details[boxes_idx]['index'])[0] # Bounding box coordinates of detected objects
        classes = self.interpreter.get_tensor(output_details[classes_idx]['index'])[0] # Class index of detected objects
        scores = self.interpreter.get_tensor(output_details[scores_idx]['index'])[0] # Confidence of detected objects

        detection_response = {}
        detection_list = []
        for i in range(len(scores)):
            label_dict = IMAGE_DETECTION_RESPONSE.copy()

            if ((scores[i] > 0.6) and (scores[i] <= 1.0)):

                ymin = int(max(1,(boxes[i][0] * input_img_height)))
                xmin = int(max(1,(boxes[i][1] * input_img_width)))
                ymax = int(min(input_img_height,(boxes[i][2] * input_img_height)))
                xmax = int(min(input_img_width,(boxes[i][3] * input_img_width)))


                label_dict["confidence"] = scores[i]
                label_dict["label_bounding_box"] = [{"x": xmin, "y": ymin}, {"x": xmax, "y": ymax}]
                label_dict["label_class_name"] = labels_list[int(classes[i])]
                detection_list.append(label_dict)
        processing_time = stop_time - start_time
        detection_response= {"detection": detection_list, "processing_time": processing_time}
        return detection_response



