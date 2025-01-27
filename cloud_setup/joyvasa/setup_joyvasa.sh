# reference: https://github.com/jdh-algo/JoyVASA

# Install CUDA
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.6.3/local_installers/cuda-repo-ubuntu2204-12-6-local_12.6.3-560.35.05-1_amd64.deb
dpkg -i cuda-repo-ubuntu2204-12-6-local_12.6.3-560.35.05-1_amd64.deb
cp /var/cuda-repo-ubuntu2204-12-6-local/cuda-*-keyring.gpg /usr/share/keyrings/
apt-get update
apt-get -y install cuda-toolkit-12-6

# Install git-lfs
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
apt-get install git-lfs

# Install JoyVASA
git clone https://huggingface.co/jdh-algo/JoyVASA
cd JoyVASA
pip install -r requirements.txt
apt-get update  
apt-get install ffmpeg -y

cd src/utils/dependencies/XPose/models/UniPose/ops
python setup.py build install
cd -

# Install Chinese-Hubert
git clone https://huggingface.co/TencentGameMate/chinese-hubert-base
cd chinese-hubert-base
cd -

# Install Wav2Vec2
git lfs install
git clone https://huggingface.co/facebook/wav2vec2-base-960h
cd -

# Install LivePortrait
huggingface-cli download KwaiVGI/LivePortrait --local-dir pretrained_weights --exclude "*.git*" "README.md" "docs"