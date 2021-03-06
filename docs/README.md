# Introduction
Our project, WYM - Wear Your Mask, is a live application that utilizes camera recording to monitor the surrounding and determine if any individuals are maskless or not wearing their masks properly.
# Directories
## data
- bounding_images: directory containing all input images for bounding box HITs
- classification_images: directory containing all input images for classification HITs
- validation_images: directory containing validation images of crowds to test our model on
- analysis: directory containing analysis files after performance quality control and aggregation
    - accuracy_iteration_with_initial.png: plot of iteration number vs accuracy with gold standard quality as initial quality
    - accuracy_iteration_without_initial.png: plot of iteration number vs accuracy assuming all workers are initially perfect
    - bounding_box_label_probabilities.png: Bar graph representing probability distribution of mask labels for each bounding box label
    - bounding_box_categories.png: Pie chart representing percentage makeup of each bounding box category
    - facee_detect.png: Pie chart representing percentage of faces detected and undetected by model
    - gold_standard_quality.csv: quality control output for every worker with tasks completed, average time spent on each task, accuracy for each face category, total accuracy, and whether or not the worker is a good worker
    - image_labels.csv: aggregation output from running EM with gold standard performance as initial quality for 1 iteration
    - model_image_labels.csv: model predictions on labels for classification images
    - model_image_preds.csv: model predictions on validation images including a list of bounding boxes, a list of labels corresponding to each bounding box, and a list a scores that the model assigns to each bounding box prediction
    - model_performance.csv: model performance on validation images containing bounding boxes, predicted labels, scores for prediction, true labels, and number of undetected faces identified by user
    - model_scores.png: Bar graph representing average confidence scores for each bounding box category
    - worker_accuracy_iteration_with_initial.png: plot of iteration number vs individual worker accuracy with gold standard quality as initial quality
    - worker_accuracy_iteration_without_initial.png: plot of iteration number vs individual worker accuracy assuming all workers are initially perfect
    - worker_model_accuracies.png: bar graph representing accuracies of all workers combined and our model on labeling classification images and validation images
    - worker_model_quality.png: graph of classification images labeled vs accuracy of workers and our FasterRCNN model
- bounding_hit_input(0-1).csv: generated CSV input for bounding box HITs
- bounding_hit_output.csv: output from bounding box HITs
- bounding_images.txt: links to bounding box input images on S3 bucket
- classification_hit_input(0-1).csv: generated CSV input for classification HITs
- classification_hit_output: output from classification HITs
- classification_images.txt: links to classification input images on S3 bucket
- classifier_input.csv: CSV input to train classifier with columns as bounding box image file names, bounding boxes, and labels corresponding to each bounding box
- gold_standard_image_labels.csv: manually assigned labels to 50 images of each of our 3 categories
- true_labels.csv: manually assigned labels to 500 originally unlabeled images to test aggregation
- unlabeled_images.csv: list of image urls that have not been manually labeled
## docs
- Mturk: directory containing information on how to contribute to our HITs
- flowchart.png: flowchart with workflow and components
- workflow.png: flowchart only listing workflow
- screenshots.pdf: Screenshot of interfaces for HITs and users
## src
Contains code for the project as well as sample inputs and outputs to our code

