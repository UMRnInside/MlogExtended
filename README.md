# MlogExtended
Mindustry logic with more instructions. Compiling to vanilla Mindustry logic IS supported. NOT A MOD.

# Features
* Tag support
* Conditional jump to tags using `xjump` instructions
* Compile to vanilla Mindustry logic

# Installtion
 * Stable release: `pip install mlog_extended` or
 * `main` branch (nightly?): `pip install git+https://github.com/UMRnInside/MlogExtended`

# Usage
 * `python3 -m mlog_extended <input_file> <output_file>`

 See `python3 -m mlog_extended --help` for more information

## Tag
Looks like `:Tag1`, `:snake_case`, `:我能吞下玻璃而不伤身体`, etc.
 * A unicode string on a SEPARATED line, starting with colon `:`, can contain leading whitespaces before `:`
 * Points to next instruction
 * has a name. e.g. The name of `:named_tag_1` is `named_tag_1`
 * Tag name should not contain whitespaces
 * Multiple tags can point to one instruction
 ```
 set x 0
 :Tag1
 :Tag2
 op add x x 1
 :Tag3
 ```

## `xjump`
 * Similar to vanilla `jump` instruction
 * But `xjump` jump to tags
 
 ```
 set i 0
 :DoWhileLoop
 op add i i 1
 xjump DoWhileLoop lessThan i 10
 print i
 
 xjump NotTooFar lessThanEq @thisx 10000
 print ". Oops, I am too far away!"
 :NotTooFar
 printflush message1
 ```

## `jump-if`
 * Similar to `xjump` instruction
 * Use C-style operators like `==` `!=` and `===`, etc.
 
 ```
 set i 0
 :DoWhileLoop
 op add i i 1
 jump-if DoWhileLoop i <= 10
 print i
 
 jump-if NotTooFar @thisx <= 10000
 print ". Oops, I am too far away!"
 :NotTooFar
 printflush message1
 ```

## `xlet`
 * C-Sytle variable assignment, but very limited.
 * Replaces vanilla `set`, `op` and `sensor` instructions.
 * Expression parsing is **NOT** supported.

 ```
 xlet a = b
 xlet a0 = b + c
 xlet a1 = 2 ** 8
 xlet a2 min c d
 xlet a3 =max c d
 xlet a4 =~ x
 xlet a5 =floor x
 xlet unitX =sensor @unit @x
 ```

## `unit-control`
 * A replacement of vanilla `ucontrol` command.
 * Python-kwargs-style argument.
 * Support aliases
 ```
 unit-control idle
 unit-control stop
 unit-control move x=128 y=192
 unit-control approach x=128 y=192 radius=9

 unit-control boost enable=1
 unit-control boost boost=1

 unit-control pathfind
 unit-control target x=targetX y=targetY shoot=shooting

 unit-control targetp unit=enemy shoot=shooting
 unit-control targetp target=enemy shoot=shooting

 unit-control itemDrop to=core amount=1
 unit-control itemTake from=core amount=1 item=@copper
 unit-control payDrop
 unit-control payTake takeUnits=myUnit
 unit-control mine x=128 y=192

 unit-control flag value=10000
 unit-control flag flag=10000
 unit-control getBlock x=1 y=2 type=0 building=resultBuilding
 unit-control getBlock x=1 y=2 resultType=0 resultBuilding=resultBuilding

 unit-control within x=1 y=2 radius=3 result=isWithinRadius
 ```

## `unit-radar` and `xradar`
 * A replacement of vanilla `uradar`/`radar` command.
 * Python-kwargs-style argument.
 * Support aliases
 * They are similar, as `uradar` and `radar` instruction are similar
 ```
 unit-radar filter1=enemy filter2=attacker filter3=flying order=1 sort=distance output=attacker
 unit-radar target=enemy orderBy=maxHealth asc=1 output=enemy
 xradar from=turret1 filter1=enemy filter2=flying orderBy=distance asc=0 output=target
 ```

## `unit-locate`
 * A replacement of vanilla `ulocate` command
 ```
 unit-locate type=ore oreType=@coal resultX=x resultY=y resultIsFound=found
 unit-locate type=building group=core isEnemy=false outX=x outY=y found=found building=core
 # Aliases
 unit-locate find=building group=core enemy=false outX=x outY=y found=found building=core
 unit-locate type=spawn resultX=x resultY=y resultIsFound=found building=building
 unit-locate type=damaged outX=x outY=y resultIsFound=found resultBuilding=building
 ```

## `xcontrol`
 * A replacement of vanilla `control` command
 ```
 # Disable a generator
 xcontrol generator1 action=toggle status=0
 xcontrol generator1 action=enabled status=0
 # Control a cyclone (turret), using argument aliases(unit vs target)
 xcontrol cyclone1 action=shoot x=enemyX y=enemyY shoot=1
 xcontrol cyclone1 action=shoot x=enemyX y=enemyY shoot=0
 xcontrol cyclone1 action=shootp unit=enemy shoot=1
 xcontrol cyclone1 action=shootp target=enemy shoot=1
 # Config a sorter to sort different items
 xcontrol sorter1 action=configure config=@copper
 xcontrol sorter1 action=config config=@lead
 # Set illuminator's color
 xcontrol illuminator1 action=color r=255 g=153 b=0
 ```
