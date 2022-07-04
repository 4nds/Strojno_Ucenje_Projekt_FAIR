Prema:
https://towardsdatascience.com/fine-tuning-pre-trained-transformer-models-for-sentence-entailment-d87caf9ec9db

BERT entailment proveden je s ciljem bolje klasifikacije agree/disagree/discuss.  
Podatci iz dataseta s odnosom "unrelated" su zanemareni.  
Provedeno je 10 epoha treniranja.  
Rezultati prikazani kao omjer broja točne i broja netočne klasifikacije na setu podataka za bodovanje u natjecanju.  


Epoch 1: train_loss: 0.4410 train_acc: 0.8237 | val_loss: 0.2086 val_acc: 0.9294 00:18:12.73

Epoch 2: train_loss: 0.1123 train_acc: 0.9634 | val_loss: 0.1021 val_acc: 0.9714 00:15:47.92

Epoch 3: train_loss: 0.0461 train_acc: 0.9866 | val_loss: 0.0981 val_acc: 0.9729 00:15:14.07

Epoch 4: train_loss: 0.0291 train_acc: 0.9913 | val_loss: 0.1075 val_acc: 0.9706 00:15:10.50

Epoch 5: train_loss: 0.0224 train_acc: 0.9935 | val_loss: 0.1148 val_acc: 0.9758 00:15:27.62

Epoch 6: train_loss: 0.0116 train_acc: 0.9967 | val_loss: 0.1107 val_acc: 0.9758 00:28:36.22

Epoch 7: train_loss: 0.0135 train_acc: 0.9959 | val_loss: 0.1229 val_acc: 0.9747 00:29:02.09

Epoch 8: train_loss: 0.0189 train_acc: 0.9949 | val_loss: 0.1431 val_acc: 0.9743 00:33:40.45

Epoch 9: train_loss: 0.0121 train_acc: 0.9965 | val_loss: 0.1328 val_acc: 0.9777 00:31:41.29

EPOCH = 10 (točno klasificirani : netočno klasificirani)  
Agree: 1014 : 889  
Discuss: 3770 : 694   
Disagree: 271 : 426  
Epoch 10: train_loss: 0.0104 train_acc: 0.9968 | val_loss: 0.1364 val_acc: 0.9784  
00:19:58.83



