Refer to the Code section for more information about each file and any future improvements
# Components
## Collect images (1, Completed)
- Find images and datasets online of people wearing masks, without masks, or wearing masks improperly
- Store in S3 bucket
## Bounding Box Task (1, Completed)
- Provide images to MTurk workers to draw bounding boxes around faces of visible people
## Crop Images (2, Completed)
- Using the bounding box data collected from workers, resize and crop images to fit the bounding box size in order to get closer pictures of faces
- Write python code to automatically crop images based on bounding box data
- Approve bounding box if all cropped images contain entire face and clear
## Label Task (2, Completed) 
- Create MTurk HIT for workers to label the newly cropped pictures as Wearing Mask Correctly, Wearing Mask Incorrectly, or Not Wearing Mask.
- Design html template to allow workers to label multiple images at once, including quality control images
## Quality Control (2, Completed)
- Use gold standard labels for certain images in order to conduct a quality check on the worker???s labels
- Have workers label multiple images at once with a couple prelabeled images mixed in
- Write python code to compute worker quality based on gold standard labels
## Aggregate Labels (2, Completed)
- Use EM in conjunction with gold standard labels performance as initial worker quality to generate true label for each image
- Write code to generate true labels using Expectation Maximization algorithm along with gold standard labels
## Train a Classifier (3, Completed)
- Using the labels determined by the workers, train a classifier to automatically determine whether or not a face in an image is Wearing Mask Correctly, Wearing Mask Incorrectly, or Not Wearing Mask.
## Analyze Accuracy (3, Completed)
- Split the data into train/test/validation sets and run the classifier to compute accuracy
- Fine tune parameters to increase accuracy
- Test model on random pictures taken to evaluate if model is good enough in a realtime setting
## Web Application (4, Completed)
- Allow users to turn on camera for live recording
- Feed camera recording into our classifier to determine if people in the recording are wearing masks properly
- Display classifier results back to the user
# Data
## Quality Control
### Input
Dataframe result from our Image Labeling HIT task with the following columns:
- WorkerId: Id of the worker who completed the task
- Input.image(1-6): Image url of images we want workers to classify
- Input.wmc_qc: Image url of wearing mask correctly quality control image
- Input.wmi_qc: Image url of wearing mask incorrectly quality control image
- Input.nwm_qc: Image url of not wearing mask quality control image
- Answer.image(1-6): Classification label of images
- Answer.wmc_qc: Classification of wearing mask correctly quality control image
- Answer.wmi_qc: Classification of wearing mask incorrectly quality control image
- Answer.nwm_qc: Classification of not wearing mask quality control image
### Output
List with the following columns:
- WorkerId: Id of the worker who completed tasks
- TasksCompleted: Number of tasks completed by worker
- TimePerTask: Average time worker spent on each task
- WearingMaskCorrectlyAccuracy: Percentage accuracy of worker when image is labeled Wearing Mask Correctly
- WearingMaskIncorrectlyAccuracy: Percentage accuracy of worker when image is labeled Wearing Mask Incorrectly
- NotWearingMaskAccuracy: Percentage accuracy of worker when image is labeled Not Wearing Mask
- TotalAccuracy: Percentage accuracy on quality control images
- GoodWorker: True if and only if the worker has 90% percent accuracy for all image categories: Wearing Mask Correctly, Wearing Mask Incorrectly, and Not Wearing Mask

Gold Standard Label Confusion Matrix: A 3x3 confusion matrix for our 3 image categories
## Aggregation 
### Input
Same Dataframe as Quality Control input

Confusion Matrix from Quality Control output
### Output
List with the following columns:
- Image: Image file name
- Label: Image label of either Wearing Mask Correctly, Wearing Mask Incorrectly, or Not Wearing Mask.
# Code
Refer to README.md in src directory for information on how to run code
- <b>result_process.py</b>: Contains quality control and aggregation functions to process results
    - Quality Control: 
        - <i>worker_quality(df)</i>: Computes worker quality from gold standard label answers
            - df: Dataframe from HIT result
            - output
                - List of tuples corresponding to different columns in data/analysis/gold_standard_quality.csv
                - Gold standard label confusion matrix
        - <i>em_worker_quality(rows, labels)</i>: Computes weighted worker quality
            - rows: Dataframe from HIT result
            - labels: Dictionary storing label for each image in the form of an array of length 3 where the value of each index represents the weight of the label corresponding to that index
            - output: Confusion matrix for each worker
    - Aggregation:
        - <i>em_votes(rows, worker_qual)</i>: Computes labels given worker quality
            - rows: Dataframe from HIT result
            - worker_quality: Dictionary storing confusion matrix for each worker
            - output: Dictionary storing label for each image in the form of an array of length 3 where the value of each index represents the weight of the label corresponding to that index
        - <i>em_iteration(rows, worker_qual)</i>: Completes one EM iteration
            - rows: Dataframe from HIT result
            - worker_quality: Dictionary storing confusion matrix for each worker
            - output: 
                - labels: Dictionary storing label for each image in the form of an array of length 3 where the value of each index represents the weight of the label corresponding to that index
                - new_worker_quality: Dictionary storing new confusion matrix for each worker
        - <i>em_vote(rows, worker_qual, iter_num, return_dict)</i>: Compute labels after iter_num iterations of the EM algorithm with initial worker quality specified by worker_qual
            - rows: Dataframe from HIT result
            - worker_quality: Dictionary storing initial confusion matrix for each worker
            - iter_num: Number of iterations to perform EM algorithm or until convergence if iter_num is less than 0
            - return_dict: Returns dictionary if true and list if false
            - output: 
                - Sorted list of image urls and their respective string labels
                - Confusion matrix for each worker
        - <i>create_classification_model_input()</i>: Generates CSV input to train classifier with columns as bounding box image file names, bounding boxes, and labels corresponding to each bounding box
