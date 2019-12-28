#When running on HPC
module load cuda/9.0
module load cudnn/v7.0.5-prod-cuda-9.0
module load opencv/3.2.0

cp cfg/Makefile_hpc darknet/Makefile

cd darknet

make
