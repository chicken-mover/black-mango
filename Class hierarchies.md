
Below is a partial summary of the class hierarchies in the app

## Level-related objects
```text
                    BasicLevel

                    SavedLevel

                BasicLevelTriggers
                        |
              <somelevel>.LevelTriggers
```

## Gameplay, sprites and scenery
```text
                        Background


                    pyglet.sprite.BaseSprite
                            |
                        BaseSprite
                            |
                +-----------+----------+
                |                      |
         BasicMobileSprite         BaseMaterial -------------------+
                |                      |                           |
           +----+-----+           +----+----+                  BasePortal
           |          |           |         |                      |
        Player    SimpleMob       |         |               Doors -+
                      |           |         |                      |
              Chaser -+     Wall -+  VoidMaterial          Stairs -+
                      |           |                                |
              Mirror -+ Platform -+                          etc. -+
                      |           |
                etc. -+     etc. -+


            BaseMask
               |
               +- PlagueDoctor
               |
               +- MaskOfAgammemnon
               |
               +- etc.
```

## UI
```text

        pyglet.window.Window
                |
            GameWindow


                            BaseView
                                |
        +--------------+--------+--------+--------------------+
        |              |                 |                    |
    CreditsView     GameView        LoadGameView        MainMenuView
```

## App
```text

                pyglet.app.EventLoop
                        |
                  BlackMangoApp
```