- <b>hit_process.py</b>: Contains functions to preprocess inputs for HITs and postprocess HIT outputs
    - <i>create_bounding_image_urls()</i>: Create text file with bounding box input image urls on S3 bucket
    - <i>create_bounding_hit_inputs()</i>: Create input CSVs for the bounding box HIT task
    - <i>crop_images()</i>: Crop bounding box images based on bounding box HIT output and save cropped images
    - <i>create_classification_image_urls()</i>: Create text file with classification input image urls on S3 bucket
    - <i>create_classification_hit_inputs():</i>: Create CSV file inputs for classification HIT given gold standard labels
- <b>train_classifier.py</b>: Trains classifier using Torchvision FastRCNNPredictor model on dataset obtained from aggregating user inputs
    - <i>def parse_bounding_box(bboxes_string)</i>: Converts list of string json objects representing bounding boxes into list of length 4 lists 
        - bboxes_string: list of string json objects
        - output: list of length 4 lists of the form [xmin, ymin, xmax, ymax]
    - <i>def parse_labels(labels_string)</i>: Converts list of string labels  into list of list of tuples
        - labels_string: list of string labels
        - output: list of integers mapping to a unique label
    - MaskDataset Class: Dataset object for our mask data
        - Initialized with a transform object that is applied to every image
        - Each item is of the form (image, annotations) where image is an image tensor and annotations is a dictionary containing bounding boxes and label data
    - <i>collate_fn(batch)</i>: Converts batch data into tuples of lists
        - batch: list (length of list varies by batch size) of tuples of the form (image, annotations)
        - output: tuple of the form (images, annotations)
    - <i>get_model_instance_segmentation(num_classes)</i>: Obtains a pretrained FasterRCNN model with number of categories specificed by num_classes
        - num_classes: the number of classes images make up (by default, FasterRCNN uses 0 as a background model so if you have 3 classes, you must specific num_classes as 4)
        - output: pretrained FasterRCNN model
- <b>generate_model_predictions.py</b>: Computes model bounding box and label predictions on each bounding box image and maps bounding boxes to true bounding boxes
    - <i>calculate_box_overlap(box0, box1)</i>: Calculate percentage overlap between two bounding boxes
        - box0: First bounding box
        - box1: Second bounding box
        - output: overlap percentage
    - <i>map_bounding_boxes(preds, bboxes, threshold)</i>: Map predicted bounding boxes to true bounding boxes if overlap percentage is above threshold
        - preds: model predictions
        - bboxes: true bounding boxes
        - threshold: float representing percentage threshold
        - output: mapped indices of true bounding boxes for each predicted bounding box
    - Execute with --show-ui option to display image with bounding boxes along the way. Press q to quit and any other key to display the next image.
- <b>model_predict.py</b>: Computes model predictions on validation images
    - Default directory path of data/validation_images
    - Execute with -i option followed by a path to a directory with images to predict on different images
- <b>model_validation.py</b>: Prompts users to determine if each bounding box is verifiable, duplicate, unverifiable, or inccorect, label if bounding box if verifiable, and count how many faces that can be labeled but does not have a bounding box
    - <i>get_user_input(frame, x0, y0, dy, num_options)</i>: Gets valid input from user, writes it to frame, and returns it
        - frame: frame to write user input to
        - x0: pixel correponding to left of text
        - y0: pixel corresponding to bottom of text
        - dy: pixel between each line
        - num_options: number of numerical options users can select from
    - Follow the prompts and enter q at any prompt to quit
- <b>quality_control_analysis.py</b>: Analyzes worker performance on gold standard labels and generates insights based on tasks completed and time spent.
    - Reads data/analysis/gold_standard_quality.csv to obtain worker gold standard performancee
    - <i>def worker_task_accuracy_scatter_plot(df)</i>: Plots tasks completed vs accuracy of each worker
        - df: dataframe containing worker gold standard performance data
    - <i>def worker_accuracy_bar_graph(df)</i>: Computes a weighted average of all worker accuracies and displays it in a bar graph
        - df: dataframe containing worker gold standard performance data
    - <i>def worker_time_accuracy_scatter_plot(df)</i>: Plots average time spent on each task vs accuracy of each worker
        - df: dataframe containing worker gold standard performance data
