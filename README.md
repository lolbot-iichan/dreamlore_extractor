# dreamlore_extractor
Simple python extractor &amp; packer for Dreamlore's games "Красный Космос" и "Книга Мёртвых"

# Compatibility:
Works with resources data of games "Красный Космос" и "Книга Мёртвых": see `cosmos.pak` examples.

Works with persistent save data of game "Красный Космос": see `triggers.scn` examples.

Works with game state save data of game "Красный Космос": see `16 окт 2016 23-59.sav` examples.

# Usage:
* unpack file `cosmos.pak` to a folder `cosmos`
 * `python dreamlore_extractor.py cosmos.pak`
 
* pack folder `cosmos` to a file `cosmos.pak`
 * `python dreamlore_extractor.py cosmos`

* unpack file `16 окт 2016 23-59.sav` to a folder `16 окт 2016 23-59`
 * `python dreamlore_extractor.py "16 окт 2016 23-59.sav"`

* pack folder `16 окт 2016 23-59` to a file `16 окт 2016 23-59.sav`
 * `python dreamlore_extractor.py "16 окт 2016 23-59"` 

* converts file `triggers.scn` to a human-readable file `triggers.scn.unpack`
 * `python dreamlore_extractor.py triggers.scn`

* converts human-readable file `triggers.scn.unpack` to a file `triggers.scn` 
 * `python dreamlore_extractor.py triggers.scn.unpack`
 
