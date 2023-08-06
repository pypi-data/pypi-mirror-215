# gmaps_locator

Under construction! Beta Version! Currently experimenting and planning!

Developed by Akbar Tolandy (c) 2023

## Examples of How To Use (Beta Version)
```python
from gmaps_locator import GetCoord

coord = GetCoord()

address = 'Jl. Jenderal Sudirman No.Kav. 60, RT.5/RW.3, Senayan, Kec. Kby. Baru, Kota Jakarta Selatan, Daerah Khusus Ibukota Jakarta 12190'
print(coord.get_latlon(address))

# example output
{'lat': '-6.2257608', 'lon': '106.804772'}
```