- <b>aggregation_analysis</b>: Computes accuracy on a sample of 500 classification images with true labels for different versions of the EM algorithm
    - <i>compute_accuracies(df, labels)</i>: Computers accuracy given true labels and predicted labels
        - df: dataframe containing true labels
        - labels: dictionary containing predicted labels from workers
    - <i>accuracy_iteration_plot(result_df, true_df, worker_qual)</i> Plots iteration number vs accuracy
        - result_df: dataframe containing results from classification HITs
        - true_df: dataframe containing true labels
        - worker_qual: initial worker quality to use for EM algorithm
    - <i>worker_accuracy_iteration_plot(result_df, true_df, worker_qual)</i> Plots iteration number vs individual worker accuracy
        - result_df: dataframe containing results from classification HITs
        - true_df: dataframe containing true labels
        - worker_qual: initial worker quality to use for EM algorithm
- <b>model_analysis.py</b>: Computes worker and model quality and plots results with baselines
    - <i>calculate_worker_quality(labels)</i>: Calculate worker confusion matrices
        - labels: dictionary mapping image file name to label
        - output: confusion matrices for each worker
    - <i>calculate_preliminary_model_accuracy(labels)</i>: Calculate model confusion matrix from data/analysis.model_image_labels.csv
        - labels: dictionary mapping image file name to label
        - output: confusion matrices for model
    - <i>calculate_model_accuracy()</i>: Calculate model confusion matrices, average scores, and percentage face detection
        - output:
            - 6 x 3 confusion matrix for 6 bounding box categories and 3 face categories
            - List of 6 average scores corresponding to each bounding box category
            - Percentage of faces detected on average
    - <i>accuracy_bar_graph(worker_qual, model_qual, val_model_qual)</i>: Plot accuracy statistics for workers and model in a bar graph
        - worker_qual: confusion matrices for each worker
        - model_qual: model confusion matrix
        - val_model_qual: validation model confusion matrix
    - <i>probability_bar_graph(cm)</i>: Plot probability of each label given the bounding box label in a bar graph
    - <i>scores_bar_graph(scores)</i>: Plot average confidence score for each bounding box category
        - scores: list of average confidence scores for each category
    - <i>detection_rate_pie_chart(detect_rate)</i>: Plot face detection rate and bounding box category makeup
        - detect rate: list containing number of incidences of each bounding box category as well as number of faces not detected
    - <i>scatter_plot(worker_qual, model_qual, val_model_qual)</i>: Plot worker and model quality along with baselines
        - worker_qual: confusion matrices for each worker
        - model_qual: model confusion matrix
        - val_model_qual: model validation confusion matrix
## hit_templates
HTML code for HIT templates
- bounding_box_mockup.html: Template for face bounding box HIT task
- classification_mockup.html: Template for face classification HIT task
## models
Contains models we have trained
- models.txt: Contains links to models in our S3 bucket
## sample_data
Sample data to test quality control and aggregation modules
- sample_hit_result.csv: sample hit result that is input to both the quality control and aggregation module
- sample_qc_out.csv: sample quality control output from gold standard labels
- sample_agg_output.csv: sample EM aggregation output
## webapp
Code to run our Flask webapp
- <b>app.py</b>
    - <i>index()</i>: Renders our home page and handles new prediction button click
    - <i>gen(camera)</i>: Continuously generates frames from camera
        - camera: VideoCamera object
    - <i>video_feed()</i>: Renders video feed from camera
- <b>camera.py</b>: 
    - <i>get_model_instance_segmentation(num_classes)</i>: Refer to the corresponding function in train_classifier.py
    - VideoCamera Class
        - Stores our video source, model, image transformations on initialization
        - <i>get_frame(self)</i>: Returns the generated image frame in bytes with model predictions and generates new predictions if the new prediction button has been pressed
        - <i>set_prediction(self, pred)</i>: Set new_pred variable which determines if get_frame should make a new prediction
            - pred: Boolean that is true if a new prediction should be made
