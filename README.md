
# Gundam TCG Deck Price Checker

A small project for helping players roughly check the price of their Gundam TCG deck against the lowest prices on TCGPlayer. This project uses product information from [tcgcsv.com](https://tcgcsv.com) to get prices.

The project retrieves the following information for each card:
Name, ProductId, Rarity, Attack Points, Hit Points, Number, Level, Cost, CardType, url, Lowest Price, Count

## Requirements

The project is written in Python 3.13.5. You need the following dependencies:

> requests
>
> pandas

You can install them using:

    python3 -m pip install requests
    python3 -m pip install pandas

## What is made so far

> Loading decks from file
>
> Storing price information locally (helps reduce the amount of requests needed to run)
>
> Updates local information if it is outdated
>
> Getting Total From Loaded Deck
>
> Export Deck Info to XLSX

## Need to work on

> UI
>
> Optimizations
>
> Other forms of searching