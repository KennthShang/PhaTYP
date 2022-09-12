# Retraining PhaTYP

There are two separate parts for retraining PhaTYP: self-supervised pre-train step (*pretrain.py*) and fine-tuning step (*finetune.py*). For both step, you need to generate the pc sentence using `preprocessing.py` first.

You can use the following command to convert your data into pc sentences (make sure your are under the 'PhaTYP/' folder):

      python preprocessing.py [--contigs INPUT_FA] [--len MINIMUM_LEN] [--midfolder DIR]

Then, you can switch into the 'train/' folder and run the `script.py` to generate the inputs of `pretrain.py` and `finetune.py`:

      python script.py [--midfolder DIR] [--out FILE_NAME] [--mode pretrain or finetine]


For example, if you want to generate a input for *pretrain.py* using the *test_contigs.fa*, you can run the following commands:

      python preprocessing.py --contigs test_contigs.fa --midfolder phatyp
      cd train/
      python script.py --midfolder ../phatyp --out train.csv --mode pretrain
 
**NOTE1:** one last thing you need to do is to add labels for the the inputs of *finetune.py* according to your contigs (1 for tempearte and 0 for virulent). Because self-supervised pre-train do not need labels for training you can directly use the output files of *script.py* as inputs. The example files can be found in the 'example/' folder. 

**NOTE2:** The **pretrain.py** will generate the pretrain model and store in 'log/' folder. Then the **finetune.py** will load the model from 'log/' as initial paprameters. The finetuned model will be stored in 'model/' folder.
      
### Example commands for *pretrain.py*
      
      python pretrain.py --train train.csv --val val.csv
      
### Commands for *finetune.py*
      
      python finetune.py --train train.csv --val val.csv


**NOTE:** Because training bert require lots of computational resource, we highly recommand you to use multiple gpu units to run pretrain.py and finetune.py. (It takes nearly a week to train the self-supervised task with 4 2080Ti). To run the code with multiple gpus, you can simply change `python` into `torchrun --nproc_per_node=n`. Please replace n with the number of gpus you have on your device. However, the will not take much time if you only use the prediction mode of PhaTYP (the provided parameters) with no gpu units.


## Dataset
All the dataset used in the paper can be found via [google drive](https://drive.google.com/file/d/100xUuwETTbNWpuWvUm5o-ENTOFcOFe6Z/view)