- <b>faster_rcnn_model.pt</b>: Trained FasterRCNN model
- templates: directory containing html files for our webapp
## Future Considerations
We have implemented the full version of our quality control and aggregation modules. We utilize gold standard labels to get an initial quality control check for our EM algorithm to start on. We then let our algorithm converge to receive our labels. That being said, for our final labels that we use to train our classifier, we will cross reference multiple versions of our algorithm and see if they match. For any inconsistencies, we will manually verify the classification label. We expect that there will be few inconsistencies since it should fairly obviously whether a person is wearing their mask correctly or not. In other words, we expect little variance in the data. The versions of our algorithm that we will cross-reference are as follows:
- Converged EM with gold standard label performance as initial quality
- Converged EM assuming all workers are initially perfect
- Majority vote: EM assuming all workers are initially perfect for 1 iteration
- EM with gold standard label performance as initial quality for 1 iteration
# Running Code
After finishing the dev environment setup, you can row the code in the src directory
1. > python hit_process.py
    1. create_bounding_image_urls() parses all images in data/bounding_images and generates data/bounding_images.txt which contains links to all our bounding box images on the S3 bucket.
    2. create_bounding_hit_inputs() then uses those S3 bounding box image urls to generate CSV inputs to our bounding box HITs.
    3. After receiving bounding box HIT results, crop_images() takes in the output in the form of data/bounding_hit_output.csv, crops images based on bounding box labels, and saves the images in data/classification_images.
    4. create_classification_image_urls() parses all images in data/classification_images and generates 'data/classification_images.txt' which contains links to all our classification images on the S3 bucket.
    5. create_classification_hit_inputs() then uses those S3 classification image urls to generate CSV inputs to our classification HITs.
2. > python result_process.py
    1. After receiving classification HIT results, worker_quality(df) reads those results as a df to generate worker quality based on gold standard label performance and also computes a confusion matrix for each worker. Using HIT results and the confusion matrix, it generates data/analysis/gold_standard_quality.csv which contains columns relating to task statistics, accuracy, and whether the worker is a good worker or not.
    2. Using the confusion matrix generated by worker_quality(df) as the initial worker quality, we run out EM algorithm, em_vote(rows, worker_qual, iter_num), for 1 iteration to aggregate our results into a list of tuple (Image, Label).
    3. Using the image labels generated by our EM algorithm and the bounding box HIT results, we generate data/classification_input.csv to train our classifier. It contains the bounding image file and for each bounding image, it stores a list of bounding boxes and a list of labels corresponding to each bounding box as separate columns.
3. > python train_classifier.py
    - Developer and Instructor Note: This code will take several hours to run and you do not need to run it since the model is saved as src/webapp/faster_rcnn_model.py
    1. Since our GPUs do not have enough memory, our model was actually trained on Google Colab. Our classifier works by first constucting a MaskDataset object which feeds inputs to train our classifier. Each item in the dataset is a tuple of the form (Image, Annotations) where Image is a tensor and Annotations contains our bounding boxes and labels for each image. 
    2. We then train a pretrained segmentation model (FasterRCNN) which allows our trained model to segment faces from an image and label them at the same time
4. > cd webapp && python app.py
    1. Runs out Flask webapp which get video input from your camera through OpenCV
    2. Loads our saved model (Instructor Note: If you trained a separate model, it will be under src/models and you can replace src/webapp/faster_rcnn_model.pt)
    3. When the user clicks the New Prediction button, we will prompt our model to make a new prediction on the given frame
# Future Analysis
## Compare aggregation model performance
We trained our model using EM with gold standard label performance as initial quality for 1 iteration but we would like to evaluate other aggregation methods to determine if we can obtain better results. The versions of our algorithm that we will cross-reference are as follows:
- Converged EM with gold standard label performance as initial quality
- Converged EM assuming all workers are initially perfect
- Majority vote: EM assuming all workers are initially perfect for 1 iteration
- EM with gold standard label performance as initial quality for 1 iteration

