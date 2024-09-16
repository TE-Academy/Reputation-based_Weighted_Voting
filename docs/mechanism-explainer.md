# Overview of Mechanisms 
by: Octopus
Researcher, Eight Arms Nine Brains

## Introduction

During the Fellowship vote associated with the TokenEngineering Academy Study Season, it was important that those with more Token Engineering expertise have more of a say in the final outcome. To achieve this, TokenEngineering Academy and Eight Arms Nine Brains worked together to guide a combined course and research group on voting mechanisms, which ultimately led to the development of a new voting mechanism, Dynamic Network Weight Scaling. This mechanism design was implemented in Snapshot by Vitor Marthendal and used for the Fellowship vote, after extensive testing and simulation to ensure that it could successfully achieve TEA's most important requirements.

In further research after the Fellowship vote, TE Academy and Eight Arms Nine Brains have extended the core ideas of Dynamic Network Scaling in two directions: *Proportional Dynamic Network Weight Scaling* and *Ordered Dynamic Network Weight Scaling*. This document lays out the key ideas and technical aspects of both mechanisms, so communities can make an informed choice of whether and how to utilize these ideas. An example Snapshot implementation by Vitor Marthendal is forthcoming. 

## Acknowledgments 

**TODO:** Thank whoever needs to be thanked, especially the students, especially acknowledge Joan and her work on GroupHug for inspiring the idea of weighting by group. 

## Example Use Case

CrayonDAO (**TODO:** double-check to make sure that no one is using this) wishes to have influence for decisions assigned according to knowledge and community engagement. The DAO plans to offer six types of color-coded NFTs: <span style="color:red">red_1</span>, <span style="color:red">red_2</span>, <span style="color:blue">blue_1</span>, <span style="color:blue">blue_2</span>, <span style="color:yellow">yellow_1</span>, and <span style="color:yellow">yellow_2</span>.

There is general consensus that the `red` NFTs are the hardest to obtain, and that having a red NFT should correspond to greater voting influence. While the `blue` and `yellow` NFTs are more common, they are still valuable -- especially if someone has achieved **all** of them. 

The designers at CrayonDAO decide to group the available NFTs in three groups:
* `red`: consisting of `red1` and `red2`
* `green`: consisting of the `blue` and `yellow` NFTs, for accounts that hold all four of them. 
* `yellow`: consisting of `blue` and `yellow` NFTs, for accounts that do not hold all four of them. 

It's worth noting a few things:
1.  these groupings are primarily about the credentials (NFTs), rather than properties of accounts. 
2. it's possible for an account to hold NFTs which fall in more than one group. 
3. every NFT should be counted exactly once in each group. 

### Creating a New Credential

**TODO:** Write about how the green credential works.

### Proportional Dynamical-Network Scaling

**TODO:** 

### Ordered Dynamical-Network Scaling
 

