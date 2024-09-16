# Overview of Mechanisms 
by: Octopus 

Researcher, Eight Arms Nine Brains

## Introduction

During the Fellowship vote associated with the TokenEngineering Academy Study Season, it was important that those with more Token Engineering expertise have more of a say in the final outcome. To achieve this, TokenEngineering Academy and Eight Arms Nine Brains worked together to guide a combined course and research group on voting mechanisms, which ultimately led to the development of a new voting mechanism, Dynamic Network Weight Scaling. This mechanism design was implemented in Snapshot by Vitor Marthendal and used for the Fellowship vote, after extensive testing and simulation to ensure that it could successfully achieve TEA's most important requirements.

In further research after the Fellowship vote, TE Academy and Eight Arms Nine Brains have extended the core ideas of Dynamic Network Scaling in two directions: *Proportional Dynamic Network Weight Scaling* and *Ordered Dynamic Network Weight Scaling*. This document lays out the key ideas and technical aspects of both mechanisms, so communities can make an informed choice of whether and how to utilize these ideas. An example Snapshot implementation by Vitor Marthendal is forthcoming. 

## Acknowledgments 

**TODO:** Thank whoever needs to be thanked, especially the students, especially acknowledge Joan and her work on GroupHug for inspiring the idea of weighting by group. 

## Overview

In general, using Dynamic Network Weight Scaling to set voting weights for a decision works as follows:

### Set-up for Process
1. Accounts have various combinations of credentials (e.g. NFTs)
2. These credentials are divided into groups
3. Someone establishes the desired properties for these groups' weights (which we call *cweights*), as well as initial starting weights for each credential.

### Mechanics of Process
The process for re-weighting to achieve desired properties works like this.

Based on the Set-up, we have the following information:
1. Create an ordered list of groups.
2.a. For each group, specify the credentials that should be used when calculating that group's `cweight`.
2.b. In addition, for each group, specify the credentials that should be re-weighted to achieve this group's target cweight.
3. Beginning with the first group in the list, calculate what the cweight would need to be so the desired properties are acehived. Calculate the current cweight based on relevant credentials, then re-weight certain credentials to achieve this property. 

## Example Use Case

CrayonDAO (**TODO:** double-check to make sure that no one is using this) wishes to have influence for decisions assigned according to knowledge and community engagement. The DAO plans to offer six types of color-coded NFTs: <span style="color:red">red_1</span>, <span style="color:red">red_2</span>, <span style="color:blue">blue_1</span>, <span style="color:blue">blue_2</span>, <span style="color:yellow">yellow_1</span>, and <span style="color:yellow">yellow_2</span>.

There is general consensus that the `red` NFTs are the hardest to obtain, and that having a red NFT should correspond to greater voting influence. While the `blue` and `yellow` NFTs are more common, they are still valuable -- especially if someone has achieved **all** of them. 

The designers at CrayonDAO decide to group the available NFTs in three groups:
* `red`: consisting of `red1` and `red2`
* `green`: consisting of the `blue` and `yellow` NFTs, for accounts that hold all four of them. 
* `other`: consisting of `blue` and `yellow` NFTs, for accounts that do not hold all four of them. 

It's worth noting a few things:
1.  these groupings are primarily about the credentials (NFTs), rather than properties of accounts. 
2. it's possible for an account to hold NFTs which fall in more than one group. 
3. every NFT should be counted exactly once in each group. 

### Creating a New Credential

Let's look at how we would process the information in **TODO:** Example Use Case. 

The initial voter data will be in tabular format, with:
* rows corresponding to accounts,
* columns corresponding to credentials, 
* each entry indicating whether that account holds that particular credential. 

In other words, we would expect account-credential data to look something like this:

<table>
  <tr>
    <th>Account</th>
    <th>red_1</th>
    <th>red_2</th>
    <th>blue_1</th>
    <th>blue_2</th>
    <th>yellow_1</th>
    <th>yellow_2</th>
  </tr>
  <tr>
    <td>1</td>
    <td>1</td>
    <td>1</td>
    <td>0</td>
    <td>0</td>
    <td>0</td>
    <td>0</td>
  </tr>
  <tr>
    <td>2</td>
    <td>0</td>
    <td>1</td>
    <td>1</td>
    <td>1</td>
    <td>1</td>
    <td>1</td>
  </tr>
  <tr>
    <td>3</td>
    <td>1</td>
    <td>0</td>
    <td>1</td>
    <td>1</td>
    <td>1</td>
    <td>1</td>
  </tr>
  <tr>
    <td>4</td>
    <td>0</td>
    <td>0</td>
    <td>1</td>
    <td>1</td>
    <td>1</td>
    <td>1</td>
  </tr>
  <tr>
    <td>5</td>
    <td>1</td>
    <td>1</td>
    <td>0</td>
    <td>1</td>
    <td>0</td>
    <td>0</td>
  </tr>
  <tr>
    <td>6</td>
    <td>1</td>
    <td>1</td>
    <td>0</td>
    <td>1</td>
    <td>0</td>
    <td>0</td>
  </tr>
  <tr>
    <td>7</td>
    <td>0</td>
    <td>0</td>
    <td>0</td>
    <td>1</td>
    <td>0</td>
    <td>1</td>
  </tr>
  <tr>
    <td>8</td>
    <td>1</td>
    <td>0</td>
    <td>0</td>
    <td>0</td>
    <td>0</td>
    <td>1</td>
  </tr>
  <tr>
    <td>9</td>
    <td>0</td>
    <td>0</td>
    <td>0</td>
    <td>1</td>
    <td>1</td>
    <td>0</td>
  </tr>
  <tr>
    <td>10</td>
    <td>0</td>
    <td>0</td>
    <td>1</td>
    <td>0</td>
    <td>0</td>
    <td>1</td>
  </tr>
