## dreamlore_extractor.py
Simple python extractor &amp; packer for Dreamlore's VN games.

### Usage:
`python dreamlore_extractor.py <game> <path>`, where `<game>` is one of `necro` / `cosmos` / `onegin` and `<path>` depends on what you want to pack / extract / convert.

### Книга Мёртвых:
Works with resources data of "Книга Мёртвых".
* unpack file `My.pak` to a folder `My`
 * `python dreamlore_extractor.py necro My.pak`
* pack folder `My` to a file `My.pak`
 * `python dreamlore_extractor.py necro My`

This game does not have persistent save data. Gallery shows BMP files that are phisically unpacked to a folder. Director's Cut Edition availability is not persisted and can be changed by loading a savegame.

**TODO:** Game state save data file format is not supported.

### Красный Космос:
Works with resources data of "Красный Космос".
* unpack file `cosmos.pak` to a folder `cosmos`
 * `python dreamlore_extractor.py cosmos cosmos.pak`
* pack folder `cosmos` to a file `cosmos.pak`
 * `python dreamlore_extractor.py cosmos cosmos`

Works with persistent save data of "Красный Космос".
* unpack file `16 окт 2016 23-59.sav` to a folder `16 окт 2016 23-59`
 * `python dreamlore_extractor.py cosmos "16 окт 2016 23-59.sav"`
* pack folder `16 окт 2016 23-59` to a file `16 окт 2016 23-59.sav`
 * `python dreamlore_extractor.py cosmos "16 окт 2016 23-59"` 

Works with game state save data of "Красный Космос".
* converts file `triggers.scn` to a human-readable file `triggers.scn.unpack`
 * `python dreamlore_extractor.py cosmos triggers.scn`
* converts human-readable file `triggers.scn.unpack` to a file `triggers.scn` 
 * `python dreamlore_extractor.py cosmos triggers.scn.unpack`
 
### Евгений Онегин:
Works with raw scenario files of "Евгений Онегин".
* converts file `main.cnes` to a human-readable file `main.nes`
 * `python dreamlore_extractor.py onegin main.cnes`
* converts human-readable file `main.nes` to a file `main.cnes` 
 * `python dreamlore_extractor.py onegin main.nes`

**TODO:** Resorces data file format is not supported.

**TODO:** Persistent save data file format is not supported.

**TODO:** Game state save data file format is not supported.
