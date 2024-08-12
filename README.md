
![RWV-Banner-Github](https://github.com/user-attachments/assets/0d60b3ff-bec3-4cbe-882f-1049f92426b1)

# Reputation-based Weighted Voting (RWV)

_RWV is a project by Token Engineering Academy Applied Research (akrtws, Eightarmsninebrainsm and Vitor Marthendal), originating from an educational program at TE Academy. It provides everything you need to roll out votings in your community, where knowledge and achievement counts: vote weighting mechanisms, a simulator, and Snapshot Strategies to be used off the shelf. If you find a bug, feel free to report. If you do a PR where tests pass, we'll be happy to merge it. And feel free to fork this repo and change it as you wish. If you need support in building a customized voting design for your community, reach out to us via Email (address)._


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

## 🧩 Understand the Components of Reputation-based Weighted Voting

### Voting Wallets carrying Reputation
- in a voting, voters express their preferences. In on-chain votings however, consider your voters as wallets. There might be individuals behind it, or organisations controlling a multi-sig. 
- they are holding tokens of reputation
- - examples include transferable, tradeable ERC-20 tokens, that are locked and staked (reputation represents skin in the game, a hodling attitude)
- - unique ERC-721 tokens, minted for a certain, unique achievement
- - ERC-1155 tokens, that represent classes of achievements, and wallets holding instances of these achievements.

All voting mechanisms in Reputation-based Weighted Voting Toolbox are made for ERC-1155 tokens. Since optimized for Snapshot votings, RWV processes tokens based on one token smart contract that you define when setting up the Snapshot strategy (see below). However, they can be adapted to ERC-20/-721 cases. Technically, any of these token types is supported by Snapshot stategies. 

Examples for reputation proofs:
- Eigentrust by Karma3Labs
- Passport by Gitcoin
- Optimist NFT
- create own graph with closest connections to badgeholder community a set of around 5000 addresses that have the closest social connection to the badgeholder community
https://gov.optimism.io/t/retro-funding-4-impact-metrics-a-collective-experiment/8226/7

### Weighting Mechanism
The Weighting Mechanism assigns a voting weight to these tokens. Before the vote is sent to the ballot, a vote assigns certain voting power to it. Our toolbox currently includes
1. Dynamic Network-Scaling 
2. Bonded Voting Weight (currently work in progress)

#### 1. Dynamic Network-Scaling
Weighted Voting based on Dynamic Network-Scaling is made for cases where the aggregated weight of certain stakeholder groups in a community should be balanced. We assume that tokens identify belonging to a certain stakeholder group. Note that since wallets can hold multiple token_Ids under the same smart contract, the wallets and individuals behind it can belong to multiple stakeholder groups.
Let's take TE Academy's case: here, we have students, graduates (those who completed a learning program successfully) and experts (course lecturers). The ERC-1155 tokens in this system certify achievements in learning or providing courses. A _course author NFT_ belongs to the expert stakeholder group. A _enrolled in course A_ NFT belongs to the student stakeholder group. Our algorithm processes the following parameters: the aggregated voting power of the stakeholder groups, and their target weight (balancing). As output, it assigns a voting weight to every token_id in the system.
Read more below (see Find your optimal parameter setting TODO)
With the Dynamic Network-Scalling mechanism, we can now balance the total voting power these stakeholder groups can achieve collectively. Additinally, this voting power is a function of the total voting power in the system, so that the voting weight of the reputation tokens dynamically updates to the current state of the ecosystem.

#### 2. Bonded Voting Weight (currently work in progress)
Description Voting Mechanisms (TODO: make this a campaign with the community: discussio - what should be the next mechanism we build?)

### The Ballot
The voting ballot is where votes are casted. In crypto cases, it's the frontend to cast your vote. It presents the voting options, and needs ballot design. The way the voting options are structured, and how votes are conducted [have a huge influence on the voting outcome](https://electionlab.mit.edu/research/ballot-design). In Snapshot votings, the ballot design is quite straightforward: you define one or several voting options for your community, and voters can choose one or several options in the Snapshot frontend.

### Voting Rule
The voting rule defines how votes are aggregated, sometimes also called aggregation rule. Again, the aggregation rule has a huge impact on the voting outcome. It starts if one or several winners should be chosen. The voting rule defines if and how a prize/reward is shared between winners. It also defines if all votes have an impact on the outcome, or if some are lost, e.g. because a minimum quorum was not met.
For Reputation-based Weighted Voting in Snapshot you can choose from many options. However, we recommend to use (TODO: make a statement what to choose)
a) in case you are looking for a single winner: Single-Winner Plurality
b) in case you are looking for a many winners: Ranked Choice (or Quadratic Voting?)

### Voting Outcome
All components mentioned above, the reputation tokens, weighting mechanim, ballot design, and voting rule are processed to find a voting outcome. Note that Snapshot allows for two routes, secret and open voting. In open voting, the pre-liminary voting outcome during the voting period is shown to voters. In secret voting (enabled by Shutter), the voting is only visible once the voting closes. There are many reasons to select one or the other routes, in many democratic votings votes are secret to avoid group think and vote manipulation.

---
### Setting up the Snapshot strategy
- Provide the smart contract address of your reputation tokens
- Select your Vote Weighting Mechanism/Snapshot Strategy:
  - - Dynamic Network-Scaling
  - - Bonded Voting Weight
- Define your parameter setting (see below)
- Set up the ballot
- Define the voting open/closing data and final settings
- Run the voting!
- This tutorial walks you through the process (TODO)

### Vote Weighting Mechanisms Specification
* Dynamic Network-Scaling (Introduction / Use Case / Math Specification)
* Bonded Voting Weight (Introduction / Use Case / Math Specification)
* Definitions (terminology)

_
## Using this framework [outdated]
To apply Reputation-based Weighted Voting, take the following steps
* Understand the Components and Design Space (see below)
* Define proofs of reputation in your community
* Select the Weighting Mechanism for your Voting Case
* Set up the Simulator (including Prerequisites, Installation, Testing/Debugging)
* Customize and verify your Vote Weighting Mechanism
* Set up your voting in Snapshot
* Run your voting
_

### Ressources
* Live Track 4 Video
  
