# [Optimal Decision Making <br />&emsp;&emsp;&emsp;&emsp;in High-Throughput Virtual Screening Pipelines](https://arxiv.org/abs/2109.11683)

## Table of contents
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Links](#links)
- [Contact](#Contact)
  
## Installation
To avoid conflicts between installed packages, it is highly recommended to create an independent virtual environment.
#### 1. Install Anaconda from [https://www.anaconda.com/download/](https://www.anaconda.com/download/).
#### 2. Create a virtual environment.
```
conda create --name your-environment-name python=3.10.9
```
#### 3. Activate the virtual environment.
```
conda activate your-environment-name
```
#### 4. Install additional Python packages. 
```
pip install numpy>=1.25.0
pip install scipy>=1.10.1
pip install pandas>=2.0.2
pip install scikit-learn>=1.2.2
pip install matplotlib>=3.7.1
pip install seaborn>=0.12.2
pip install openpyxl>=3.1.2
```
#### (Optional) Install Visual Studio Code from [https://code.visualstudio.com/Download/](https://code.visualstudio.com/Download).

## Usage
### Reproducing the simulation results presented in the manuscript.
```
python main_framework1_analytic.py % Reproduce the analytic simulation results based on the first optimization framework.
python main_framework2_analytic.py % Reproduce the analytic simulation results based on the second optimization framework.
python plotAnalyticResultsManuscript.py % Plot and save the analytic simulation results.

python main_framework1_ncRNAScreening.py % Reproduce the long non-coding RNA sequence screening simulation results based on the first optimization framework
python main_framework2_ncRNAScreening.py % Reproduce the long non-coding RNA sequence screening simulation results based on the second optimization framework
python plotncRNAScreeningManuscript.py % Plot and save the long non-coding RNA sequence screening simulation results.
```

### Applying to your own dataset.
#### 1. Format the training dataset.
<img src="https://github.com/bjyoontamu/occ/blob/main/images/training-dataset.JPG" width="700" />

###### * For more details, take a look at the training dataset of the long non-coding RNA screening campaign in [https://github.com/bjyoontamu/occ/tree/main/data/](https://github.com/bjyoontamu/occ/tree/main/data).

#### 2. Update the source code to accomodate the constructed high-throughput virtual screening pipeline.

###### * For the first optimization framework, use [main_framework1_ncRNAScreening.py](https://github.com/bjyoontamu/occ/blob/main/main_framework1_ncRNAScreening.py). For the second, use [main_framework2_ncRNAScreening.py](https://github.com/bjyoontamu/occ/blob/main/main_framework2_ncRNAScreening.py).

#### 3. Run the source code to find the optimal screening policy.
```
# For the first optimization framework
python main_framework1_ncRNAScreening.py 
# For the second optimization framework
python main_framework2_ncRNAScreening.py
```

#### 4. Use the identified optimal screening policy for your own high-throughput virtual screening pipeline.

## License
The source code is licensed under the terms of the MIT Open Source
license and is available for free.

## Links
* [arXiv preprint](https://arxiv.org/abs/2109.11683)

## Contact
Byung-Jun Yoon [bjyoon@tamu.edu]<br />
Hyun-Myung Woo [hmwoo@inu.ac.kr]

