![PhaTYP](logo.png)

PhaTYP is a python library for bacteriophages' lifestyle prediction. PhaTYP is a BERT-based model and rely on protein-based vocabulary to convert DNA sequences into sentences for prediction.



## News !!!

1. This folder will be no longer maintained. The program has been updated and move to PhaBOX [https://github.com/KennthShang/PhaBOX], which is more user-friendly. Hope you will enjoy it.

2. Our web server for phage-related tasks (including phage identification, taxonomy classification, lifestyle prediction, and host prediction) is available! You can visit [https://phage.ee.cityu.edu.hk/] to use the GUI. We also provided more detailed intermediate files and visualization for further analyzation. 


# Overview
The main function of PhaTYP is to predict the lifestyles (virulent or temperate) of phage-like contigs. The input of the program should be fasta files and the output will be a csv file showing the predictions. Since it is a Deep learning model, if you have GPU units on your PC, we recommand you to use them to save your time.

If you have any trouble installing or using PhaTYP, please let us know by emailing us (jyshang2-c@my.cityu.edu.hk).

### Quick install
*Note*: we suggest you to install all the package using conda (both miniconda and [Anaconda](https://anaconda.org/) are ok).

After cloning this respository, you can use anaconda to install the **phatyp.yaml**. This will install all packages you need with gpu mode (make sure you have installed cuda on your system to use the gpu version. Othervise, it will run with cpu version). The command is: `conda env create -f phatyp.yaml -n phatyp`

If you want to use the gpu to accelerate the program:
* cuda
* Pytorch-gpu

* For cpu version pytorch: `conda install pytorch torchvision torchaudio cpuonly -c pytorch`
* For gpu version pytorch: Search [pytorch](https://pytorch.org/) to find the correct cuda version according to your computer


### Prepare the database and environment
Due to the limited size of the GitHub, we zip the database. Before using PhaTYP, you need to unpack them using the following commands.

1. When you use PhaTYP at the first time
```
cd PhaTYP/
conda env create -f phatyp.yaml -n phatyp
conda activate phatyp

fileid="1tsUArctGf9Fd3xa-0sEcp6ykwxTy9uxG"
filename="model.zip"
html=`curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}"`
curl -Lb ./cookie "https://drive.google.com/uc?export=download&`echo ${html}|grep -Po '(confirm=[a-zA-Z0-9\-_]+)'`&id=${fileid}" -o ${filename}

unzip model.zip
pip install .
```
*Note:* **Please check whether the pytorch_model.bin is larger than 200M before using PhaTYP**
* Because the parameter is larger than 200M, we cannot upload it to GitHub directly. Please make sure you have downloaded model.zip correctly.
* if you cannot download the *model.zip* from the command lines above, please use the [Google Drive link](https://drive.google.com/file/d/1tsUArctGf9Fd3xa-0sEcp6ykwxTy9uxG/view?usp=sharing) to download it and place it under the *PhaTYP/* root folder.



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

### Dataset and retraining the model
Detailed information can be found in 'train/' folder

### Updates
We added a parameter called 'prodigal' for you to use different versions of the prodigal. You can use the path of your prodigal. Or if you have added your prodigal into your env path, you can use the path's name.

```
python preprocessing.py --contigs test_contigs.fa --prodigal prodigal-gv

OR

python preprocessing.py --contigs test_contigs.fa --prodigal /path/to/prodigal/prodigal-gv
```

### References

PhaTYP was accpeted by Briefings in Bioinformatcs: [PhaTYP: Predicting lifestyle for bacteriophages using BERT](https://doi.org/10.1093/bib/bbac487)

Jiayu Shang, Xubo Tang, Yanni Sun, PhaTYP: predicting the lifestyle for bacteriophages using BERT, Briefings in Bioinformatics, 2022;, bbac487, https://doi.org/10.1093/bib/bbac487

The arXiv version can be found via: [PhaTYP: Predicting lifestyle for bacteriophages using BERT](https://arxiv.org/abs/2206.09693)


### Contact
If you have any questions, please email us: jyshang2-c@my.cityu.edu.hk


