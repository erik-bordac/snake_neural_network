# SOČ
Tento program bol vytvorený k mojej práci SOČ - Vytvorenie neurónovej siete

## Požiadavky
```
pip install -r requirements.txt
```

## Ako používať
V súbore app.py vo funkcii define_parameters() treba nastaviť parametre.

```Parameter "episodes" určuje, koľko hier bude had hrať.```
```Parameter "weights_path" je cesta k natrénovanému / novému agentovi.```
```Parameter "load_weights" určuje, či chceme načítať už natrénovaného agenta.```
```Parameter "train" určuje, či chceme trénovať agenta.```
```Parameter "plot_score" určuje, či sa po skončení programu ukáže graf s výsledkami nášho agenta.```
```Parameter "show_every" určuje, ktoré epizódy sa majú zobraziť. (ak "show_every" == 5 -> každá piata epizóda sa vykreslí)```

Na spustenie programu spustite súbor app.py

### Náhlad
![alt text](https://github.com/erik-bordac/snake_neural_network/blob/main/images/snake.gif)
