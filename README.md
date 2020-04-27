# mtgodecklists

## Goal

Automaticaly search, gather and classify decklists from any kind of online tournaments of Magic : The Gathering (MTGO).

## Scrapping

https://magic.wizards.com/en/content/deck-lists-magic-online-products-game-info

## Classifying by Expert Rules

### Building of Expert Rules

Expert rules are fixed rules to make classification, within the Magic : The Gathering context, following process will be built as :  
DECK <deck_name>  
RULES :  
MD :  
<rules_for_md>  
SB :  
<rules_for_sb>  
- search a card in the MD : <card_name> in  
- search n exemplars card in the MD : <n> <card_name> =  
- search at least n exemplars cards in the MD : <n> <card_name> <  
- search at maximum n exemplars cards in the MD : <n> <card_name> >  
  
### Prediction of archetype
  
Number of expert rules matched is counted to choose the deck, if number of matched rules is too low, deck is "Other" instead of the archetype with the higghest score.

## Classify by Machine Learning

Maybe one day.

## API

To use that easily.

## Feedback

Please feel free to critic and comment.

## Rights

Open-source code and tool for any Magic : The Gathering player or any Python friendly people !
Please at least cite the github if you use it in public.