</table>

For understanding how voting weight information is processed, it's helpful to color-code each entry by which credential group it belongs to. 

<table>
  <tr>
    <th>Account</th>
    <th>red_1</th>
    <th>red_2</th>
    <th>blue_1</th>
    <th>blue_2</th>
    <th>yellow_1</th>
    <th>yellow_2</th>
  </tr>
  <tr>
    <td>1</td>
    <td class="red">1</td>
    <td class="red">1</td>
    <td class="gray">0</td>
    <td class="gray">0</td>
    <td class="gray">0</td>
    <td class="gray">0</td>
  </tr>
  <tr>
    <td>2</td>
    <td class="red">0</td>
    <td class="red">1</td>
    <td class="green">1</td>
    <td class="green">1</td>
    <td class="green">1</td>
    <td class="green">1</td>
  </tr>
  <tr>
    <td>3</td>
    <td class="red">1</td>
    <td class="red">0</td>
    <td class="green">1</td>
    <td class="green">1</td>
    <td class="green">1</td>
    <td class="green">1</td>
  </tr>
  <tr>
    <td>4</td>
    <td class="red">0</td>
    <td class="red">0</td>
    <td class="green">1</td>
    <td class="green">1</td>
    <td class="green">1</td>
    <td class="green">1</td>
  </tr>
  <tr>
    <td>5</td>
    <td class="red">1</td>
    <td class="red">1</td>
    <td class="gray">0</td>
    <td class="gray">1</td>
    <td class="gray">0</td>
    <td class="gray">0</td>
  </tr>
  <tr>
    <td>6</td>
    <td class="red">1</td>
    <td class="red">1</td>
    <td class="gray">0</td>
    <td class="gray">1</td>
    <td class="gray">0</td>
    <td class="gray">0</td>
  </tr>
  <tr>
    <td>7</td>
    <td class="red">0</td>
    <td class="red">0</td>
    <td class="gray">0</td>
    <td class="gray">1</td>
    <td class="gray">0</td>
    <td class="gray">1</td>
  </tr>
  <tr>
    <td>8</td>
    <td class="red">1</td>
    <td class="red">0</td>
    <td class="gray">0</td>
    <td class="gray">0</td>
    <td class="gray">0</td>
    <td class="gray">1</td>
  </tr>
  <tr>
    <td>9</td>
    <td class="red">0</td>
    <td class="red">0</td>
    <td class="gray">0</td>
    <td class="gray">1</td>
    <td class="gray">1</td>
    <td class="gray">0</td>
  </tr>
  <tr>
    <td>10</td>
    <td class="red">0</td>
    <td class="red">0</td>
    <td class="gray">1</td>
    <td class="gray">0</td>
    <td class="gray">0</td>
    <td class="gray">1</td>
  </tr>
