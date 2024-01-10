
init python:
    
    import random

    class MinesweeperGame:

        def __init__(self, dimx, dimy, bombs):

            if dimx > dimy:

                self.dimx = dimx

                self.dimy = dimy

            else:

                self.dimx = dimy

                self.dimy = dimx

            self.bombs = bombs

            self.table = MinesweeperTileset(self.dimx, self.dimy, bombs)

            self.dim = 1000//self.dimy

            self.colors = [u'#fff',u'#060afe',u'#388e3c',u'#d32f2f',u'#ba2fd3',u'#d38f2f',u'#2fbed3',u'#2fd38f',u'#f5e42b']


    class MinesweeperTileset:

        def __init__(self, dimx, dimy, bombs):

            self.explosion = False

            self.bombs = bombs

            self.opened = 0

            self.marked = 0

            self.tiles = []

            self.dimx = dimx

            self.dimy = dimy

            for i in range(dimy):

                self.tiles.append([])

                for j in range(dimx):

                    self.tiles[i].append(MinesweeperTile(posi = i, posj = j))

            self.pomlist = range(dimx*dimy)

            random.shuffle(self.pomlist)

            for i in range(bombs):

                ii = self.pomlist[i] // dimx
                jj = self.pomlist[i] % dimx

                self.tiles[ii][jj].bomb = True

                pomarr = self.getNeighbours(ii,jj)

                for x in pomarr:

                    x.num += 1

        def getNeighbours(self, posi, posj):

            nbrs = []

            if (posi == 0 and posj == 0):

                nbrs.append(self.tiles[posi+1][posj+1])
                nbrs.append(self.tiles[posi+1][posj])
                nbrs.append(self.tiles[posi][posj+1])

            elif (posi == 0 and posj == self.dimx - 1):

                nbrs.append(self.tiles[posi][posj-1])
                nbrs.append(self.tiles[posi+1][posj])
                nbrs.append(self.tiles[posi+1][posj-1])

            elif (posi == self.dimy - 1 and posj == 0):

                nbrs.append(self.tiles[posi-1][posj+1])
                nbrs.append(self.tiles[posi-1][posj])
                nbrs.append(self.tiles[posi][posj+1])

            elif (posi == self.dimy - 1 and posj == self.dimx - 1):

                nbrs.append(self.tiles[posi-1][posj-1])
                nbrs.append(self.tiles[posi-1][posj])
                nbrs.append(self.tiles[posi][posj-1])

            else:

                if posi == 0:

                    nbrs.append(self.tiles[posi+1][posj-1])
                    nbrs.append(self.tiles[posi+1][posj])
                    nbrs.append(self.tiles[posi+1][posj+1])
                    nbrs.append(self.tiles[posi][posj-1])
                    nbrs.append(self.tiles[posi][posj+1])

                elif posj == 0:

                    nbrs.append(self.tiles[posi-1][posj])
                    nbrs.append(self.tiles[posi+1][posj])
                    nbrs.append(self.tiles[posi-1][posj+1])
                    nbrs.append(self.tiles[posi][posj+1])
                    nbrs.append(self.tiles[posi+1][posj+1])

                elif posi == self.dimy - 1:

                    nbrs.append(self.tiles[posi-1][posj-1])
                    nbrs.append(self.tiles[posi-1][posj])
                    nbrs.append(self.tiles[posi-1][posj+1])
                    nbrs.append(self.tiles[posi][posj-1])
                    nbrs.append(self.tiles[posi][posj+1])

                elif posj == self.dimx - 1:

                    nbrs.append(self.tiles[posi-1][posj-1])
                    nbrs.append(self.tiles[posi][posj-1])
                    nbrs.append(self.tiles[posi+1][posj-1])
                    nbrs.append(self.tiles[posi-1][posj])
                    nbrs.append(self.tiles[posi+1][posj])

                else:

                    nbrs.append(self.tiles[posi-1][posj-1])
                    nbrs.append(self.tiles[posi-1][posj])
                    nbrs.append(self.tiles[posi-1][posj+1])
                    nbrs.append(self.tiles[posi][posj-1])
                    nbrs.append(self.tiles[posi][posj+1])
                    nbrs.append(self.tiles[posi+1][posj-1])
                    nbrs.append(self.tiles[posi+1][posj])
                    nbrs.append(self.tiles[posi+1][posj+1])

            return nbrs


        def open(self, posi, posj):

            self.tiles[posi][posj].opened = True

            self.opened += 1

            if self.tiles[posi][posj].bomb == True:

                self.explosion = True

            else:

                if not self.tiles[posi][posj].num:

                    pomarr = self.getNeighbours(posi,posj)

                    for x in pomarr:

                        if not x.opened:

                            self.open(posi = x.posi, posj = x.posj)


        def toggle(self, posi, posj):

            self.tiles[posi][posj].marked ^= True

            if self.tiles[posi][posj].marked:
                
                self.marked += 1

            else:

                self.marked -= 1 

        def force_open(self, posi, posj):

            nbrs = self.getNeighbours(posi,posj)

            pomnum = 0
            for x in nbrs:

                if x.marked:

                    pomnum+=1

            if pomnum == self.tiles[posi][posj].num:

                for x in nbrs:

                    if not x.opened and not x.marked:

                        self.open(posi = x.posi, posj = x.posj)

            # else:

            #     for x in nbrs:

            #         if not x.opened:

            #             x.hlight = True


            

    class MinesweeperTile:

        def __init__(self, posi, posj):

            self.posi = posi
            self.posj = posj

            self.bomb = False
            self.marked = False
            self.num = 0
            self.opened = False
            self.hlight = False


