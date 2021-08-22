# MlogExtended
Mindustry logic with more instructions. Compiling to vanilla Mindustry logic IS supported. NOT A MOD.

# Features
* Tag support
* Conditional jump to tags using `xjump` instructions
* Compile to vanilla Mindustry logic

# Usage
 * `mlog_extended/BasicCompiler.py`

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