</table>
<style>
  .red {background-color: #FF0000;}
  .green {background-color: #008000;}
  .gray {background-color: #808080;}
</style>

If we used this setup to try to re-weight the `blue` and `yellow` NFTs, we run into an issue: setting them based on the `other` group will essentailly set the cweight of the `green` group, which may make it impossible to achieve the desired relationship. 

The solution is to use an **indicator** which creates an additional credential. In this case, we add a new `green` column that indicates whether an account holds all `blue` and `yellow` credentials. 

<table>
  <tr>
    <th>Account</th>
    <th>red_1</th>
    <th>red_2</th>
    <th>blue_1</th>
    <th>blue_2</th>
    <th>yellow_1</th>
    <th>yellow_2</th>
    <th>green</th>
  </tr>
  <tr>
    <td>1</td>
    <td class="red">1</td>
    <td class="red">1</td>
    <td class="gray">0</td>
    <td class="gray">0</td>
    <td class="gray">0</td>
    <td class="gray">0</td>
    <td class="green">0</td>
  </tr>
  <tr>
    <td>2</td>
    <td class="red">0</td>
    <td class="red">1</td>
    <td class="green">1</td>
    <td class="green">1</td>
    <td class="green">1</td>
    <td class="green">1</td>
    <td class="green">1</td>
  </tr>
  <tr>
    <td>3</td>
    <td class="red">1</td>
    <td class="red">0</td>
    <td class="green">1</td>
    <td class="green">1</td>
    <td class="green">1</td>
    <td class="green">1</td>
    <td class="green">1</td>
  </tr>
  <tr>
    <td>4</td>
    <td class="red">0</td>
    <td class="red">0</td>
    <td class="green">1</td>
    <td class="green">1</td>
    <td class="green">1</td>
    <td class="green">1</td>
    <td class="green">1</td>
  </tr>
  <tr>
    <td>5</td>
    <td class="red">1</td>
    <td class="red">1</td>
    <td class="gray">0</td>
    <td class="gray">1</td>
    <td class="gray">0</td>
    <td class="gray">0</td>
    <td class="green">0</td>
  </tr>
  <tr>
    <td>6</td>
    <td class="red">1</td>
    <td class="red">1</td>
    <td class="gray">0</td>
    <td class="gray">1</td>
    <td class="gray">0</td>
    <td class="gray">0</td>
    <td class="green">0</td>
  </tr>
  <tr>
    <td>7</td>
    <td class="red">0</td>
    <td class="red">0</td>
    <td class="gray">0</td>
    <td class="gray">1</td>
    <td class="gray">0</td>
    <td class="gray">1</td>
    <td class="green">0</td>
  </tr>
  <tr>
    <td>8</td>
    <td class="red">1</td>
    <td class="red">0</td>
    <td class="gray">0</td>
    <td class="gray">0</td>
    <td class="gray">0</td>
    <td class="gray">1</td>
    <td class="green">0</td>
  </tr>
  <tr>
    <td>9</td>
    <td class="red">0</td>
    <td class="red">0</td>
    <td class="gray">0</td>
    <td class="gray">1</td>
    <td class="gray">1</td>
    <td class="gray">0</td>
    <td class="green">0</td>
  </tr>
  <tr>
    <td>10</td>
    <td class="red">0</td>
    <td class="red">0</td>
    <td class="gray">1</td>
    <td class="gray">0</td>
    <td class="gray">0</td>
    <td class="gray">1</td>
    <td class="green">0</td>
  </tr>
</table>
<style>
  .red {background-color: #FF0000;}
  .green {background-color: #008000;}
  .gray {background-color: #808080;}
</style>

This additional information makes the calculating and re-weighting processes much easier. Let's turn our attention to the mechanism of how this re-weighting works. 

### Proportional Dynamic Network Weight Scaling

In **Proportional Dynamic Network Weight Scaling**, the user speciifes:
1. The group rules for NFTs: precise logic around how NFTs should be summed to calculate their *cweight*. 
2. The proportions that each NFT grouping should have, in terms of total cweight, once the process is complete.
3. The initial weights for each NFT. 

The algorithm will go in order from smallest cweight proportion to largest, setting the eligible rules to achieve the correct proportion. 

As an example, let's suppose that the user gives the following input logic:
1. The three credential groups are `red`, `green`, and `other`. 
2. * To calculate the cweight of `green`, add up the weighted `red_1` and `red_2` entries for all accounts. 
* The `red_1` and `red_2` credentials should be re-weighted to make `red` have the right proprtion. 
* To calculate the cweight of `green`, add up the `green`, `blue_1`, `blue_2`, `yellow_1`, and `yellow_2` entries for the accounts that hold a `green` credential. 
* Only the `green` credential will be re-weighted for the `green` group. 
* To calculate the cweight of `other`, add up the `green`, `blue_1`, `blue_2`, `yellow_1`, and `yellow_2` entries for the accounts that do not hold a `green` credential. 


Here's how it actually works, step-by-step: 
**Step 0:** The user sets initial data: 
* **Desired cweight Proportions:** `red`: 0.5, `green`: 0.3, `other`: 0.2. 
* **Initial Weights:** `red_1`: 5.0, `red_2`: 4.0, `blue_1`: 2.0, `blue_2`: 2.0, `yellow_1`: 2.0, `yellow_2`: 1.0. 
**Step 1:** For the `other` group, everything will stay as-is: there is no need to re-weight. We calculate the `other_cweight` as **TODO: calculate the cweight**. 

**Step 2:** 
* For the `green` group, we calculate the `initial_cweight` using the `yellow_1`, `yellow_2`, `blue_1` and `blue_2` credentials. 
* We do not re-set the weights of any `yellow` or `blue` credentials, since they have already been set. 
* We re-weight only the `green` credential, so that the final cweight of the `green` credential group is exactly 1.5 times that of `other`. (1.5 = 0.3/0.2)

**Step 3:** 
* For the `red` group, we calculate the `initial_cweight` using the initial weights of `red_1` and `red_2`. 
* We re-weight the `red_1` and `red_2` credentials, so that the final cweight of the `red` credential group is exactly 2.5 times that of other. (2.5 = 0.5/0.2) 

After this process has completed, the final weights are set. The user can then test using their desired metrics, to see if the weights produce acceptable properties. If not, they can re-set the initial weights and start over. (This generate-test-and-reset process could also be automated.)


### Ordered Dynamical-Network Scaling

**TODO:** Explain this mechanism.  

 

