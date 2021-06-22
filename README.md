# oct-choroid-seg
Code for the paper "Automatic choroidal segmentation in OCT images using supervised deep learning methods"

Link: https://www.nature.com/articles/s41598-019-49816-4

If the code and methods here are useful to you and aided in your research, please consider citing the paper.

# Dependencies 
* Python 3.6.4
* Keras 2.4.3
* tensorflow 2.3.1
* h5py
* Matplotlib
* numpy

# BioTeam Github Guidance

## Inspect example_data.hdf5

Extract images and segmentation files from example_data.hdf5 with `hdf5readimages.py`

## Run with example_data.hdf5

For a quick test use `epochs = 100` in train_script_semantic_general.py instead of 10000

1. Create `results` and `data` directories at same level of .git  
2. Add the paths to file `parameters.py` (Example: DATA_LOCATION = '/Users/user1/git/ML-Image-Segmentation/data/')
3. Install a conda environment with

`conda env create --name ml_env --file environment.yml`

4. Activate the conda environment with `conda activate ml_env` and run 

`python train_script_semantic_general.py`

### What to expect

* During training, the dice_coef (Dice Coefficient) increases as tensorflow converges on a better model
* The results directory has one `config.hdf5` file and several hdf5 files asigned to  an `epoch` number 
* To read any hdf5 file from the `results` directory, run `hdf5scan.py`

## BioTeam version: Train by reading images from a directory

1. Create `INPUT_LOCATION` directory at same level of .git with sub-directories 
   with expected names train_images, train_segs, val_images, val_segs, test_images, test_segs
2. Copy the files in the corresponding directories. __A minimum of 3 train and val files is required for training__
3. Add the `INPUT_LOCATION` path to file `parameters.py`
4. Set BIOTEAM constant  = 1 in train_script_semantic_general.py and save the file
5. As before activate the conda environment with `conda activate ml_env` and run 

`python train_script_semantic_general.py`

### What to expect
1. readdirimages.py will create an hdf5 file `img_data.hdf5` with the images and segs files in the same format as the `example_data.hdf5`
2. `img_data.hdf5` can be read with `hdf5readimages.py`
3. `img_data.hdf5` cannot be used as input to the original Kugelman et al code (BIOTEAM = 0) because it contains areas, not boundaries
4. Al other files and results are in the same format as before

# Training a model (patch-based)
1. Modify *load_training_data* and *load_validation_data* functions in *train_script_patchbased_general.py* to load your training and validation data (see comments in code). [see example data file and load functions]
2. Choose one of the following and pass as first training parameter as shown in code:
    * *model_cifar* (Cifar CNN)
    * *model_complex* (Complex CNN) [default]
    * *model_rnn* (RNN)
3. Can change the desired patch size (*PATCH_SIZE*) as well as the name of your dataset (*DATASET_NAME*).
4. Run *train_script_patchbased_general.py*
5. Training results will be saved in the location defined by *parameters.RESULTS_LOCATION*. Each new training run will be saved in a new seperate folder named with the format: 
(*TIMESTAMP*) _ (*MODEL_NAME*) _ (*DATASET_NAME*). Each folder will contain the following files:
    * *config.hdf5* (summary of parameters used for training)
    * *stats_epoch#.hdf5* (training and validation results for each epoch up to epoch #)
    * one or more *model_epoch&.hdf5* files containing the saved model at each epoch &
  
# Training a model (semantic)
1. Modify *load_training_data* and *load_validation_data* functions in *train_script_semantic_general.py* to load your training and validation data (see comments in code). [see example data file and load functions]
2. Choose one of the following and pass as first training parameter as shown in code:
    * *model_residual* (Residual U-Net)
    * *model_standard* (Standard U-Net) [default]
    * *model_sSE* (Standard U-Net with sSE blocks)
    * *model_cSE* (Standard U-Net with cSE blocks)
    * *model_scSE* (Standard U-Net with scSE blocks)
3. Can change the name of your dataset (*DATASET_NAME*).
4. Run *train_script_semantic_general.py*
5. Training results will be saved in the location defined by *parameters.RESULTS_LOCATION*. Each new training run will be saved in a new seperate folder named with the format: 
(*TIMESTAMP*) _ (*MODEL_NAME*) _ (*DATASET_NAME*). Each folder will contain the following files:
    * *config.hdf5* (summary of parameters used for training)
    * *stats_epoch#.hdf5* (training and validation results for each epoch up to epoch #)
    * one or more *model_epoch&.hdf5* files containing the saved model at each epoch &
  
# Evaluating a model (patch-based)
1. Modify *load_testing_data* function in *eval_script_patchbased_general.py* to load your testing data (see comments in code). [see example data file and load function]
2. Specify trained network folder to evaluate.
3. Specify filename of model to evaluate within the chosen folder: *model_epoch&.hdf5*
4. Run *eval_script_patchbased_general.py*
5. Evaluation results will be saved in a new folder (with the name *no_aug_(DATASET_NAME).hdf5*) within the specified trained network folder. Within this, a folder is created for each evaluated image containing a range of .png images illustrating the results qualitatively as well as an *evaluations.hdf5* file with all quantitative results. A new *config.hdf5* file is created in the new folder as well as *results.hdf5* and *results.csv* files summarising the overall results after all images have been evaluated.
  
# Evaluating a model (semantic)
1. Modify *load_testing_data* function in *eval_script_semantic_general.py* to load your testing data (see comments in code). [see example data file and load function]
2. Specify trained network folder to evaluate.
3. Specify filename of model to evaluate within the chosen folder: *model_epoch&.hdf5*
4. Run *eval_script_semantic_general.py*
5. Evaluation results will be saved in a new folder (with the name *no_aug_(DATASET_NAME).hdf5*) within the specified trained network folder. Within this, a folder is created for each evaluated image containing a range of .png images illustrating the results qualitatively as well as an *evaluations.hdf5* file with all quantitative results. A new *config.hdf5* file is created in the new folder as well as *results.hdf5* and *results.csv* files summarising the overall results after all images have been evaluated.

# Still to be added
* *RNN bottleneck* and *Combined* semantic network models
* Code and instructions for preprocessing using contrast enhancement (Girard filter)