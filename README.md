# Travel times across London

This package allows you to see approximate travel times across London from any given starting point. Please note that at this point postcodes are limited to central London.

Go to the directory where you want to install the script and run:

```
git clone https://github.com/wbglaeser/travel-times-london.git
```

Then to create the heatmap around a postcode simply run (the script will prompt you for necessary input). 

```
python draw_heatmap.py
```

You need to make sure that you all necessary packages installed. Otherwise you need to download them, for example using the common pip installer. For example for the package geopy type in.

```
pip install geopy
```

The following picture shows an example heatmap for a postcode in North London.

![alt text](https://raw.githubusercontent.com/wbglaeser/travel-times-london/master/example/Figure_1.png)]


