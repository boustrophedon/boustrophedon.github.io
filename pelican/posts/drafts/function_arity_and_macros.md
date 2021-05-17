zero arity functions are powerful

context: thinking about photoshop macros or drawing program undo-redo logs

how would you make it so that you can copy an arbitrary sublist of the action log and run it as a macro?

if they all have zero arity, then you can always run them - they might error with "no current selected region", but you can at least run them.

that is, instead of having `deleteRegion(region)`, your UI-exposed functions are always of the form `deleteCurrentlySelectedRegion()` which may of course internally be just `{currentregion = getCurrentRegion; deleteRegion(currentregion);}`

this may also be useful for the UI server concept - all ui-exposed functions could be zero arity.

issues: need to store/record state separately for playback so state still has to be reified.

further concepts: is the usefulness here due to some kind of composition law? 0 arity functions commute wrt composition?
