from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision import models, transforms
import cv2
import torch

inverse_label_map = {
    1: "Wearing Mask Correctly",
    2: "Wearing Mask Incorrectly",
    3: "Not Wearing Mask"
}

color_map = {
    1: (0, 255, 0),
    2: (0, 255, 255),
    3: (0, 0, 255)
}

# Load pretrained segmentation model
def get_model_instance_segmentation(num_classes):
    model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes+1)

    return model

class VideoCamera(object):
    def __init__(self):
        # Store video and model
        self.video = cv2.VideoCapture(0)
        model = get_model_instance_segmentation(3)
        model.load_state_dict(torch.load('faster_rcnn_model.pt', map_location=torch.device('cpu')))
        self.model = model.eval()
        self.transform = data_transform = transforms.Compose([
                transforms.ToTensor() 
        ])
        self.new_pred = False
        self.preds = None

    def __del__(self):
        self.video.release()        

    # Get image frame and makes new predictions if necessary
    def get_frame(self):
        ret, frame = self.video.read()
        # Make predictions on frame
        if self.new_pred:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_tensor = [self.transform(frame)]
            self.preds = self.model(img_tensor)[0]
            self.new_pred = False
        # Show predictions on frame
        if self.preds:
            threshold = 0.95
            found = False
            l = self.preds["scores"].shape[0]
            i = 0
            # Display predictions above threshold, decrementing threshold if no predictions are above
            while i < l:
                if self.preds["scores"][i].item() >= threshold:
                    # Get bounding box and label
                    xmin, ymin, xmax, ymax = [int(x.item()) for x in self.preds["boxes"][i]]
                    class_num = self.preds["labels"][i].item()
                    # Draw UI
                    label = inverse_label_map[class_num]
                    color = color_map[class_num]
                    cv2.putText(frame, label, (xmin, ymin - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
                    i += 1
                    found = True
                else:
                    if found:
                        break
                    else:
                        threshold -= 0.05
        ret, jpeg = cv2.imencode('.jpg', frame)
        
        return jpeg.tobytes()

    # Set video to make a new prediction next frame
    def set_prediction(self, pred):
        self.new_pred = pred