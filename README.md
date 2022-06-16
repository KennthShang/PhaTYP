![PhaTYP](logo.png)

PhaTYP is a python library for bacteriophages' lifestyle prediction. PhaTYP is a BERT-based model and rely on protein-based vocabulary to convert DNA sequences into sentences for prediction. 

# Overview
The main function of PhaTYP is to predict the lifestyles (virulent or temperate) of phage-like contigs. The input of the program should be fasta files and the output will be a csv file showing the predictions. Since it is a Deep learning model, if you have GPU units on your PC, we recommand you to use them to save your time. 

If you have any trouble installing or using PhaTYP, please let us know by emailing us (jyshang2-c@my.cityu.edu.hk).


## Required Dependencies
* Python 3.x
* Numpy
* Pandas
* Pytorch>1.8.0
* transformer
* datasets
* [Diamond](https://github.com/bbuchfink/diamond)
* [Prodigal](https://github.com/hyattpd/Prodigal)


If you want to use the gpu to accelerate the program:
* cuda
* Pytorch-gpu

* For cpu version pytorch: `conda install pytorch torchvision torchaudio cpuonly -c pytorch`
* For gpu version pytorch: Search [pytorch](https://pytorch.org/) to find the correct cuda version according to your computer

### Quick install
*Note*: we suggest you to install all the package using conda (both miniconda and [Anaconda](https://anaconda.org/) are ok).

After cloning this respository, you can use anaconda to install the **PhaTYP.yaml**. This will install all packages you need with gpu mode (make sure you have installed cuda on your system to use the gpu version. Othervise, it will run with cpu version). The command is: `conda env create -f PhaTYP.yaml -n phatyp`


### Prepare the database and environment
Due to the limited size of the GitHub, we zip the database. Before using PhaTYP, you need to unpack them using the following commands.

1. When you use PhaTYP at the first time
```
cd PhaTYP/
conda env create -f PhaTYP.yaml -n phatyp
conda activate phatyp
cd database/
bzip2 -d database.fa.bz2
cd ..

fileid="1tsUArctGf9Fd3xa-0sEcp6ykwxTy9uxG"
filename="model.zip"
html=`curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}"`
curl -Lb ./cookie "https://drive.google.com/uc?export=download&`echo ${html}|grep -Po '(confirm=[a-zA-Z0-9\-_]+)'`&id=${fileid}" -o ${filename}

unzip model.zip
```
*Note:* **Please check whether the pytorch_model.bin is larger than 200M before using PhaTYP**
* Because the parameter is larger than 200M, we cannot upload it to GitHub directly. Please make sure you have downloaded model.zip correctly.
* if you cannot download the *model.zip* from the command lines above, please use the [Google Drive link](https://drive.google.com/file/d/1tsUArctGf9Fd3xa-0sEcp6ykwxTy9uxG/view?usp=sharing) to download it and place it in the *database/* folder. 



2. If the example can be run without any bugs, you only need to activate your 'phatyp' environment before using PhaTYP.
```
conda activate phatyp
```


## Usage

```
python preprocessing.py [--contigs INPUT_FA] [--len MINIMUM_LEN] [--midfolder DIR]
python PhaTYP.py [--out OUTPUT_CSV] [--midfolder DIR]
```

**Options**


      --contigs INPUT_FA
                            input fasta file
      --len MINIMUM_LEN
                            predict only for sequence >= len bp (default 3000)
      --out OUTPUT_CSV
                            The output csv file (prediction)
      --midfolder DIR
                            Folder to store the intermediate files (default phatyp/)

**Example**

Prediction on the example file:

    python preprocessing.py --contigs test_contigs.fa
    python PhaTYP.py --out example_prediction.csv

The prediction will be written in *example_prediction.csv*. The CSV file has three columns: contigs names, prediction, and prediction score. The test_contig.fasta contain a phage genome, so the output is phage.
    
### References (will be avaliable soon)
The arXiv version can be found via: [PhaTYP: Predicting lifestyle for bacteriophages using BERT]()

### Contact
If you have any questions, please email us: jyshang2-c@my.cityu.edu.hk


