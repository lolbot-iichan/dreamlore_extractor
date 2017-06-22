## dreamlore_extractor.py
Simple python extractor &amp; packer for [Dreamlore](http://www.dreamloregames.com)'s VN games:

1. [Книга мертвых: Потерянные души](http://www.cdnavigator.ru/Game.aspx?id=34)

2. [Красный Космос](http://www.dreamloregames.com/cosmos/)

3. [Евгений Онегин](http://www.dreamloregames.com/onegin/)

### Usage:
`python dreamlore_extractor.py <game> <path>`, where 
  * `<game>` is one of `necro` / `cosmos` / `onegin`, 
  * `<path>` depends on what you want to pack / extract / convert.
  
>  Usage: python dreamlore_extractor.py(necro|cosmos|onegin) <path&gt;

>    extracts:

>        necro  <pak-file> with packed pak data

>        cosmos <pak-file> with packed pak data

>        cosmos <sav-file> with packed sav data

>        cosmos <scn-file> with encoded scripts/persistent data

>        onegin <cnes-file> with encoded scripts

>        onegin <pak-file> with packed pak data (+cnes converted)

>        onegin <sys0.dfn-file> with encoded persistent data

>        onegin <sys0.dfn-file> with encoded sound settings

>    packs:

>        necro  <folder> with unpacked pak data

>        cosmos <folder> with unpacked pak/sav data

>        cosmos <scene-file> with readable scripts/persistent data

>        onegin <nes-file> with readable scripts

>        onegin <sys0.persistent-file> with readable persistent data

>        onegin <sys1.persistent-file> with readable sound settings

### Книга Мёртвых:
Works with resources data of "Книга Мёртвых".
* unpack file `My.pak` to a folder `My`
 * `python dreamlore_extractor.py necro My.pak`
* pack folder `My` to a file `My.pak`
 * `python dreamlore_extractor.py necro My`

This game does not have persistent save data. Gallery shows BMP files that are phisically unpacked to a folder. Director's Cut Edition availability is not persisted and can be changed by loading a savegame.

Works with game state save data of "Книга Мёртвых".
* converts file `16 окт 2016 23-59.sav` to a human-readable file `16 окт 2016 23-59.save`
 * `python dreamlore_extractor.py necro 15 окт 2016 23-59.sav`
* converts human-readable file `16 окт 2016 23-59.save` to a file `16 окт 2016 23-59.sav` 
 * `python dreamlore_extractor.py necro 15 окт 2016 23-59.save`
 
### Красный Космос:
Works with resources data of "Красный Космос".
* unpack file `cosmos.pak` to a folder `cosmos`
 * `python dreamlore_extractor.py cosmos cosmos.pak`
* pack folder `cosmos` to a file `cosmos.pak`
 * `python dreamlore_extractor.py cosmos cosmos`

Works with game save data of "Красный Космос".
* unpack file `16 окт 2016 23-59.sav` to a folder `16 окт 2016 23-59`
 * `python dreamlore_extractor.py cosmos "16 окт 2016 23-59.sav"`
* pack folder `16 окт 2016 23-59` to a file `16 окт 2016 23-59.sav`
 * `python dreamlore_extractor.py cosmos "16 окт 2016 23-59"` 

Works with persistent state save data of "Красный Космос".
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

Works with resources data of "Евгений Онегин".
* unpack file `data0004.pak` to a folder `data0004`
 * `python dreamlore_extractor.py onegin data0004.pak`

**NOTE:** cnes-scripts are converted to human-readable nes-scripts during unpacking. See above on how to convert them back to binary format.

Creating pak-files is not supported because of `zipfile` library limitations.

**NOTE:** pak-file is just a password-protected ZIP archive. Password is "putinissatan".

Works with persistent save data and sound settings of "Евгений Онегин".
* converts file `sys0.dfn` to a human-readable file `sys0.persistent`
 * `python dreamlore_extractor.py onegin sys0.dfn`
* converts human-readable file `sys1.persistent` to a file `sys1.dfn` 
 * `python dreamlore_extractor.py onegin sys1.persistent`

**TODO:** Game state save data file format is not supported.