First we will cross-reference the outputs and determine which files differ in labels between the 4 aggregation methods. We will then have experts(us) label the differing files to determine the true output. We expect that there will not too many differences to the point where we will not be able to label them ourselves. If that is the case, we will simply label a sample size to determine the most accurate aggregation model. We will then revise our model to using the most effective aggregation model.
## Compare model performance against random and majority class baselines
We will calculate expected performance of a random and majority class predictor on our dataset and compare that to our classifier. This will involve parsing our data/analysis/image_labels.csv file to determine the percentage makeup of each class and then computing the expected performance of the majority class and random predictory
## Compare model performance with worker
We plan to test our model on classification images and compare its performance to that of workers to determine if our model is a good worker. To do this, we must run our model on the bounding box HIT images and compute bounding boxes. This is because our model is a segmentation model and not trained to predict on a closeup of a single person's face. We removed duplicate bounding box predictions by computing overlap between boxes and removing those with overlap greater than 70 percent. We also used the same overlap function to map predicted bounding boxes to to true bounding boxes. With this mapping, we were also to determine which classification image our predicted labels corresponded to. 
With worker labels in data/classification_hit_output.csv and our model's predictions, we will compute confusion matrixes and plot the results, along with majority and random baselines. 
## Model bounding box and classification performance
For the preliminary analysis, we primarily analyzed model training performance when it comes to labeling images. For the final analysis, we will gather 100 images from another dataset and have our model run predictions on them. We will then manually go through all predictions and remove duplicate and incorrect face segmentations. We will also make note for each image how many faces there are as well as the correct labels for each face. 
With this, we can determine how well the model can recognize faces, how often it predicts bounding boxes on duplicate faces, how often it predicts bounding boxes on things that are not faces, as well as the confusion matrix of the model after predicting on all 100 images. We will then plot our analysis of bounding box and classification performance. 
# Running Analysis Code
1. > python generate_model_predictions.py
    - To show images with predicted and true bounding boxes run:
    > python generate_model_predictions.py --show-ui
    - Press q to quit and any other key to display the next image.
    - Developer and Instructor Note: This code will take several hours to run and you do not need to run it because the output csv is saved as data/analysis/model_image_labels.csv. Running it will rewrite the output csv so if you do not run the script in full, be sure to reset the git repository.
    1. Reads data/classifier_input.csv to get true bounding boxes and labels for each image
    2. Make predictions on each image using model/faster_rcnn_model.pt and remove duplicate bounding boxes
    3. Map predicted bounding boxes to true bounding boxes
    4. Display predicted bounding boxes in color and true bounding boxes in black if code was run with --show-ui option
    5. Save predicted labels for each bounding box image in data/analysis/model_image_labels.csv
2. > python model_predict.py
    - Defaults to data/validation_images directory
    - To specify a different directory, run with -i option followed by path
    - Developer and Instructor Note: This code will take an hour to run and you do not need to run it because the output csv is saved as data/analysis/model_image_preds.csv.
    1. Reads all images in the validation image directory
    2. Compute model predictions on all validation images
    3. Save predictions in data/analysis/model_image_preds.csv
3. > python model_validation.py
    - Defaults to data/validation_images directory
    - To specify a different directory, run with -i option followed by path
    - Developer and Instructor Note: This code requires manual work and you do not need to run it because the output csv is saved as data/analysis/model_performance.csv. Saves the work in the output csv as you go so if you want to test, you must first delete the output csv.
    1. Displays bounding boxes for each image to users 1 by 1
    2. Asks user to determine if bounding box is:
        - Verifiable (You can label the face in the image)
        - Duplicate (There already exists a bounding box over the same face)
        - Unverifiable (The face in the bounding is too blurry or small to be labeled)
        - Incorrect (The bounding box does not capture a face)
    3. If the bounding box is verifiable, we ask to user to label the face
    4. After all bounding boxes have been labeled, we ask the user how many additional faces they can label that does not have a bounding box
    5. Saves the user input to data/analysis/model_performance.csv
4. > python quality_control_analysis.py
    1. Reads worker gold standard performance from data/analysis/gold_standard_quality.csv
    2. Plots tasks completed vs accuracy
    3. Plots bar graph of average worker accuracy for each category
    4. Plots average time spent on each task vs accuracy
5. > python aggregation_analysis.py
    1. Reads the classification hit output as well as true labels for 500 images in the classification hit output
    2. Runs the EM algorithm with gold standard label performance as initial worker quality and plots iteration number vs accuracy on the 500 images
    3. Runs the EM algorithm without initial worker quality (assumes workers are initially perfect) and plots iteration number vs accuracy on the 500 images
    4. Runs the EM algorithm with gold standard label performance as initial worker quality and plots iteration number vs individual worker accuracy on the 500 images
    5. Runs the EM algorithm without initial worker quality (assumes workers are initially perfect) and plots iteration number vs individual worker accuracy on the 500 images
6. > python model_analysis.py
    1. Reads true classification image labels from data/analysis/image_labels.csv
    2. Compute worker confusion matrices by comparing results in data/classification_hit_output.csv with true labels
    3. Compute model confusion matrix by comparing data/analysis/model_image_labels.csv and true image labels
    4. Compute model validation confusion matrix by readding data/analysis/model_performance.csv
    5. Plots accuracy statistics for workers and our model using the respective confusion matrices
    6. Plots probability distribution for each bounding box categories
    7. Plots average confidence scores for each bounding box categories
    8. Plots pie charts for face detection rate and bounding box category makeup
    9. Plots images labeled vs accuracy for workers and model along with majority and random baselines