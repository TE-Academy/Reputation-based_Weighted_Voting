
![RWV-Banner-Github](https://github.com/user-attachments/assets/0d60b3ff-bec3-4cbe-882f-1049f92426b1)

# Reputation-based Weighted Voting (RWV)

_RWV is a project by Token Engineering Academy Research (akrtws, Eightarmsninebrainsm and Vitor Marthendal), originating from an educational program at TE Academy. It provides everything you need to roll out votings in your community, where knowledge and achievement counts: vote weighting mechanisms, a simulator, and Snapshot Strategies to be used off the shelf. If you find a bug, feel free to report. If you do a PR where tests pass, we'll be happy to merge it. And feel free to fork this repo and change it as you wish._


### Introduction
The design space of token-based governance is enormous. However, in the reality of DAO governance, only a handful of primitives have achieved significant adoption. 1token1vote links voting power directly to the number of tokens held. Vote delegation allows token holders to assign their voting rights to another party, enabling concentrated decision-making power based on trust. Reputation-based Weighted Voting (RWV) aims to complement these concepts with a third class of voting mechanism: make a voter’s track record count in decision-making and use proofs of expertise and achievements as a signal to define the voting weight and decision-making power.

This RWV Toolbox enables communities, governance researchers, and DAO participants to roll out reputation-based weighted voting in their community.

Use the RWV Toolbox, to...
* Integrate on-chain proofs to define voting power (ERC-20/ERC-721/ERC-1155)
* Select vote weighting mechanisms and customize parameters to make the vote weighting fit to your community
* Run ready-to-use simulations to test your parameter setting (dictatorship-proof, sybil resistance)
* Role out a RWV on Snapshot using the RWV Snapshot Strategies and your parameter setting 

### Table of Contents
(links to sections below)

---
![01_RWV_votingcomponents](https://github.com/user-attachments/assets/a76b5d9c-2e7b-4d2f-915b-c034e3ca371c)

## Understand the Components of Reputation-based Weighted Voting

### Voting Wallets carrying Reputation
- in a voting, voters express their preferences. In on-chain votings however, consider your voters as wallets. There might be individuals behind it, or organisations controlling a multi-sig. 
- they are holding tokens of reputation
- - examples include transferable, tradeable ERC-20 tokens, that are locked and staked (reputation represents skin in the game, a hodling attitude)
- - unique ERC-721 tokens, minted for a certain, unique achievement
- - ERC-1155 tokens, that represent classes of achievements, and wallets holding instances of these achievements.

All voting mechanisms in Reputation-based Weighted Voting Toolbox are made for ERC-1155 tokens. Since optimized for Snapshot votings, RWV processes tokens based on one token smart contract that you define when setting up the Snapshot strategy (see below). However, they can be adapted to ERC-20/-721 cases. Technically, any of these token types is supported by Snapshot stategies. 


### Weighting Mechanism
The Weighting Mechanism assigns a voting weight to these tokens. 



### Using this framework [write a brief paragraph on every step]
To apply Reputation-based Weighted Voting, take the following steps
* Understand the Components and Design Space (see below)
* Define proofs of reputation in your community
* Select the Weighting Mechanism for your Voting Case
* Set up the Simulator (including Prerequisites, Installation, Testing/Debugging)
* Customize and verify your Vote Weighting Mechanism
* Set up your voting in Snapshot
* Run your voting

### Understand the components [add diagram]
* Ballot (Voter Input)
* Vote Weighting Mechanisms
* Aggregation Rule
* Vote Outcome (Voter Output)
* Why simulations?

---

### Setting up the Snapshot strategy
- Define the Reputation tokens you'd like to process in your voting, provide the smart contract address
- Select your Snapshot Strategy:
  - - Dynamic Network-Scaling
  - - Bonded Voting Weight
- Define your parameter setting (see below)
- Define the ballot
- Define the voting open/closing data and final settings
- Run the voting!
- This tutorial walks you through the process (TODO)

### Vote Weighting Mechanisms
* Dynamic Network-Scaling (Introduction / Use Case / Math Specification)
* Bonded Voting Weight (Introduction / Use Case / Math Specification)
* Definitions (terminology)

### Ressources
* Live Track 4 Video
  
