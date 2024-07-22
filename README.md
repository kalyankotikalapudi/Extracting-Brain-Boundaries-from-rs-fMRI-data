This repository houses a comprehensive suite of projects that analyze resting state functional magnetic resonance imaging (rs-fMRI) scans. The analysis includes boundary extraction, cluster detection, and supervised machine learning classification.

Project Overview
These projects collectively aim to automate the processing of rs-fMRI data to facilitate various analyses:

Brain Boundary Extraction: Automatically extract brain slices and their boundaries from spatial independent component images.
Semi-supervised Cluster Detection: Apply clustering techniques to detect and count significant clusters in the extracted brain slices.(DBSCAN)
Supervised Classification of IC Images: Classify IC images as Noise or Resting State Network (RSN) using supervised machine learning techniques.(VGG16 Deep learning model)

Objectives
Extract and identify brain boundaries and slices from spatial ICs.
Detect the number of clusters within these slices using unsupervised learning.
Classify IC images as either Noise or RSN using supervised learning techniques.

Technology Requirements
Python 3.6 to 3.9
Repository Contents

brainExtraction.py: Extracts brain slices and boundaries from IC images.
clustering.py: Performs unsupervised cluster detection on brain slices.
classification.py: Trains and applies a machine learning model for IC image classification.
test.py: Generic testing script to validate each part of the project using a folder named testPatient.

Additional utility scripts and configuration files as needed. Also there is an ETL pipline initially to consolidate data into a unified database and this was done not as per requiremnet of project just to practical knowledge on ETL

Usage
Boundary Extraction: Run brainExtraction.py to process images and extract boundaries.
Cluster Detection: After extracting slices, run clustering.py to detect clusters.
Classification: With the labeled dataset, use classification.py to train and test the model for binary classification.
