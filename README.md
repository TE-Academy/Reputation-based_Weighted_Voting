
![RWV-Banner-Github](https://github.com/user-attachments/assets/0d60b3ff-bec3-4cbe-882f-1049f92426b1)

# Reputation-based Weighted Voting (RWV)

_RWV is a project by Token Engineering Academy Applied Research (akrtws, Eightarmsninebrainsm and Vitor Marthendal), originating from an educational program at TE Academy. It provides a toolbox to roll out votings in your community, where knowledge and achievement counts: vote weighting mechanisms, a simulator, and Snapshot Strategies to be used off the shelf. If you find a bug, feel free to report. If you do a PR where tests pass, we'll be happy to merge it. 

CALL TO ACTION FOR OPEN-SOURCE DEVELOPMENT (discuss if should be rolled out now)
Below you find the current proofs and mechanisms our framework supports. What other proofs should we integrate? What other mechanisms should be covered? Learn more, and submit your proposal here: https://docs.opensource.observer/blog/request-for-impact-metrics

If you need support in building a customized voting design for your community, reach out to us via Email (address)._


### Introduction
The design space of token-based governance is enormous. However, in the reality of DAO governance, only a handful of primitives have achieved significant adoption. 1token1vote links voting power directly to the number of tokens held. Vote delegation allows token holders to assign their voting rights to another party, enabling concentrated decision-making power based on trust. Reputation-based Weighted Voting (RWV) aims to complement these concepts with a third class of voting mechanism: make a voter’s track record count in decision-making and use proofs of expertise and achievements as a signal to define the voting weight and decision-making power.

This RWV Toolbox enables communities, governance researchers, and DAO participants to roll out reputation-based weighted voting in their community.

Use the RWV Toolbox, to...
* Integrate on-chain proofs to define voting power (ERC-20/ERC-721/ERC-1155)
* Select vote weighting mechanisms and customize parameters to make the vote weighting fit to your community
* Run a mechanism audit to find critical vulnerabilities (dictatorship, sybil resistance)
* Role out your voting (link to understand the components, voting rule)

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
- https://devouch.xyz/
- create own graph with closest connections to badgeholder community a set of around 5000 addresses that have the closest social connection to the badgeholder community
https://gov.optimism.io/t/retro-funding-4-impact-metrics-a-collective-experiment/8226/7

### Reputation Proofs

#### OpenRank by Karma3Labs

OpenRank offers advanced ranking and recommendation systems for social graphs using multiple algorithms, including Eigentrust. These rankings and reputations are easily accessible to any smart contract, protocol, or through [APIs](https://docs.openrank.com/openrank-sdk/publishing-rankings-with-openrank-sdk), making them ideal for both on-chain voting mechanisms (like Tally and SnapshotX) and off-chain systems (such as Snapshot).

The social graphs can be sourced from platforms like Farcaster, Lens Protocol, and various on-chain data. Reputation algorithms are fully customizable to meet the specific needs of any community. As a decentralized reputation system, OpenRank enables ranking and recommending users based on their activity and contributions, fostering a more engaged and trustworthy community.

#### Gitcoin Passport

Gitcoin Passport leverages [Verifiable Credentials](https://www.dock.io/post/verifiable-credentials) (offchain and cryptographically verified attestations) to authenticate users based on multiple "Stamps" from different authenticators, such as Google and LinkedIn (Web2), Guild and Snapshot (Web3), and onchain transactions. The sum of these stamps is aggregated into a single Passport score, which can be used to grant access to exclusive features, rewards, and voting power in the Gitcoin ecosystem. All credentials maintain user privacy but are easily verifiable offchain, making them extremely simple to integrate as proofs for communities using offchain voting mechanisms. A voting mechanism can request either a threshold of total Passport score or a specific stamp to grant voting power to the user. The passport score and stamps can be easily accessed through an [API](https://docs.passport.xyz/building-with-passport/passport-api/api-reference).

#### DeVouch

DeVouch uses [Ethereum Attestation Service](https://attest.org/) to create onchain attestations for flagging projects from Gitcoin, Giveth and Optimism Retro Funding. Users can vouch for different projects, creating a social graph between members of reputable organizations and impactful projects. A Graphql API containing the vouches is [available](https://optimism.backend.devouch.xyz/graphql). Since this project is specific to a subset of communities, it would be more interesting in a voting mechanism to use standalone vouches (EAS attestations) as a proof of reputation for each community.

#### Ethereum Attestation Service (EAS)

EAS allows to make attestations, onchain or offchain statements about anything.
![Alt text](image.png)
The attestations can be stored onchain or offchain and queried through a [graphql API](https://docs.attest.org/docs/developer-tools/api). Any kind of reputation dynamics can be built on top of this service, since any entity can make any arbitrary statement about any other entity. This is a very flexible and powerful tool for building reputation systems such as [digital identity](https://docs.attest.org/docs/idea--zone/use--case--examples/digital-identity), [voting systems](https://docs.attest.org/docs/idea--zone/use--case--examples/voting-systems), [reputation systems](https://docs.attest.org/docs/idea--zone/use--case--examples/reputation-systems) and [much more](https://docs.attest.org/docs/category/example-use-cases).

### Weighting Mechanism
The Weighting Mechanism assigns a voting weight to these tokens. Before the vote is sent to the ballot, a vote assigns certain voting power to it. Our toolbox currently includes
1. Dynamic Network-Scaling 
2. Indicator Function (a particular set of proofs to gain weight)

Formulate as constrained optimization problem, and how to approach it.

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
Note: Properties emerge based on combination of Weighting & Voting Rule! Both the Weighting Mechanisms and the Voting Rule have huge impact on the outcome, and interact/have dependencies, that's why you should always evaluate both in combination.

### Voting Outcome
All components mentioned above, the reputation tokens, weighting mechanim, ballot design, and voting rule are processed to find a voting outcome. Note that Snapshot allows for two routes, secret and open voting. In open voting, the pre-liminary voting outcome during the voting period is shown to voters. In secret voting (enabled by Shutter), the voting is only visible once the voting closes. There are many reasons to select one or the other routes, in many democratic votings votes are secret to avoid group think and vote manipulation.

---
### Setting up the Simulations, verify your parameter settings
- Nakamoto Coefficient
- see https://github.com/TE-Academy/Reputation-based_Weighted_Voting/blob/ock/issue-26/simulation-demo/notebooks/demonstration.ipynb

### Setting up a reputation-based voting
- Define your proofs of reputation
- Select your Vote Weighting Mechanism:
  - - Dynamic Network-Scaling
  - - second?
- Define your parameter setting, optimize towards your requirements (see docs link)
- Set up the ballot
- Define your aggregation rule (voting rule) 
- This tutorial walks you through the process (TODO, create video)

- Different/customized UI connected to Snapshot UI (TODO?)

### Vote Weighting Mechanisms Specification
* Dynamic Network-Scaling (Introduction / Use Case / Math Specification)
* Core feature: balancing, more is more between groups, however, more is less within a category, how to improve? Comments on reputation and zero-sum games
* Additional feature: "more-is-more" balancing, removes the negative side effect that reputation *within* a group is a zero-sum game, so that all benefit from accumulating weight in the network
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
  
