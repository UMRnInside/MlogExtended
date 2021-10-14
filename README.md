# MlogExtended
Mindustry logic with more instructions. Compiling to vanilla Mindustry logic (vanilla mlog)IS supported. NOT A MOD.

# Features
* Conditional jump to tags using `xjump` instructions.
* Extended instruction set 
* 99% compatible with vanilla Mindustry logic.
* Accurate 1:1 conversion from MlogExtended code to vanilla mlog code.
    * Except for `__unsafe_call`, it takes 2 instructions.
    * `if-elif-else-endif` and `while-wend` has more costs, too.
* Compile to vanilla Mindustry logic for in-game use.
* "Decompile" from vanilla mlog code.

# Installtion
 * Stable release: `pip install mlog_extended` or
 * `main` branch (nightly?): `pip install git+https://github.com/UMRnInside/MlogExtended`
 * [Web version](https://umrninside.github.io/mlogex-compiler-web)

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
 * Replaces vanilla `set`, `op`, `sensor` and `getlink` instructions.
 * Expression parsing is **NOT** supported.

 ```
 xlet a = b
 xlet a0 = b + c
 xlet a0 = b * c
 # '/' for floating-point numbers, and '//' for integers
 xlet a0 = b / c
 xlet a0 = b // c

 # '^' Stands for bitwise XOR
 xlet a1 = 2 ** 8
 xlet a2 min c d
 xlet a3 =max c d

 # NOTE: NO EXPRESSION PARSING
 xlet a4 =~ x
 xlet a5 =floor x
 xlet unitX =sensor @unit @x
 xlet turret =getlink 2
 # With simple += support
 xlet a += 5
 xlet a //= 2
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

## `xdraw`
 * A replacement of vanilla `draw` command
 ```
 # Clear display, using material gray color #373737
 xdraw clear r=55 g=55 b=55
 xdraw clear rgb=0x373737
 # Set stroke width
 xdraw stroke width=1
 # Set color to #FF9100
 xdraw color rgb=0xFF9100
 # Draw a line
 xdraw line x=3 y=1 x2=3 y2=80
 xdraw line x1=3 y1=1 x2=3 y2=80
 # Draw a rectangle
 xdraw rect x1=5 y1=5 height=5 width=10
 # Draw a line rectangle
 xdraw lineRect x1=15 y1=5 height=5 width=10
 # Draw a pentagon
 xdraw poly x=20 y=40 sides=5 radius=10 rotation=0
 # Draw a triangle
 xdraw triangle x1=30 y1=30 x2=20 y2=30 x3=20 y3=20
 # Draw a cyclone
 xdraw color rgb=FFFFFF
 xdraw image x=60 y=60 image=@cyclone size=40 rotation=0
 # Flush
 drawflush display1
 ```

## `__unsafe_call` and `__unsafe_return`
 * Thin wrapper of "function calls"

 ```
 xlet i = 10
 :loop
 xlet delays = 60 - 5
 :delay1s
 xlet delays = delays - 1
 jump-if delay1s delays > 0
 
 # Pass arguments
 xlet print_content = i
 xlet message_board = message1
 # Function call
 __unsafe_call AutoPrint
 xlet i = i - 1
 jump-if loop i >= 0
 end
 
 :AutoPrint
 print print_content
 printflush message_board
 # Return statement, does NOT return a value
 __unsafe_return AutoPrint
 ```

## `if-elif-else-endif`
 * Supported by procedural compiler
 * Similar restrictions to `xlet`
 * Cost: 3N+2 vanilla mlog instructions, if there are N `elif` and `else` statements.
 ```
if i == 0
    xlet sign = 0
elif i < 0
    xlet sign = -1
else
    xlet sign = 1
endif
 ```

## `while-wend` or `while-endwhile`
 * Supported by procedural compiler
 * Similar restrictions to `xlet`
 * Support `break` and `continue`
 * Cost: 3 vanilla mlog instructions, 1 at the beginning and 2 at the end
 * **NOTE**: you cannot use `else if` directly, use `elif` instead
 ```
xlet i = 0
while i < 10
    print i
    print ", "
    xlet i += 1
    if i == 6
        continue
    elif i == 8
        break
    endif
wend
printflush message1
 ```
