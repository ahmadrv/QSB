# Download Miniconda file
wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.1.0-1-Linux-x86_64.sh \
-O ~/miniconda.sh

# Install Miniconda
CONDA_DIR=$HOME/miniconda3
chmod +x ~/miniconda.sh
~/miniconda.sh -b -p $CONDA_DIR
rm ~/miniconda.sh

# Conda initilization
~/miniconda3/bin/conda init
source ~/.bashrc