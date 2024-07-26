# Bonding Curve Weighting Mechanism v1
## Math Specification 

**Overall Idea:**
The weight of a particular NFT is specified by a bonding curve. As this specific NFT becomes more common, the  

**Mathematical Specification**

There is a collection of NFTs, numbered 1 through $N$.
The weight of the $k$th NFT is defined by
$$\vec{w}_k = F_k(\vec{x}),$$ where $w_k$ is the weight of NFT $k$ and the $x_k$ is the number of NFT $k$ that have been minted. 

## Example 1: All Curves the Same

As a basic example, suppose there is a system with three NFTs where the bonding curve for each is defined by 

$$w_k = F_k(\vec{x}) = \displaystyle\frac{100}{x_k}$$

for $k \in \{1,2,3\}.$$ 

The table below shows how the weight of each NFT would be assigned based on the number of NFTs.

|       | Amount | Weight |
|-------|--------|--------|
| NFT 1 | 5      | 20.0   |
| NFT 2 | 40     | 2.5    |
| NFT 3 | 100    | 1.0    |

## Example 2: Designing Curves to Achieve Specific Properties

It is possible to create individual curves with distinct properties. It is also possible to have the bonding curve depend on the amounts of different NFTs, not just the ones whose weight is being determined. 

For instance, there is a three NFT system that should have the following properties:
1. The weight of NFT 1 should always be at least 5.0.
2. The weight of NFT 3 should always be exactly four times the weight of NFT 2.

These properties could be achieved with the following set of bonding curves:

$$F_1(\vec{x}) = 105.0 - \displaystyle\frac{100.0}{x_1}$$

$$F_2(\vec{x}) = \displaystyle\frac{100.0}{x_2}$$

$$F_3(\vec{x}) = 4 \cdot \displaystyle\frac{100.0}{x_2}$$ 


## TODO: Add image of curve that could work.
## TODO: Discuss specific use cases. 




