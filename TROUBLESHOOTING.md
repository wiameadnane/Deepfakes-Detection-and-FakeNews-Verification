# Troubleshooting Guide

## TensorFlow DLL Load Error on Windows

### Problem
```
ImportError: DLL load failed while importing _pywrap_tensorflow_internal
```

### Solutions (try in order):

#### Solution 1: Install Microsoft Visual C++ Redistributable
TensorFlow requires Microsoft Visual C++ Redistributable to be installed.

1. Download and install [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
2. Restart your computer
3. Try running the application again

#### Solution 2: Use TensorFlow CPU version with specific compatibility
```bash
# Activate your virtual environment first
venv\Scripts\activate

# Uninstall current TensorFlow
pip uninstall tensorflow tensorflow-gpu keras

# Install compatible version
pip install tensorflow==2.10.1
pip install keras==2.10.0
```

#### Solution 3: Check Python Version
TensorFlow 2.12+ requires Python 3.8-3.11. Check your Python version:
```bash
python --version
```

If you have Python 3.12+, you need to either:
- Use Python 3.11 or lower, OR
- Use TensorFlow 2.15+ (experimental support)

#### Solution 4: Install TensorFlow with specific build
For Windows, try the CPU-only version which has fewer dependency issues:
```bash
pip uninstall tensorflow
pip install tensorflow-cpu==2.10.1
```

#### Solution 5: Check System Architecture
Ensure you're using 64-bit Python on a 64-bit Windows system:
```bash
python -c "import struct; print(struct.calcsize('P') * 8)"
```
Should output `64`. If it outputs `32`, install 64-bit Python.

### Recommended Quick Fix for This Project

Since you're on Windows, the most reliable solution is:

```bash
# Activate virtual environment
venv\Scripts\activate

# Uninstall problematic packages
pip uninstall -y tensorflow keras mtcnn

# Install compatible versions
pip install tensorflow-cpu==2.10.1
pip install keras==2.10.0
pip install mtcnn==0.1.1

# Test the installation
python -c "import tensorflow as tf; print(tf.__version__)"
```

### Alternative: Use TensorFlow 2.15+ (Latest)

If the above doesn't work, try the latest version which has better Windows support:

```bash
pip uninstall -y tensorflow keras
pip install tensorflow==2.15.0
pip install keras==2.15.0
```

### Verify Installation

After fixing, test TensorFlow:
```bash
python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__); print('GPU available:', tf.config.list_physical_devices('GPU'))"
```

### Additional Notes

- **GPU Support**: If you need GPU support, you'll need to install CUDA and cuDNN separately
- **Anaconda Users**: If using Anaconda, consider using `conda install tensorflow` instead of pip
- **WSL2**: You're using WSL2 according to your system info. Consider running the Python app from Linux side of WSL2 for better compatibility

## Other Common Issues

### Issue: "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### Issue: "NEWSAPI_KEY not found"
- Make sure you created `.env` file in the project root
- Verify the file contains: `NEWSAPI_KEY=your_actual_api_key`
- Ensure there are no quotes around the API key

### Issue: "No module named 'PyQt6'"
```bash
pip install PyQt6
```

### Issue: MoviePy errors
```bash
pip install moviepy decorator imageio imageio-ffmpeg
```

### Issue: Whisper model download fails
- The first run will download the Whisper model (~140MB)
- Ensure you have stable internet connection
- Model is cached in `~/.cache/whisper/`