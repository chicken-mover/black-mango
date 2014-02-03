# Working with MangoEd

The MangoEd editor is extremely basic. It's main purpose is not actually to be
a pretty UI for making levels, but to allow the stored level format to be
something that isn't very human readable (but much easier to work with
code-wise).

The side-effect of that, of course, is that it allows you to play with level
concepts and layouts without having to painstakingly hand-code them beforehand.

Note that this can and will overwrite levels in the main game directory, so
proceed with caution. I highly recommend starting new git branches to do an
kind of intesive level work, and comitting early and often.

## Starting the editor

You can start the level editor like this:

```bash
$ python mangoed/run.sh somelevel
```

If 'somelevel' exists (in `blackmango/levels/somelevel`) it will be opened for
editing. If it does not exist, it will be created on save.

You will need to keep the console running the level editor open, because all
text input and output will happen in stdout, not in the GUI view.

## Controls

### Mode switching

MangoEd uses `vi`-like 'modes' to track what is being edited at any given
moment. When switching modes, a message will be printed to stdout.

There are three modes:

* `select` - The default mode. You can enter `select` mode from any other mode
  by pressing <kbd>Esc</kbd>. In this mode, clicking on a grid square will
  select the topmost object in that square and switch to the appropriate editing
  mode (`block` or `mob`). This mode is also used for switching 'rooms' (or
  'floors'). Use the key sequence <kbd>:</kbd>+*number*+<kbd>Enter</kbd> to
  switch to a room/floor of a particular number.
* `block` - Mode for placing and editing blocks. Clicking on a square will place
  the currently selected block type. (Blocks may be selected by typing
  <kbd>:</kbd>+*number*+<kbd>Enter</kbd>.) Blocks may be deleted by hovering
  over a grid square and pressing <kbd>Delete</kbd> or <kbd>Backspace</kbd>.
  Existing blocks may be edited by hovering them and pressing <kbd>E</kbd>.
  You can enter `block` mode by pressing <kbd>B</kbd>.
* `mobs` - This mode functions identically to the `block` mode, but on mobs. The
  key for entering `mobs` mode is <kbd>M</kbd>. Selecting mobs for placement
  operates in the same manner.

### Editing properties of placed objects

When an object is placed, you can edit its properties by pressing <kbd>E</kbd>.
You will then be prompted (at the console) to enter the relevant properties of
the object. The actual GUI will hang during this process (due to how Pyglet is
architected), but the program is functioning normally.

By way of example, the promps for an ordinary mob might be the following:
```
Enter facing direction (1, 2, 3, 4) for (up, right, down left) [3]:
```

A portal object might be the following:
```
Enter destination as (x, y, z) [0, 0, 0]:
```

Note that the value in square brackets indicates the default that will be used
if you press <kbd>Enter</kbd> without entering a value.