# OSM shelter/wilderness_hut summary

Total elements returned by Overpass (amenity=shelter OR tourism=wilderness_hut, ROI+NI admin areas): 2432

**Most `amenity=shelter` hits are bus-stop/picnic/gazebo shelters, not trail shelters** — OSM overloads this tag heavily. The breakdown and candidate list below filter for that; see `overpass-ireland.json` for the untouched raw response.

## By primary tag

- `amenity=shelter`: 2411
- `tourism=wilderness_hut`: 21

## `amenity=shelter` by `shelter_type`

- `public_transport`: 1127 — noise, excluded below
- `(untagged)`: 675
- `weather_shelter`: 336
- `gazebo`: 180 — noise, excluded below
- `picnic_shelter`: 41 — noise, excluded below
- `dugout`: 8
- `lean_to`: 7
- `pavilion`: 7 — noise, excluded below
- `pergola`: 7 — noise, excluded below
- `smoking`: 5 — noise, excluded below
- `bathing_shelter`: 5 — noise, excluded below
- `changing_rooms`: 3 — noise, excluded below
- `basic_hut`: 2
- `bicycle_parking`: 2 — noise, excluded below
- `wildlife_hide`: 1
- `beach_shelter`: 1
- `building`: 1
- `dugoutq`: 1
- `dugout3`: 1
- `parking`: 1 — noise, excluded below

(325 additional unnamed `weather_shelter` nodes exist with no other context — deferred until we can cross-filter by distance from a trail; not listed below.)

## Candidates worth reviewing (42)

| name | osm type/id | lat,lon | tag | operator/access |
|---|---|---|---|---|
| Altnabrocky Hut | node/3715035560 | 54.04982,-9.60852 | shelter_type=weather_shelter | National Parks |
| Bird Watching Hut | node/1759048569 | 53.21706,-7.72565 | shelter_type=wildlife_hide | - |
| Brogan Carroll Bothy | way/158451129 | 53.98934,-9.57281 | tourism=wilderness_hut | yes |
| Brushers Gap Hut | node/1650372116 | 53.03097,-6.28805 | shelter_type=weather_shelter | Mountain Meitheal |
| Bubble Dome | way/521528715 | 54.51699,-7.88181 | tourism=wilderness_hut | - |
| Bubble Dome | way/521528984 | 54.51739,-7.88129 | tourism=wilderness_hut | - |
| Bubble Dome | way/521528985 | 54.51722,-7.88146 | tourism=wilderness_hut | - |
| Bubble Dome | way/521528986 | 54.51686,-7.88362 | tourism=wilderness_hut | - |
| Bubble Dome | way/521528988 | 54.51675,-7.88332 | tourism=wilderness_hut | - |
| Bubble Dome | way/1429017113 | 54.51695,-7.88316 | tourism=wilderness_hut | - |
| Bubble Dome | way/1429017114 | 54.51681,-7.88274 | tourism=wilderness_hut | - |
| Bubble Dome | way/1429017115 | 54.51763,-7.88176 | tourism=wilderness_hut | - |
| Clay Pigeon Shelter | way/472645488 | 54.72272,-6.68041 | shelter_type=weather_shelter | - |
| Emergency Shelter | way/186012730 | 52.00180,-9.73613 | shelter_type=weather_shelter | - |
| Flood Room | way/112519266 | 54.60955,-7.87185 | shelter_type=weather_shelter | - |
| Glenabo | node/6557326088 | 52.13009,-8.29632 | tourism=wilderness_hut | - |
| Hiker Shelter | way/260643077 | 51.96607,-9.56390 | shelter_type=weather_shelter | OPW |
| Lough Aroher Hut | node/1874100475 | 54.00422,-9.62060 | shelter_type=weather_shelter | Mountain Meitheal |
| McCann's House Bothy | way/1293759191 | 53.99501,-9.53662 | tourism=wilderness_hut | yes |
| Mucklagh Hut | node/1606755282 | 52.91502,-6.40476 | shelter_type=weather_shelter | Mountain Meitheal |
| Mullacor Hut | node/1619539857 | 52.97090,-6.37415 | shelter_type=lean_to | Mountain Meitheal |
| Scout Log Cabin | node/8621481952 | 53.08081,-7.66012 | tourism=wilderness_hut | http://www.scouting.ie/, private |
| Shoddy Hut | way/1188673532 | 54.19259,-5.89368 | tourism=wilderness_hut | yes |
| Telefón | way/1125224641 | 52.53989,-7.27313 | shelter_type=weather_shelter | - |
| The Deer Stalkers Hut (bothy) | way/1206912831 | 55.01192,-8.01091 | tourism=wilderness_hut | - |
| Tram Shelter | way/233277604 | 53.36368,-6.17706 | shelter_type=weather_shelter | - |
| Trannish Island Bothy | way/692946459 | 54.20987,-7.50397 | tourism=wilderness_hut | Share Discovery Village |
| soft area shelter | way/1535803907 | 53.33083,-6.31813 | shelter_type=weather_shelter | - |
| *(unnamed)* | node/6920238411 | 52.25734,-9.73498 | shelter_type=lean_to | - |
| *(unnamed)* | node/14137822089 | 51.93760,-7.85144 | shelter_type=basic_hut | Cork County Council |
| *(unnamed)* | node/14158461513 | 54.86027,-5.80679 | shelter_type=lean_to | - |
| *(unnamed)* | node/14281511902 | 53.95341,-8.29705 | tourism=wilderness_hut | - |
| *(unnamed)* | way/908479759 | 52.32208,-9.38602 | shelter_type=lean_to | - |
| *(unnamed)* | way/908479760 | 52.32163,-9.38619 | shelter_type=lean_to | - |
| *(unnamed)* | way/908479761 | 52.32121,-9.38636 | shelter_type=lean_to | - |
| *(unnamed)* | way/908479762 | 52.32076,-9.38652 | shelter_type=lean_to | - |
| *(unnamed)* | way/1212110461 | 53.57036,-6.78534 | shelter_type=basic_hut | - |
| *(unnamed)* | way/1344813080 | 54.35939,-5.71174 | tourism=wilderness_hut | - |
| *(unnamed)* | way/1344813081 | 54.35977,-5.71190 | tourism=wilderness_hut | - |
| *(unnamed)* | way/1558646801 | 54.12178,-6.38706 | tourism=wilderness_hut | - |
| *(unnamed)* | way/1558646802 | 54.12189,-6.38710 | tourism=wilderness_hut | - |
| *(unnamed)* | way/1558646803 | 54.12198,-6.38716 | tourism=wilderness_hut | - |