transform hlighttf():

    easeout 0.3 alpha 0.5
    easein 0.3 alpha 1.0

screen msw_screen(ms):

    modal True
    zorder 1000

    add "background.png"

    frame:

        xalign 0.99
        yalign 0.01
        fixed:

            xsize 200
            ysize 120


            vbox:
                label "Bombs:"
                hbox:
                    text str(ms.table.marked)
                    text "/"
                    text str(ms.table.bombs)
    frame:

        xalign 0.5
        yalign 0.5
    
        fixed:

            xsize ms.dim*ms.dimx
            ysize ms.dim*ms.dimy
    
            for i in range(len(ms.table.tiles)):

                for j in range(len(ms.table.tiles[i])):

                    button:

                        xsize ms.dim
                        ysize ms.dim

                        xpos j * ms.dim
                        ypos i * ms.dim

                        if not ms.table.tiles[i][j].opened:
                            
                            background u'#cc0066'
                            hover_background u'#dd0077'
                            alternate [Function(ms.table.toggle, posi = i, posj = j)]
                            action [Function(ms.table.open, posi = i, posj = j)]
                            if ms.table.tiles[i][j].marked:

                                text ('X') xalign 0.5 yalign 0.5

                            #if ms.table.tiles[i][j].hlight:

                                #at hlighttf

                                #$ ms.table.tiles[i][j].hlight = False

                        else:

                            background u'#191316'
                            alternate [Function(ms.table.force_open, posi = i, posj = j)]
                            action [Function(ms.table.force_open, posi = i, posj = j)]
                            if ms.table.tiles[i][j].bomb:

                                text ('O') xalign 0.5 yalign 0.5

                            elif ms.table.tiles[i][j].num:

                                text (str(ms.table.tiles[i][j].num)) xalign 0.5 yalign 0.5 color ms.colors[ms.table.tiles[i][j].num]


                        
                        #hovered []

    if ms.table.explosion:

        button:

            background u'#191316aa'
            xsize 1920
            ysize 1080

            action [Hide("msw_screen"),Jump("start")]

        vbox:
            xalign 0.5 
            yalign 0.5
            text "The mine exploded :((" size 50 xalign 0.5 yalign 0.5
            text "Press anywhere to play again!" xalign 0.5 yalign 0.5

    if ms.dimx*ms.dimy - ms.table.opened == ms.table.bombs:

        button:

            background u'#191316aa'
            xsize 1920
            ysize 1080

            action [Hide("msw_screen"),Jump("start")]

        vbox:
            xalign 0.5 
            yalign 0.5
            text "You found all the mines!!!" size 50 xalign 0.5 yalign 0.5
            text "Press anywhere to play again!" xalign 0.5 yalign 0.5

label start:

    $ msgame = MinesweeperGame(20,24,99)

    show screen msw_screen(ms = msgame)

    pause

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show eileen happy

    # These display lines of dialogue.

    e "You've created a new Ren'Py game."

    e "Once you add a story, pictures, and music, you can release it to the world!"

    # This ends the game.

    return
