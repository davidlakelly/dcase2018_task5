# Dataset directory
$DEV_DATASET_DIR="C:\Users\David\Desktop\dcase_5\dcase2018_task5\DCASE2018-task5-dev"
$EVAL_DATASET_DIR="C:\Users\David\Desktop\dcase_5\dcase2018_task5\DCASE2018-task5-eval"

# You need to modify this path
$WORKSPACE="C:\Users\David\Desktop\dcase_5\dcase2018_task5"

$BACKEND="pytorch"
$HOLDOUT_FOLD=1
$GPU_ID=1
$CUDA_VISIBLE_DEVICES=$GPU_ID 

# Check files
python utils/features.py checkfiles --dataset_dir=$DEV_DATASET_DIR
python utils/features.py checkfiles --dataset_dir=$EVAL_DATASET_DIR

python utils/features.py logmel --dataset_dir=$DEV_DATASET_DIR --workspace=$WORKSPACE
python utils/features.py logmel --dataset_dir=$EVAL_DATASET_DIR --workspace=$WORKSPACE

$HOLDOUT_FOLD=1
$CUDA_VISIBLE_DEVICES=$GPU_ID 

python $BACKEND/main_pytorch.py train --dataset_dir=$DEV_DATASET_DIR --workspace=$WORKSPACE --validate --holdout_fold=$HOLDOUT_FOLD --cuda


python $BACKEND/main_pytorch.py inference_validation_data --dataset_dir=$DEV_DATASET_DIR --workspace=$WORKSPACE --holdout_fold=$HOLDOUT_FOLD --iteration=5000 --cuda

######################## Full train ########################

python $BACKEND/main_pytorch.py train --dataset_dir=$DEV_DATASET_DIR --workspace=$WORKSPACE --cuda



python $BACKEND/main_pytorch.py inference_testing_data --workspace=$WORKSPACE --iteration=5000 --cuda