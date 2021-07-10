# Differential Cryptanalysis on Substitution–Permutation Network

In this project, a differential cryptanalysis has been worked on a basic algorithm named as toy cipher. This algorithm has a SPN network which consist of four rounds. (substitution-permutation network). There are S-box layer, P-box layer and key mixing layer.

* Plaintext: 16-bits
* Key: 32-bits
* Ciphertext: 16-bits

In our cipher, the data block has been xored with 16-bit sub-key which has been generated from 32-bit masterkey. The  16-bit  data block has been broken into four 4-bit sub-blocks. Each sub-block has been assigned to s-boxes receiving 4-bit size input. The most fundamental property of an S-box is that it is a nonlinear mapping. And the permutation layer of a round is simply the tranposition of the bits or the permutation of the bit positions. The whole algorithm is shown in the figure 1.

<p align="center">
  <img src="https://raw.githubusercontent.com/sumeyyekucukdemir/cryptanalysis/main/img/toycipher.png" height="738px" width="425px">
</p>

Differential attack is a chosen plaintext attack so many  plaintext has been generated randomly. Differential cryptanalysis exploits the high probability of certain occurrences of plaintext differences and differences into the last round of the ciphertext. The DDT (Differential Distribution Table) has been constructed which tabularize the complete data for an S-box in a difference distribution table in which the rows represent input difference values (in hexadecimal) and the columns represent output  differences values (in hexadecimal). Each element of the table represents the number of occurrences of the corresponding output difference value given the input difference. The pair in the table is called differential and these differential can combined to form a differential trial. Large values in the table decide the differential trial.DDT table is shown in figure 2.

<p align="center">
  <img src="https://raw.githubusercontent.com/sumeyyekucukdemir/cryptanalysis/main/img/DDT.png">
</p>

The following difference pairs of the S-box has been used in our algorithm :

<p align="center">
  <img src="https://raw.githubusercontent.com/sumeyyekucukdemir/cryptanalysis/main/img/DiffSbox.png">
</p>

In differential attack, T is the set of tuples of the form (x, x*, y, y*) and x’=x $\\oplus$ x* is fixed. A  certain filtering operation has been applied. Tuples (x, x*, y, y*) for which the differential holds are often called right pairs and it is the right pairs that allow us to determine the relevant key bits. It follows that a right pair must have y1=y1* and y3=y3* where yi’s are sub-block of ciphertext y. After filtering operation, each possible candidate subkey has been tested and incremented an appropriate counter if a certain xor is observed. The step include computing an xor with candidate subkeys and applying inverse S-box, followed by computation of the relevant xor-value. This attack aims to reach some bits of the subkey in the last round that is K5,5,…,K5,8 ,K5,13,…,K5,16 .When the input pairs are increased, the probability of reaching the correct result increases.

<p align="center">
  <img src="https://raw.githubusercontent.com/sumeyyekucukdemir/cryptanalysis/main/img/Pseudocode.png">
</p>
