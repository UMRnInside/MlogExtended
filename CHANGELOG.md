# Changelog since v0.0.4

## v0.1.5
 * ProceduralCompiler: support `do-dowhile`
 * BasicCompiler: add `compile_with_mappings`
 * General: report correct line number when "No such mlogex tag" error occurs.

## v0.1.4
 * `unit-control`: add `out` prefix to output variables
 * `xlet`: support `lookup`

## v0.1.3
 * ProceduralCompiler: faster `if` and `while`

## v0.1.2
 * `xlet`: fix typo in `lessThanEq` and `greaterThanEq`

## v0.1.1
 * ProceduralCompiler: fix `if` condition skipping the second block

## v0.1.0:
 * Add ProceduralCompiler
 * ProceduralCompiler: support `if-elif-else-endif`
 * ProceduralCompiler: support `while-wend`

## v0.0.9
 * BasicDecompiler: fix unary operation not decompiling correctly

## v0.0.8
 * BasicDecompiler: fix jump conversion failure

## v0.0.7
 * Support decompilation

## v0.0.6
 * `xlet` instruction support operators like `+=`, `*=`, etc.

## v0.0.5
 * Add `xdraw` instruction
 * Not overwriting output file when compilation failed

## v0.0.4
 * `xlet` instruction support `=getlink`
 * Add `__unsafe_call` and `__unsafe_return`
 * Add compile-time macro `__TAG_COUNTER()`
