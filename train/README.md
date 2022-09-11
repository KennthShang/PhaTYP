# Retraining PhaTYP

There are two separate parts for retraining PhaTYP: self-supervised pre-train step (*pretrain.py*) and fine-tuning step (*finetune.py*). For both step, you need to generate the pc sentence using `preprocessing.py` first.

You can use the following command to convert your data into pc sentences (make sure your are under the 'PhaTYP/' folder):

      python preprocessing.py [--contigs INPUT_FA] [--len MINIMUM_LEN] [--midfolder DIR]

Then, you can swith into the 'train/' folder and run the `script.py` to generate the inputs of `pretrain.py` and 'finetune.py':

      python script.py [--midfolder DIR] [--out FILE_NAME]


For example, if you want to generate a input for *pretrain.py* using the *test_contigs.fa*, you can run the following commands:

      python preprocessing.py --contigs test_contigs.fa --midfolder phatyp
      cd train/
      python script.py --midfolder ../phatyp --out train.csv
 
**NOTE:** one last thing you need to do is to add labels for the the inputs of *finetune.py* according to your contigs (1 for tempearte and 0 for virulent). Because self-supervised pre-train do not need labels for training you can directly use the output files of *script.py* as inputs. The example files can be found in the 'example/' folder. 

      
### Commands for *pretrain.py*
      
      python pretrain.py --train train.csv --val val.csv
      
### Commands for *finetune.py*
      
      python finetune.py --train train.csv --val val.csv
