import pygame, time, os, re, sys, ast, random, itertools, csv, operator

pygame.init()

pygame.mouse.set_cursor(*pygame.cursors.broken_x) #Change cursor
clock = pygame.time.Clock() #Initialise clock to control fps


BLACK      = (   0,   0,   0)
WHITE      = ( 255, 255, 255)
GREEN      = (   0, 255,   0) 
RED        = ( 255,   0,   0)
BLUE       = (   0,   0, 255)
DARKYELLOW = ( 217, 151,   9)
DARKGREY   = (  42,  42,  45)
DARKGREYPOP= (  66,  63,  74)
LIGHTGREEN = ( 140, 255, 144)
PURPLE     = ( 170,  0, 255)
DARKBLUE   = (  12,  12, 240)
BROWN      = ( 139,  69,  19)
ORANGE     = ( 240, 126,  12)
GREY       = ( 128, 128, 128)

class Moves:
    Move_Dict = {'Level 1':2, 'Level 2':2, 'Level 3':2, 'Level 4':10, 'Level 5':10, 'Level 6':10, 'Level 7':10, 'Level 8':10, 'Level 9':10, 'Level 10':10,
                 'Level 11':1, 'Level 12':10, 'Level 13':10, 'Level 14':10, 'Level 15':10, 'Random':255, 'Sandbox':255, 'Practise 1':10, 'Practise 2':10,
                 'Practise 3':10}
    
    @classmethod
    def Display(cls, GameMode, NoOfMoves):
        cls.MaxNoMoves = cls.Move_Dict.get(GameMode)
        if not cls.MaxNoMoves:
            cls.MaxNoMoves = 10 #If MaxMoves not set for particular level, default is 10
        MovesLeft = cls.MaxNoMoves - NoOfMoves
        GREEN_STRENGTH = MovesLeft/Moves.MaxNoMoves * 255
        MoveCountBackGround = pygame.draw.rect(screen, DARKGREYPOP, ((1010), (95), (180), (10)))
        MoveCountBar = pygame.draw.rect(screen, (255,GREEN_STRENGTH,0), ((1010), (95), (180), (10)))
        MoveCountDisplay_text = (X_text_font.render("Remaining Moves: {0}/{1}".format(MovesLeft,cls.MaxNoMoves),True,BLACK)) #Displays the total number of functions the user has entered
        screen.blit(MoveCountDisplay_text, [(1010), (95)])
        if MovesLeft == 0 and Message.Info != 'Welldone! All monsters have been killed! Level complete!':
            Message.Info = "You failed to complete this level, press 'any key' to view menu"

    @classmethod
    def MoveIsValid(cls, NoOfMoves, GameMode, ObjectStorage):
        Valid = True
        if NoOfMoves == cls.MaxNoMoves:
            RestartMenu.Display(GameMode, ObjectStorage)
            Valid = False
        return Valid

class Format:
    
    @staticmethod
    def GridLock(Coords): 
        Coords = (Coords[0]-(Coords[0]%30), Coords[1]-(Coords[1]%30)) #changed to 1 DP
        return Coords
    @staticmethod
    def GetWidth(Surface, Division=True): #Removes the need for TextLength = (...) then TextLength//2 sub
        Width = Surface.get_rect().width
        if Division:
            Width = Width//2
        return Width
    @staticmethod
    def GetHeight(Surface, Division=True):
        Height = Surface.get_rect().height
        if Division:
            Height = Height//2
        return Height
    
class BackGroundListenner: 
    FullScreen = False #Records whether the user is in fullscreen or not

    @classmethod
    def Listen(cls, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                cls.FullScreen = not cls.FullScreen
                if cls.FullScreen:
                    screen = pygame.display.set_mode((1200, 600), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((1200, 600)) #Can use , pygame.RESIZABLE in order to resize screen with mouse
            elif event.key == pygame.K_RCTRL:
                Music.Switch()

screen = pygame.display.set_mode((1200, 600)) #To enter fullscreen upon program execution use: screen = pygame.display.set_mode((1200, 600), pygame.FULLSCREEN)
pygame.display.set_caption("Trajectoriam")
          
#Load all image files as objects//Refer to as <DIR>.<IMAGE>
class Image:
    def __DirectoryScan(self, PATH): #Private method; do not attempt to run outside class
        File_Contents = os.listdir(PATH)
        for File in File_Contents:
            if re.search(r'.png$', File): #Apply below for each PNG file
                Attribute = 'self.' + File.replace('.png','')
                exec(Attribute + " = pygame.image.load(os.path.join('{0}', '{1}')).convert()".format(PATH, File)) #Dynamically define attributes
                
    def __init__(self, Path):
        self.Path = Path
        self.__DirectoryScan(Path)

    def ScreenShot(): #Optional function, not in code
        pygame.image.save(screen, 'Temporary.png')

Image_Directories = [x[0] for x in os.walk('Images')][1:] #Not interested in 'Images' || Notice the double // to nullify meaning of '/' to interpreter
for Path in Image_Directories:
    SubDir_Name = re.findall(r'[^\\]+$', Path)[0]
    exec(SubDir_Name + " = Image('{}')".format(Path))
    
pygame.display.set_icon(Graphics.TrajectoriamIcon) #set icon
#pre-loading fonts to be used during program
        
XXV_text_font = pygame.font.SysFont('Calibri', 25, True, False)
XX_text_font = pygame.font.SysFont('Calibri', 20, True, False)
X_text_font = pygame.font.SysFont('Calibri', 10, True, False)
XL_text_font = pygame.font.SysFont('Calibri', 40, True, False)
XLV_text_font = pygame.font.SysFont('Calibri', 45, True, False)
XLV_Gothic_text_font = pygame.font.SysFont('centurygothic', 45, True, False)



class Animation: #Cannot be called 'Animations' as we have a directory called 'Animations'
    MICHAELFRAMES = []
    for Frame in range(1,59): #Load all frames in 'MichaelGames' directory
        MICHAELFRAMES.append("MichaelGames.Frame{}".format(Frame))

    EndOffSet = None

    @classmethod
    def FlipBook(cls):
        FlipBookSound.Play()
        try:
            for Frame in cls.MICHAELFRAMES:
                screen.fill(BLACK)
                screen.blit(eval(Frame), [300, 168]) #Use eval instead of exec
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        raise BreakIt 
                clock.tick(15)
        except BreakIt:
            pass
         #must be within for loop to control frames per second
        DisplayMenu()

    @classmethod
    def _DownwardImageMotion(cls, Image_File, Division): 
        if cls.EndOffSet <= Format.GetHeight(Image_File, False)*(1-1/Division)*-1:
            cls.ResetOffSet(Image_File, Division, 'Down')
        else:
            cls.EndOffSet += (-5)
        screen.blit(Image_File, [0, cls.EndOffSet])

    @classmethod
    def _LeftwardImageMotion(cls, Image_File, Division):
        if cls.EndOffSet <= Format.GetWidth(Image_File, False)*(1-1/Division)*-1:
            cls.ResetOffSet(Image_File, Division, 'Left')
        else:
            cls.EndOffSet += (-5)
        screen.blit(Image_File, [cls.EndOffSet, 0])
        
    @classmethod
    def _UpwardImageMotion(cls, Image_File, Division):
        if cls.EndOffSet >= 0:
            cls.ResetOffSet(Image_File, Division, 'Up')
        else:
            cls.EndOffSet += (5)
        screen.blit(Image_File, [0, cls.EndOffSet])
        
    @classmethod
    def _RightwardImageMotion(cls, Image_File, Division):
        if cls.EndOffSet >= 0:
            cls.ResetOffSet(Image_File, Division, 'Right')
        else:
            cls.EndOffSet += (5)
        screen.blit(Image_File, [cls.EndOffSet, 0])

    @classmethod
    def ImageMotion(cls, Image_File, Division, Direction):
        try:
            exec('cls._'+Direction+'wardImageMotion(Image_File, Division)')
        except TypeError: #Will only ever trigger when function is first executed
            cls.ResetOffSet(Image_File, Division, Direction)
            
    @classmethod
    def ResetOffSet(cls, Image_File, Division, Direction):
        cls.EndOffSet = {'Up': -Format.GetHeight(Image_File, False)*(1-1/Division)*1,
                         'Right': -Format.GetWidth(Image_File, False)*(1-1/Division)*1, 'Down': 0, 'Left': 0}.get(Direction)


class BoxPrompt:
    Icon_Reference = ['Resume', Graphics.ResumeIcon, 'Restart', Graphics.RestartIcon, 'MainMenu', Graphics.HomeIcon,
                       'Help', Graphics.HelpIcon, 'Mute', Graphics.MuteIcon, 'UnMute', Graphics.SoundIcon, 'Back', Graphics.HomeIcon]
    def __init__(self, Title, Icons): #'Sound' should always be the last element
        self.Title = Title
        self.Sound = False
        if 'Sound' in Icons:
            self.Sound = True
        self.Help_Display = False
        for i in range(len(Icons)): #i = Icon
            if Icons[i] == 'Sound':
                Icons[i] = ['UnMute', Graphics.SoundIcon]
            else:
                Icons[i] = [Icons[i], BoxPrompt.Icon_Reference[BoxPrompt.Icon_Reference.index(Icons[i])+1]]
        self.Icons = Icons
        
    def Display(self, GameMode, ObjectStorage, Tracking='', Resurrect=False, Movement=False):
        
        BlitParameterInput, IconReference = False, []
        self.Run = True
        self.GameMode = GameMode
        self.Tracking = Tracking
        self.Resurrect = Resurrect
        self.Movement = Movement
        self.ObjectStorage = ObjectStorage #required for sandbox trials
        screenshot = screen.copy()
        screenshot.set_alpha(50)
        while self.Run:
            
            screen.fill(BLACK)
            IconBlitList = []
            screen.blit(screenshot, [0, 0])
            screen.blit(Graphics.BoxPromptButtonBackGround, [375, 225])
            Pause_text = XXV_text_font.render(self.Title,True,RED)
            screen.blit(Pause_text, [600-Format.GetWidth(Pause_text), (235)])
            
            if self.Sound:
                if Music.Sound:
                    self.Icons[-1] = ['Mute', Graphics.SoundIcon]
                else:
                    self.Icons[-1] = ['UnMute', Graphics.MuteIcon]
                    
            OffSet = 0
            for Icon in self.Icons:
                IconBlitList.append(screen.blit(Icon[1], ([395+OffSet+(45*(5-len(self.Icons))), 270])))
                OffSet += 90

            if BlitParameterInput:
                screen.blit(BlitParameterInput[0],BlitParameterInput[1])
                
            Message.Display(2)
            
            if self.Help_Display:
                if GameMode in ['Sandbox', 'Design']:
                    InstructionDisplay = screen.blit(Graphics.DevInstructions, ([390, 100]))
                else:
                    InstructionDisplay = screen.blit(Graphics.Instructions, ([390, 100]))

            pygame.display.flip()
            for event in pygame.event.get():
                BackGroundListenner.Listen(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #event.button == 1 - left mouse click
                    MouseClick = pygame.mouse.get_pos()
                    ButtonClick.Play()
                    if self.Help_Display:
                        if InstructionDisplay.collidepoint(MouseClick):
                            self.Help_Display = not self.Help_Display
                    else:
                        for i in range(len(IconBlitList)): #i = ['Graphics.SoundIcon', [x,y]]
                            if IconBlitList[i].collidepoint(MouseClick):
                              getattr(self, '_{}'.format(self.Icons[i][0]))()
                elif pygame.MOUSEMOTION:
                    if len(IconReference) == 0: #Only construct once
                        for t in range(len(IconBlitList)):
                            IconReference.append([self.Icons[t][0], tuple(IconBlitList[t])])
                    else:
                        IconReference[-1] = [self.Icons[-1][0], tuple(IconBlitList[t])]
                    BlitParameterInput = CursorOverButton(IconBlitList, IconReference)
        clock.tick(60)

    def _Resume(self):
        self.Run = False
    def _Restart(self):
        if self.GameMode != 'Design':
            if self.GameMode == 'Sandbox':
                PlayGame(self.GameMode, self.ObjectStorage, Resurrect=self.Resurrect, Movement=self.Movement)
            else:
                PlayGame(self.GameMode, Tracking=self.Tracking, Resurrect=self.Resurrect, Movement=self.Movement)
            self.Run = False
            USER.Restart = True
        else:
            Message.Info = 'Only levels can be restarted! Press "t" to play your design!'
            Message.Display(2)
    def _MainMenu(self):
        Message.LoadingScreen()
        SpritePositions.ResetImage_Alphas('G')
        if 'Level' in self.GameMode: #changed from if Total_Score
            USER.CheckScore()
            DisplayMenu()
        elif 'Practise' in self.GameMode:
            USER.Restart = True
            self.Run = False
        else:
            USER.Restart = False
            self.Run = False
            DisplayMenu() #Safe to call here
    def _UnMute(self):
        Music.Switch()
    def _Mute(self):
        Music.Switch()
    def _Help(self):
        self.Help_Display = not self.Help_Display
    def _Back(self):
        self.Run = False
        USER.Restart = True
        SpritePositions.ResetImage_Alphas('G')
        Message.LoadingScreen()
                            
PauseMenu = BoxPrompt('Game Paused', ['Resume', 'Restart', 'MainMenu', 'Help', 'Sound'])
RestartMenu = BoxPrompt('Level Failed, moves depleted', ['Resume', 'Restart', 'MainMenu', 'Sound'])
SandboxMenu = BoxPrompt('Game Paused', ['Resume', 'Restart', 'Back', 'Help', 'Sound'])

class Message:
    TextColour = WHITE #Can change text colour
    Frame = 0
    InputColour = GREEN
    Width_Pos, Height_Pos = 600, 150 
    Info = None
    Log = []

    @classmethod
    def Format(cls, Width_Pos=600, Height_Pos=150, TextColour=WHITE): #Can change formatting, by calling this subroutine
        cls.Width_Pos = Width_Pos
        cls.Height_Pos = Height_Pos
        cls.TextColour = TextColour

    @classmethod
    def Display(cls, Length_Seconds):
        if cls.Info:
            Times = 60*Length_Seconds
            cls.__Check()
            if cls.Frame != Times:
                Message_text = (XXV_text_font.render(cls.Info,True,cls.TextColour))
                Message_text = screen.blit(Message_text, [(cls.Width_Pos)-Format.GetWidth(Message_text), (cls.Height_Pos)])
                cls.Frame += 1
            elif cls.Frame == Times:
                if cls.Info == 'Welldone! All monsters have been killed! Level complete!': #User cannot change cls.Info if this is its value, within PlayGame
                    USER.Restart = True
                    cls.Format()
                    Complete.Play()
                    Message.LoadingScreen()
                cls.Reset()
            
    @classmethod
    def Reset(cls): 
        cls.Frame = 0
        cls.InputColour = GREEN
        cls.Info = None

    @classmethod
    def __Check(cls):
        cls.Log.append(cls.Info)
        if len(cls.Log) == 2:
            if cls.Log[1] != cls.Log[0]: #Reset display duration if a new message comes in
                cls.Frame = 0
            del cls.Log[0]

    @staticmethod
    def LoadingScreen(): #Can be moved into the Message class
        LoadingFrames = ["Loading", "Loading.", "Loading..", "Loading..."]
        LoadingFrameEntry = 0
        for Frame in range((len(LoadingFrames)+1)*2):
            if LoadingFrameEntry == 4:
                LoadingFrameEntry = 0
            screen.fill(BLACK)
            Loading_text = (XLV_text_font.render(LoadingFrames[LoadingFrameEntry],True,WHITE))
            screen.blit(Loading_text, [(600)-Format.GetWidth(Loading_text), (250)])
            pygame.display.flip()
            LoadingFrameEntry += 1
            clock.tick(40)
                
####To break out of 2 for loops
class BreakIt(Exception): pass

class Music: #Used for background music
    Sound = True
    def __init__(self, Track, Duration):
        self.Track = Track
        self.Duration = Duration
        if Music.Sound:
            pygame.mixer.music.load(os.path.join('Music', self.Track+'.mp3'))
            pygame.mixer.music.play(self.Duration)
            
    def ChangeTrack(self, Track): #Used when track is changed
        self.Track = Track
        pygame.mixer.music.load(os.path.join('Music', self.Track+'.mp3'))
        pygame.mixer.music.play(self.Duration)                

    def Switch(): #Alters the class variable, called when all sound is to be paused/unpaused
        Music.Sound = not Music.Sound
        if Music.Sound:
            pygame.mixer.music.unpause()
            pygame.mixer.unpause()
        else:
            pygame.mixer.music.pause()
            pygame.mixer.pause()
            
class SoundEffects: #Used for short-burst soundeffects
    def __init__(self, Track):
        self.Track = Track
        self.PlayBack = pygame.mixer.Sound(os.path.join('Music',self.Track+'.wav'))

    def Play(self):
        if Music.Sound:
            self.PlayBack.play()

Complete = SoundEffects('LevelComplete')
ButtonClick = SoundEffects('ButtonClick')
LaserEffect = SoundEffects('LaserEffect')
FlipBookSound = SoundEffects('FlipBookSound')

class USER_DATABASE:
    FilePath = os.path.join('AccountDetails', 'AccountDetails.csv')

    @classmethod
    def CreateNewUser(cls, Account):
        with open(cls.FilePath, 'a', newline='') as OpenFile:
            csv.writer(OpenFile).writerow(Account)

    @classmethod
    def ReloadData(cls): #Accounts for data written to file
        File_Contents = []
        File_Contents.extend(csv.reader(open(cls.FilePath)))
        cls.File_Contents = File_Contents
        
class USER: #As we will only ever deal with one instance from the USER class there is no point in having an __init__ method
    Total_Score = 0
    Level_Score = 0
    Username = None
    Password = None
    Row = None #So we know at where the user is held in File_Contents
    Session_Scores = 0
    Restart = False

    @classmethod
    def CheckScore(cls):
        cls.Minimum = min(cls.Session_Scores)
        if cls.Total_Score > cls.Minimum: #If the new score obtained is higher than any of the user's previous score then it will be replaced with the greater one
            cls.Session_Scores[cls.Session_Scores.index(cls.Minimum)] = cls.Total_Score #replace the minimum score with the higher score obtained
            USER_DATABASE.File_Contents[cls.Row][2:5] = cls.Session_Scores #replace old tuples with updated tuples
            writer = csv.writer(open(USER_DATABASE.FilePath, 'w', newline=''))
            writer.writerows(USER_DATABASE.File_Contents) #Write to the csv file the new data, all previous data is overwritten
        cls.Total_Score = 0

    @classmethod
    def LevelIncrement(cls, Damage_Dealt):
        cls.Level_Score += Damage_Dealt**2
        if cls.Level_Score > 9999: #Limited to 4 digits
            cls.Level_Score = 9999

class SpritePositions:
    Sprite_Collection = []
    AreaOfEffectCords = []
    Grave_Images = [Objects.G1, Objects.G2, Objects.G3, Objects.G4]
    Type_Dict = {'M': 'MONSTERS', 'R': 'ROCKS', 'G': 'GRAVESTONES'}
    Clicked = [False, False] #Contains the profile image's blit parameter
    
    @classmethod
    def Get(cls, GameMode, ObjectStorage):
        cls.Sprite_Collection = []
        if GameMode == 'Sandbox':
            cls.Read(ObjectStorage)
        elif GameMode != 'Random':
            ObjectStorage = LoadFile(GameMode,'Pre-Made')
            Message.Info = None #Void the Message output from 'LoadFile'
            cls.Read(ObjectStorage)
        else:
            #RANDOM GAME MODE - so map must be randomly generated
            Taken_Positions = [] #Used as object positioning is random therefore object may overlap another
            while len(Taken_Positions) != 25:
                Coords = cls.RandomCoords()
                if Taken_Positions.count(Coords) == 0:
                    Taken_Positions.append(Coords)

            while len(cls.Sprite_Collection) != 15:
                cls.Sprite_Collection.append(eval('MONSTERS({0}, "{1}", {2})'.format(random.randint(1,4), 'M', Taken_Positions.pop())))
            while len(cls.Sprite_Collection) != 25:
                cls.Sprite_Collection.append(eval('ROCKS({0}, "{1}", {2})'.format(1, 'R', Taken_Positions.pop())))
                cls.Sprite_Collection.append(eval('GRAVESTONES({0}, "{1}", {2})'.format(random.randint(1,4), 'G', Taken_Positions.pop())))

    @classmethod
    def Read(cls, ObjectStorage):
        cls.Sprite_Collection = []
        for Sprite in range(len(ObjectStorage)):
            Type = ObjectStorage[Sprite][1][0] #Get the first character of the Type element string
            Pos = list(ObjectStorage[Sprite][0])
            Rank = int(ObjectStorage[Sprite][1][1]) #Must convert to int
            cls.Sprite_Collection.append(eval(cls.Type_Dict.get(Type))(Rank, Type, Pos)) #Dynamically create sprite objects
            
    @classmethod
    def CheckClick(cls, Click_Point):
        cls.Clicked = [False, False]
        for s in cls.Sprite_Collection:
            if s.Surface.collidepoint(Click_Point):
                cls.Clicked[0] = s.ClickedGraphic
                cls.Clicked[1] = ([1010, 115])
                break

    @classmethod
    def Resurrect(cls, Roll=1, NoToResurrect='ALL'):
        if Roll == 1:
            NoResurrected = 0
            for s in cls.Sprite_Collection:
                if s.Type == 'G': #Make all graves flashing
                    s.Resurrect() #Set alpha values if resurrect unsuccessful, but resurrect is successful
                    if type(NoToResurrect) is int:
                        NoResurrected += 1
                        if NoResurrected == NoToResurrect:
                            break #Need not iterate through other graves once quota is reached
        else:
            cls.FlashGraves()

    @classmethod
    def FlashGraves(cls):
        try:
            if cls.Grave_Images[0].get_alpha() <= 0 or cls.Grave_Images[0].get_alpha() >= 255:
                cls.T_Increment = cls.T_Increment*-1
            for Image in cls.Grave_Images:
                Image.set_alpha(Image.get_alpha()+cls.T_Increment)
        except TypeError:
            cls.ResetImage_Alphas('G')

    @classmethod
    def ResetImage_Alphas(cls, Type):
        if Type == 'G':
            for Image in cls.Grave_Images:
                Image.set_alpha(255)
        cls.T_Increment = 1 #Can alter fade in/out rate here

    @classmethod
    def Display(cls):
        for s in cls.Sprite_Collection:
            s.Surface = screen.blit(s.Graphic, s.Position)
            
    @classmethod
    def GameOver(cls):
        GameOver = True
        for s in cls.Sprite_Collection:
            if s.Type == 'M':
                GameOver = False
                break
        return GameOver

    @classmethod
    def PointCollision(cls, Coords):
        BLOCKED = False
        for s in cls.Sprite_Collection:
            if s.Type != 'G':
                Hit, KILL = s.IsHit(Coords)
                if Hit:
                    if not s.Bypass:
                        BLOCKED = True
                        break
                    elif KILL: 
                        if s.Type == 'M':
                            Dead_Sprite_Index = cls.Sprite_Collection.index(s)
                            cls.Sprite_Collection[Dead_Sprite_Index] = GRAVESTONES(s.MaxHealth, 'G', s.Position)
                    break #Once a hit is noticed, we need not iterate through the remaining sprites so iteration is broken
        return BLOCKED


    @classmethod
    def CheckForCollision(cls, Coords):
        cls.AreaOfEffectCords.append(Coords)
        if cls.THIN_AreaOfEffectCords.count(Format.GridLock(Coords)) == 0:
            cls.THIN_AreaOfEffectCords.append(Format.GridLock(Coords))
            if cls.PointCollision(Format.GridLock(Coords)):
                raise BreakIt
                     
    @classmethod
    def SketchGraph(cls, Equation, ListToString, YorX):
        cls.AreaOfEffectCords = [] #may remove this
        cls.THIN_AreaOfEffectCords = []
        cls.DAMAGE = 0
        Equation = cls.FormEquation(Equation) #Could be a class variable so you can generate a log
        if YorX == 'y':
            #CONSIDER POSITIVE X
            try:
                for x in [x * 0.1 for x in range(5010)]:#x in range(0,501)
                    EquationString = re.sub(r'\(([^(])*\)', '({0})'.format(x),  Equation)
                    try:
                        if 0 <= eval(EquationString) <= 599: #y-values
                            Coords = [x+500, 599-eval(EquationString)]
                            cls.CheckForCollision(Coords)
                    except ZeroDivisionError:
                        pass
            except BreakIt:
                pass
            #NOW CONSIDER NEGATIVE X
            try: 
                for x in [x * 0.1 for x in range(0,-5010, -1)]:#x in range(0,-501, -1)
                    EquationString = re.sub(r'\(([^(])*\)', '({0})'.format(x),  Equation)
                    try:
                        if 0 <= eval(EquationString) <= 599:
                            Coords = [x+500, 599-eval(EquationString)]
                            cls.CheckForCollision(Coords)
                    except ZeroDivisionError:
                        pass
            except BreakIt:
                pass

        if YorX == 'x':
            #CONSIDER POSITIVE Y
            try:
                for y in [y * 0.1 for y in range(6010)]:
                    EquationString = re.sub(r'\(([^(])*\)', '({0})'.format(y),  Equation)
                    try:
                        if -500 <= eval(EquationString) <= 500:
                            Coords = [eval(EquationString)+500,599-y]
                            cls.CheckForCollision(Coords)
                    except ZeroDivisionError:
                        pass
            except BreakIt:
                pass
            
        if cls.DAMAGE: #Score creditted once all processing done
            USER.LevelIncrement(cls.DAMAGE)
            
        Message.Info = 'You have entered: '+str(ListToString)

    @classmethod
    def RandomMovement(cls, Roll=1):
        if Roll == 1:
            for s in cls.Sprite_Collection:
                if s.Type == 'M':
                    s.Move()

    @staticmethod
    def FormEquation(Equation):
        for Entry in range(len(Equation)):
            if '^' in Equation[Entry]: #Catches all unknown coefficients
                Equation[Entry] = Equation[Entry].replace('^', '**')
            if re.search(r'[xy]', Equation[Entry]):
                try:
                    if (Entry == 0) or (Equation[Entry-1] in ['+','-','/']):
                        Equation[Entry] = re.sub(r'[xy]', '()', Equation[Entry])
                    else:
                        Equation[Entry] = re.sub(r'[xy]', '*()', Equation[Entry])
                except IndexError:
                    pass
        Equation = ''.join(Equation) #Convert array to string
        return Equation
                       
    @staticmethod
    def RandomCoords(): #valid range is (1, 1) to (970, 569), I.e.: on the game screen
        #####SOMETHING HERE#####
        RANDOM_X = random.randint(1, 970)
        RANDOM_Y = random.randint(1, 569)
        RANDOM_CORDS = Format.GridLock(([RANDOM_X, RANDOM_Y])) #added gridlock functionality
        return list(RANDOM_CORDS) #Outputs a list whose elements form a valid random coordinate
            
class Sprites:
    def __init__(self, Rank, Type, InitialPosition):
        self.Rank = Rank
        self.Health = None
        self.Bypass = True
        self.Type = Type #'M', 'R', 'G'
        self.InitialPosition = InitialPosition
        self.Position = InitialPosition


    def IsHit(self, Coords):
        KILL = False
        Hit = False
        if self.Surface.collidepoint(Coords):
            Hit = True
            if self.Health:
                self.Health += -1
                SpritePositions.DAMAGE += 1
                if self.Health == 0:
                    KILL = True
                else:
                    self.HpUpdate()
        return Hit, KILL
    
    def HpUpdate(self):
        self.Graphic = getattr(Objects, '{0}{1}'.format(self.Type, self.Health))
        self.ClickedGraphic = getattr(Profiles, '{0}{1}'.format(self.Type, self.Health))

    def Reset(self): #If restart is clicked
        self.Health = self.MaxHealth
        self.Position = self.IntialPosition
        self.HpUpdate()

class MONSTERS(Sprites):
    def __init__(self, Rank, Type, InitialPosition):
        super().__init__(Rank, Type, InitialPosition)
        self.MaxHealth = Rank #Directly related to the rank of the piece
        self.Health = Rank
        self.Graphic = getattr(Objects, 'M{}'.format(self.Rank))
        self.ClickedGraphic = getattr(Profiles, 'M{}'.format(self.Rank))

    def Move(self):
        Move = random.choice([0,1])
        if Move:
            UorD = random.choice([-1,1])
            LorR = random.choice([-1,1])
            self.Position = [self.Position[0]+(30*UorD), self.Position[1]+(30*LorR)]
        
class ROCKS(Sprites):
    def __init__(self, Rank, Type, InitialPosition):
        super().__init__(Rank, Type, InitialPosition)
        self.Bypass = False
        self.Graphic = Objects.R
        self.ClickedGraphic = Profiles.R
        
class GRAVESTONES(Sprites):
    
    def __init__(self, Rank, Type, InitialPosition):
        super().__init__(Rank, Type, InitialPosition)
        self.Graphic = getattr(Objects, 'G{}'.format(self.Rank))
        self.ClickedGraphic = getattr(Profiles, 'G{}'.format(self.Rank))

    def Resurrect(self):
        Index = SpritePositions.Sprite_Collection.index(self)
        SpritePositions.Sprite_Collection[Index] = MONSTERS(self.Rank, 'M', self.Position)
            
        
def DisplayMenu():
    BackGroundFrame = [Graphics.MenuBackGround,Graphics.MenuBackGround1,Graphics.MenuBackGround2,Graphics.MenuBackGround3,Graphics.MenuBackGround4]
    BlitParameterInput = False
    NAME_DISPLAY = (XXV_text_font.render("Logged in as: %s" %USER.Username,True,ORANGE))
    Menu_Options = ['Start New Game', 'Random Level', 'Instructions', 'Practise Level', 'Developer Mode', 'View Leaderboard']
    IconReference = [['Watch credits',(Graphics.TrajectoriamLogo, [0, (540)])], ['Logout', (Graphics.LogOutIcon, [(1155),0])], ['Mute',(Graphics.SoundIcon, [0,0])]]
    while True:
        screen.fill(BLACK) #Removes all previously blitted images, reduces amount of memory allocation for program
        IconBlitList, Button_Icons = [], [] #Redefine arrays
        MainMenuFrameEntry = random.randint(0,4) #Random frames allow ellusion of 'low power'
        screen.blit(BackGroundFrame[MainMenuFrameEntry], [0, 0])
        screen.blit(Graphics.MenuMonster, [(460),(10)])
        OffSet = 300 #Constant step variable which allows images to be blitted the same distance apart, redefined at each iteration
        for Button in range(len(Menu_Options)):
            Button_Icons.append(screen.blit(Graphics.MainMenuBottonBackGround, [(390), (OffSet)]))
            Button_text = (XXV_text_font.render(Menu_Options[Button],True,DARKGREYPOP))
            screen.blit(Button_text, [(600)-Format.GetWidth(Button_text), (OffSet)]) #Blit the text such that it is centred 
            OffSet += 50
        if not Music.Sound: #Initially, sound is true
            IconReference[2] = ['UnMute',(Graphics.MuteIcon, [0,0])]
        else:
            IconReference[2] = ['Mute',(Graphics.SoundIcon, [0,0])]
        for Icon in range(len(IconReference)):
            IconBlitList.append(screen.blit(IconReference[Icon][1][0],IconReference[Icon][1][1]))
        if BlitParameterInput:
            screen.blit(BlitParameterInput[0],BlitParameterInput[1])
        screen.blit(NAME_DISPLAY, [(55), 0])
        pygame.display.flip() #Outputs all images that are 'blitted' onto the screen
        for event in pygame.event.get(): #Listens for which event ocurred, if any
            BackGroundListenner.Listen(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #If event is a left-mouse click then check whether it clicked on any images
                MouseClick = pygame.mouse.get_pos()
                ButtonClick.Play()
                if Button_Icons[0].collidepoint(MouseClick):
                    Story_Level_Collection, MaxLevels = GetLevels()
                    for Level in Story_Level_Collection: #Allows to progress for one level to the next, can edit easily if more levels are added
                        PlayGame(Level, Tracking=str(MaxLevels))
                        USER.Restart = False
                        USER.Total_Score += USER.Level_Score
                    USER.Total_Score += 1000 #Mode completion bonus points
                    USER.CheckScore() #Check score against user's current scores
                elif Button_Icons[1].collidepoint(MouseClick):
                    GameMode = 'Random'
                    PlayGame(GameMode, Resurrect=True, Movement=True)
                elif Button_Icons[2].collidepoint(MouseClick):
                    DisplayInstructions(MainMenuFrameEntry, BackGroundFrame)
                elif Button_Icons[3].collidepoint(MouseClick):
                    DisplayPractiseOptionChoice(MainMenuFrameEntry)
                elif Button_Icons[4].collidepoint(MouseClick):
                    GameMode = 'Design'
                    DeveloperMode(GameMode)
                elif Button_Icons[5].collidepoint(MouseClick):
                    DisplayLeaderBoard(MainMenuFrameEntry, BackGroundFrame)
                elif IconBlitList[2].collidepoint(MouseClick):
                    Music.Switch()
                elif IconBlitList[1].collidepoint(MouseClick):
                    USER.Username, USER.Password, USER.Row, USER.Session_Scores = 0, 0, 0, 0
                    IntroScreen()
                elif IconBlitList[0].collidepoint(MouseClick):
                    Message.LoadingScreen()
                    Animation.FlipBook()
            elif pygame.MOUSEMOTION:
                BlitParameterInput = CursorOverButton(IconBlitList, IconReference)
        clock.tick(15) #Limit to 15 frames per second

def GetLevels(GameMode='Level', Start=None, End=None):
    LevelsToSort = []
    PreMade_Levels = os.listdir('Pre-Made')
    for l in PreMade_Levels:
        if GameMode in l: #Change 'Level 1' to 'Story 1'
            LevelsToSort.append(l[:-3]) #Slicing omitts file extension
    SortedLevels = SortLevels(LevelsToSort, GameMode)
    MaxLevels = len(SortedLevels)
    SortedLevels = SortedLevels[Start:End] #Select the range of levels user will do
    
    return SortedLevels, MaxLevels

def SortLevels(ToSort, GameMode):
    Numbers_Only = []
    for File in ToSort:
        Numbers_Only.append(int(re.findall(r'\d+', File)[0]))
    ToSort = [GameMode+' {}'.format(str(x)) for x in sorted(Numbers_Only)]
    
    return ToSort

def DisplayLeaderBoard(MainMenuFrameEntry, BackGroundFrame): 
    LeaderBoard, BlitParameterInput = True, False
    Sorting = "DEFAULT" #Leaderboard is displayed sorted by default, I.e.: sorted by highest score
    TableFIELD1, TableFIELD2, TableFIELD3, TableFIELD4, TableFIELD5 = SortLeaderBoardFile(Sorting)
    IconReference = [['Sort by highest average', (Graphics.SortAverageIcon, [(1055),(128)])],
                     ['Sort by highest score', (Graphics.SortHighestIcon, [(1000), (128)])]]
    while LeaderBoard:
        screen.fill(BLACK)
        IconBlitList = []
        if MainMenuFrameEntry == 5:
            MainMenuFrameEntry = 1
            BackGroundFrame = BackGroundFrame[::-1]
        screen.blit(BackGroundFrame[MainMenuFrameEntry], [0, 0])
        screen.blit(Graphics.MainMenuBottonBackGround, [(390), (50)])
        screen.blit(Graphics.LeaderBoardBackGround, [(240),(128)])
        Button_text = (XXV_text_font.render('Leaderboard',True, ORANGE))
        screen.blit(Button_text, [(600)-Format.GetWidth(Button_text), (50)])
        BackButtonIcon = screen.blit(Graphics.BackButtonIcon, [(1100), (500)])

        for Icon in range(len(IconReference)):
            IconBlitList.append(screen.blit(IconReference[Icon][1][0],IconReference[Icon][1][1]))
            
        if BlitParameterInput:
            screen.blit(BlitParameterInput[0],BlitParameterInput[1])

        OffSet = 0
        for Record in range(6): #Only want to display 6 records of scores, top 5 people and the user
            screen.blit(TableFIELD1[Record], [(260), (205+OffSet)])
            screen.blit(TableFIELD2[Record], [(478-Format.GetWidth(TableFIELD2[Record])), (205+OffSet)])
            screen.blit(TableFIELD3[Record], [(638-Format.GetWidth(TableFIELD3[Record])), (205+OffSet)])
            screen.blit(TableFIELD4[Record], [(798-Format.GetWidth(TableFIELD4[Record])), (205+OffSet)])
            screen.blit(TableFIELD5[Record], [(918-Format.GetWidth(TableFIELD5[Record])), (205+OffSet)])
            OffSet += 65

        if Sorting == "AVERAGE":
            Boarder = pygame.draw.rect(screen, DARKYELLOW, ((1055), (128), (45), (45)), 3)
        else:
            Boarder = pygame.draw.rect(screen, DARKYELLOW, ((1000), (128), (45), (45)), 3)
            
        pygame.display.flip()
        MainMenuFrameEntry += 1
        for event in pygame.event.get():
            BackGroundListenner.Listen(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                MouseClick = pygame.mouse.get_pos()
                ButtonClick.Play()
                if BackButtonIcon.collidepoint(MouseClick):
                    DisplayMenu()
                elif IconBlitList[0].collidepoint(MouseClick):
                    if Sorting != "AVERAGE": #Ensures sorting subroutine is only executed if a new sorting method is chosen
                        Sorting = "AVERAGE"
                        TableFIELD1, TableFIELD2, TableFIELD3, TableFIELD4, TableFIELD5 = SortLeaderBoardFile(Sorting)
                elif IconBlitList[1].collidepoint(MouseClick):
                    if Sorting != "DEFAULT": #Ensures sorting subroutine is only executed if a new sorting method is chosen
                        Sorting = "DEFAULT"
                        TableFIELD1, TableFIELD2, TableFIELD3, TableFIELD4, TableFIELD5 = SortLeaderBoardFile(Sorting)
            elif pygame.MOUSEMOTION:
                BlitParameterInput = CursorOverButton(IconBlitList, IconReference)
        clock.tick(15)

def SortLeaderBoardFile(Sorting): 
    TableFIELD1, TableFIELD2, TableFIELD3, TableFIELD4, TableFIELD5 = [], [], [], [], []
    No_Sort = []
    Scores = USER_DATABASE.File_Contents
    DEFAULT_Sort, AVERAGE_Sort = {}, {}
    for Row in range(1,len(Scores)):
        name = Scores[Row][0]
        Session_Scores = list(map(int, Scores[Row][2:5]))
        No_Of_Zeros = Session_Scores.count(0) #When a new user is created they are assigned 3 scores of 0, average after one game is therefore calculated unfairly
        try:
            average = round(sum(Session_Scores)/(3-No_Of_Zeros)) #If there is 2 zeros then average = only score//if there is 1 zero, then average accounts for 2 scores
        except ZeroDivisionError:
            average = 0 #If a new user
        highest = max(Session_Scores)
        DEFAULT_Sort[name], AVERAGE_Sort[name] = highest, average
        No_Sort.append([name,Session_Scores,average])
    Sort_Methods = {'DEFAULT':sorted(DEFAULT_Sort.items(), key=operator.itemgetter(1),reverse=True),
                    'AVERAGE':sorted(AVERAGE_Sort.items(), key=operator.itemgetter(1),reverse=True)}
    Sort = Sort_Methods.get(Sorting) #Gets the value associated with the key, in this case the sorted data as a list of tuples
    OffSet = 0
    for name in Sort[0:5]: #Iterating through sliced list to output only top 5
        USER_SCORES = [item for item in No_Sort if item[0] == name[0]]
        TableFIELD1.append((XX_text_font.render(name[0], True, ( 217, 151+OffSet,   9+OffSet)))) #Arbitrary values to ensure text is formatted properly
        TableFIELD2.append((XX_text_font.render(str(USER_SCORES[0][1][0]), True, ( 217, 151+OffSet,   9+OffSet))))
        TableFIELD3.append((XX_text_font.render(str(USER_SCORES[0][1][1]), True, ( 217, 151+OffSet,   9+OffSet))))
        TableFIELD4.append((XX_text_font.render(str(USER_SCORES[0][1][2]), True, ( 217, 151+OffSet,   9+OffSet))))
        TableFIELD5.append((XX_text_font.render(str(USER_SCORES[0][2]), True, ( 217, 151+OffSet,   9+OffSet))))
        OffSet += 20

    SORTED_USER_DATA = [item for item in Sort if item[0] == USER.Username] #isolates the tuple relating to the user in the 'Sort' list of tuples
    USER_POS = Sort.index(SORTED_USER_DATA[0])+1 #finds the position of the user in the sorted list of tuples

    USER_SCORES = [item for item in No_Sort if item[0] == USER.Username]
    TableFIELD1.append((XX_text_font.render("{0}. {1}".format(USER_POS,USER.Username), True, ORANGE)))
    TableFIELD2.append((XX_text_font.render(str(USER.Session_Scores[0]), True, ORANGE)))
    TableFIELD3.append((XX_text_font.render(str(USER.Session_Scores[1]), True, ORANGE)))
    TableFIELD4.append((XX_text_font.render(str(USER.Session_Scores[2]), True, ORANGE)))
    TableFIELD5.append((XX_text_font.render(str(USER_SCORES[0][2]), True, ORANGE)))
    
    return TableFIELD1, TableFIELD2, TableFIELD3, TableFIELD4, TableFIELD5
    
def DeveloperMode(GameMode, ObjectStorage=None, Object=None):
    Message.LoadingScreen()
    if ObjectStorage == None:
        ObjectStorage = []
    while True:
        Valid = False #Determines whether created map can be tested or not//constantly requires checking
        screen.blit(Maps.IDEBackGround, [0, 0]) #Always blitted first, so that it is at the back
        
        if ObjectStorage: #if an object has been placed
            for Placement in range(len(ObjectStorage)):
                Pos = ObjectStorage[Placement][0]
                Type = ObjectStorage[Placement][1]
                if Type[0] == 'M':
                    Valid = True #Map can only be tested if at least one monster has been placed
                screen.blit(getattr(Objects, '{}'.format(Type)), Pos) #Co-ordinate value can be tuple of a list
                
        pygame.draw.rect(screen,DARKGREY,((1000),0,(200),(600)))
        
        OptionsIcon = screen.blit(Graphics.Options, [(1145), (10)])
                
        ObjectDisplayBackGround = pygame.draw.rect(screen, DARKGREYPOP, ((1010), (65), (180), (375)))
  
        CordsDisplayLarge = pygame.draw.rect(screen, DARKGREYPOP, ((1010), (445), (180), (45)))
        CordsDisplayLargeBoarder = pygame.draw.rect(screen, BLACK, ((1010), (445), (180), (45)), 3)

        GameModeDisplay = pygame.draw.rect(screen, DARKGREYPOP, ((1010), (545), (180), (35)))
        GameModeDisplay_text = (XXV_text_font.render("Mode: "+GameMode,True,PURPLE))
        screen.blit(GameModeDisplay_text, [(1010), (545)])

        ToolDisplay = pygame.draw.rect(screen, DARKGREYPOP, ((1010), (500), (180), (40)))
        UndoOption = (XX_text_font.render("(U)ndo",True,ORANGE))
        ClearOption = (XX_text_font.render("(C)lear",True,ORANGE))
        SaveOption = (XX_text_font.render("(S)ave",True,ORANGE))
        LoadOption = (XX_text_font.render("(L)oad",True,ORANGE))
        TestOption = (XX_text_font.render("(T)est",True,ORANGE))
        screen.blit(UndoOption, [(1010), (500)])
        screen.blit(ClearOption, [(1070), (500)])
        screen.blit(SaveOption, [(1010), (520)])
        screen.blit(LoadOption, [(1070), (520)])
        screen.blit(TestOption, [(1130), (510)])

        MousePosition = pygame.mouse.get_pos()
        if Object:
            if Object[0] == 'M': #Added statements so user can determine which mode their cursor is in
                OUTLINE = RED
            elif Object[0] == 'R': #Only interested in first character of string
                OUTLINE = GREY
            elif Object[0] == 'G':
                OUTLINE = BROWN
        else:
            OUTLINE = PURPLE
        CordsToScreen(MousePosition, OUTLINE)
        
        MonsterIcon = screen.blit(Objects.M1, [(1025), (80)])
        RockIcon = screen.blit(Objects.R, [(1085), (80)])
        GraveIcon = screen.blit(Objects.G, [(1145), (80)])
        
        Monster2Icon = screen.blit(Objects.M2, [(1025), (120)])
        Monster3Icon = screen.blit(Objects.M3, [(1085), (120)])
        Monster4Icon = screen.blit(Objects.M4, [(1145), (120)])

        Grave2Icon = screen.blit(Objects.G2, [(1025), (160)])
        Grave3Icon = screen.blit(Objects.G3, [(1085), (160)])
        Grave4Icon = screen.blit(Objects.G4, [(1145), (160)])
        
        Message.Display(2)
                
        pygame.display.flip()
        for event in pygame.event.get():
            BackGroundListenner.Listen(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                Object = None
                ObjectStorage = IDEInput('Load', ObjectStorage)
                
            elif event.type == pygame.KEYDOWN and ObjectStorage:
                if event.key == pygame.K_u:
                    Object = None
                elif event.key == pygame.K_c:
                    ObjectStorage = []
                elif event.key == pygame.K_s:
                    if Valid:
                        ObjectStorage = IDEInput('Save', ObjectStorage)
                elif event.key == pygame.K_t:
                    if Valid:
                        USER.Restart = False
                        PlayGame("Sandbox", ObjectStorage, Resurrect=True) #Did not assign GameMode before this routine is called to prevent restarts occuring
                        SpritePositions.ResetImage_Alphas('G')
                    else:
                        Message.Info = "There must be at least one enemy on the map"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                MouseClick = pygame.mouse.get_pos()
                ButtonClick.Play()
                if OptionsIcon.collidepoint(MouseClick):
                  PauseMenu.Display(GameMode, ObjectStorage)
                elif MonsterIcon.collidepoint(MouseClick):
                    Object = 'M1' #Objects.Minion
                elif Monster2Icon.collidepoint(MouseClick):
                    Object = 'M2'
                elif Monster3Icon.collidepoint(MouseClick):
                    Object = 'M3'
                elif Monster4Icon.collidepoint(MouseClick):
                    Object = 'M4'
                elif RockIcon.collidepoint(MouseClick):
                    Object = 'R1' #Objects.Rock
                elif GraveIcon.collidepoint(MouseClick):
                    Object = 'G1' #Objects.GraveStone
                elif Grave2Icon.collidepoint(MouseClick):
                    Object = 'G2'
                elif Grave3Icon.collidepoint(MouseClick):
                    Object = 'G3'
                elif Grave4Icon.collidepoint(MouseClick):
                    Object = 'G4'
                elif CordsToScreen(MouseClick):
                    MouseClick = Format.GridLock(MouseClick) #Gridlock functionality
                    if Object:
                        ObjectStorage.append([MouseClick, Object])
                    else: #If the user is undoing instead of placing
                        for Placement in range(len(ObjectStorage)): #Check if an occupied position is being deleted
                            if ObjectStorage[Placement][0] == MouseClick:
                                del ObjectStorage[Placement] 
                                break
        clock.tick(60)
        if len(ObjectStorage) >= 2: #Only check for duplicate positions if at least 1 object has been placed
            ObjectStorage = ValidatePositions(ObjectStorage) #Remove duplicate positions

def ValidatePositions(ObjectStorage):
    Taken_Pos = [] #Stores all positions currently occupied
    for Placement in range(len(ObjectStorage)): #Iterates through placed objects to determine whether position clicked is already taken
        try:
            if Taken_Pos.count(ObjectStorage[Placement][0]) == 0:
                Taken_Pos.append(ObjectStorage[Placement][0])
            else:
                del ObjectStorage[Placement] #Pops the object added by the user
        except:
             pass
    return ObjectStorage #Returns valid positioning, ensures all positions contain only 1 object

            
def IDEInput(KEY, ObjectStorage):  
    LoadOrWrite = True
    User_Input_Collection = []
    screenshot = screen.copy()
    screenshot.set_alpha(100)
    while LoadOrWrite:
        screen.fill(BLACK)
        screen.blit(screenshot, [0,0])
        
        InputBar = pygame.draw.rect(screen, BLACK, (0, (545), (1000), (55)))
        if len(User_Input_Collection) > 40: #File name should not exceed 40 characters in length
            del User_Input_Collection[-1]
        FileName = (''.join(map(str, User_Input_Collection))).title() #I can apply 2 functions here by using parenthesis
        INPUTBOX = (XXV_text_font.render(KEY+", file: "+FileName,True,WHITE)) #KEY informs the user what process is going to occur to the file

        screen.blit(INPUTBOX, [(30), (555)])
        pygame.display.flip()
        for event in pygame.event.get():
            BackGroundListenner.Listen(event)
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == 'backspace' and len(User_Input_Collection) >= 1:
                    del User_Input_Collection[-1]
                elif pygame.key.name(event.key) == 'return' and len(User_Input_Collection) >= 1:
                    FileName = FileName.strip() #Omits trailing and leader 'spaces'//Must be applied here!
                    try:
                        if KEY == 'Load':
                            ObjectStorage = LoadFile(FileName, 'Creations', ObjectStorage) #added title()
                        elif KEY == 'Save':
                            SaveToFile(FileName.title(), ObjectStorage)
                        elif KEY == 'Overwrite' and len(User_Input_Collection) == 1 and User_Input_Collection[0] == 'y':
                            Message.Info = "File Overwritten!" #Allows SaveToFile to trigger 'overwrite file' process
                    except:
                        pass
                    LoadOrWrite = False
                elif pygame.key.name(event.key) == 'escape': #allows the user to cancel the load/save process
                    LoadOrWrite = False
                    Message.Info = KEY+" Process Cancelled."
                elif pygame.key.name(event.key) == 'space':
                    User_Input_Collection.append(' ')
                elif not len(pygame.key.name(event.key)) > 1:
                    User_Input_Collection.append(pygame.key.name(event.key))
    clock.tick(1) #FPS is set very low so that keyboard input stack is not updated frequently
    return ObjectStorage
    
def SaveToFile(FileName, ObjectStorage):
    File_Path = 'Creations' #May be changed if the user wants to save to a different directory
    FileName = os.path.join(File_Path, FileName+str('.txt')) #First parameter is always from the point of view from where this py file is
    try:
        FileHandle = open(FileName, 'r') #attempts to read, serves as a check to whether file inputted exists or not
        FileHandle.close()
        ObjectStorage = IDEInput('Overwrite', ObjectStorage)
        if Message.Info == "File Overwritten!": #Returns true only if the user enters 'y'
            FileHandle = open(FileName, 'w')
            FileHandle.write(str(ObjectStorage))
        else:
            Message.Info = "Overwritten Process Cancelled!"
    except:
        FileHandle = open(FileName, 'w')
        FileHandle.write(str(ObjectStorage))
        Message.Info = "File saved successfully to the 'Creations' folder!"
    FileHandle.close()

def LoadFile(FileName, File_Path, ObjectStorage=None):
    try:
        FileName = os.path.join(File_Path, FileName+str('.txt'))
        FileHandle = open(FileName, 'r')
        ObjectStorage = FileHandle.readline() #Read the first lines completely
        FileHandle.close()
        ObjectStorage = ast.literal_eval(ObjectStorage) #convert from string to list
        Message.Info = "File loaded successfully!"
    except:
        Message.Info = "File does not exist!"
    
    return ObjectStorage

def DisplayInstructions(MainMenuFrameEntry, BackGroundFrame):
    Instructions = True
    while Instructions:
        screen.fill(BLACK)
        if MainMenuFrameEntry == 5:
            MainMenuFrameEntry = 1
            BackGroundFrame = BackGroundFrame[::-1]
        screen.blit(BackGroundFrame[MainMenuFrameEntry], [0, 0])
        screen.blit(Graphics.MainMenuBottonBackGround, ([390, 50]))
        screen.blit(Graphics.Instructions, ([390, 100]))
        Button_text = (XXV_text_font.render('Instructions',True,ORANGE))
        screen.blit(Button_text, [(600)-Format.GetWidth(Button_text), (50)])
        BackButtonIcon = screen.blit(Graphics.BackButtonIcon, ([1100, 500])) 
        pygame.display.flip()
        MainMenuFrameEntry += 1
        for event in pygame.event.get():
            BackGroundListenner.Listen(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                MouseClick = pygame.mouse.get_pos()
                ButtonClick.Play()
                if BackButtonIcon.collidepoint(MouseClick):
                    Instructions = False
        clock.tick(15)
        
def DisplayPractiseOptionChoice(MainMenuFrameEntry):
    DisplayPractiseOptionChoice = True
    BackGroundFrame = [Graphics.MenuBackGround,Graphics.MenuBackGround1,Graphics.MenuBackGround2,Graphics.MenuBackGround3,Graphics.MenuBackGround4]
    while DisplayPractiseOptionChoice:
        screen.fill(BLACK)
        if MainMenuFrameEntry == 5:
            MainMenuFrameEntry = 1
            BackGroundFrame = BackGroundFrame[::-1]
        screen.blit(BackGroundFrame[MainMenuFrameEntry], [0, 0])
        Menu_Options = ['Practise Option Select', ' 1. Example using y=x^2', ' 2. Example of Rocks', ' 3. Example of multiple paths']
        OffSet = 50
        Button_Icons = []
        for Button in range(len(Menu_Options)):
            Button_Icons.append(screen.blit(Graphics.MainMenuBottonBackGround, ([390, OffSet])))
            Button_text = (XXV_text_font.render(Menu_Options[Button],True, DARKGREYPOP))
            screen.blit(Button_text, [(600)-Format.GetWidth(Button_text), (OffSet)])
            OffSet += 100 # Ensures buttons are blitted to the screen in increments of 50, so they appear apart
            
        BackButtonIcon = screen.blit(Graphics.BackButtonIcon, ([1100, 500]))
        MainMenuFrameEntry += 1
        pygame.display.flip()
        for event in pygame.event.get():
            BackGroundListenner.Listen(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #event.button == 1 - left mouse click
                MouseClick = pygame.mouse.get_pos()
                ButtonClick.Play()
                if Button_Icons[1].collidepoint(MouseClick):
                    GameMode = 'Practise 1'
                    PlayGame(GameMode)
                    USER.Restart = False
                elif Button_Icons[2].collidepoint(MouseClick):
                    GameMode = 'Practise 2'
                    PlayGame(GameMode)
                    USER.Restart = False
                elif Button_Icons[3].collidepoint(MouseClick):
                    GameMode = 'Practise 3'
                    PlayGame(GameMode)
                    USER.Restart = False
                elif BackButtonIcon.collidepoint(MouseClick):
                    DisplayPractiseOptionChoice = False #Better than DisplayMenu()
        clock.tick(15)

def ScaleText(TextRectangle, MaxWidth):
    WidthScale = 1
    if TextRectangle.get_width() > MaxWidth:
        WidthScale = MaxWidth/TextRectangle.get_width()
    New_Dimensions = (int(TextRectangle.get_width() * WidthScale), int(TextRectangle.get_height()))
    TextRectangle = pygame.transform.scale(TextRectangle, New_Dimensions)

    return TextRectangle
       
def PlayGame(GameMode, ObjectStorage=None, Tracking='', Resurrect=False, Movement=False):
    Display, ExponentialValue = True, 1
    MouseDrag, MouseRightClick, GridGuide = False, False, False
    User_Input_Collection = []
    EnterKeyPressedTimes, USER.Level_Score, NoOfMoves = 0, 0, 0
    
    Message.InputColour, GameMode_Colour = GREEN, GREEN
    
    if GameMode == 'Sandbox':
        GameMode_Colour = PURPLE
    elif GameMode == 'Random':
        GameMode_Colour = RED
        
    SpritePositions.Get(GameMode, ObjectStorage)
    Message.LoadingScreen()
    SpritePositions.ResetImage_Alphas('G') #Reset image alphas before each game begins
    
    if Tracking: #Allows the user to see their progress
        if '/' not in Tracking:
            Tracking = '/'+Tracking
        
    while not USER.Restart:
        screen.fill(BLACK)
        if GameMode == 'Random':
            screen.blit(Maps.RandomLevelBackGround, [0, 0])
        elif 'Practise' in GameMode:
            screen.blit(Maps.PractiseLevelBackGround, [0, 0])
        else:
            screen.blit(Maps.MainLevelBackGround, [0,0])

        if Movement:
            SpritePositions.RandomMovement(random.randint(1,1000))

        if Resurrect:
            SpritePositions.Resurrect(random.randint(1,1000))

        SpritePositions.Display() #Ensures sprites have second lowest blit priority and hence only go to the front of the background
        
        pygame.draw.rect(screen,DARKGREY,(1000,0,200,600))
        OptionsIcon = screen.blit(Graphics.Options, [1145, 10])

        TotalScoreDisplay = pygame.draw.rect(screen, DARKGREYPOP, (1010, 10, 125, 45))
        TotalScoreDisplay_text = (XXV_text_font.render("Score ({})".format(USER.Total_Score),True,DARKYELLOW)) #Displays the user's cumulative score for the game
        ScoreDisplay_text = (XXV_text_font.render(str(USER.Level_Score),True,DARKYELLOW)) #Displays the user's score attained for the level they are on only
        screen.blit(TotalScoreDisplay_text, [1010, 10])
        screen.blit(ScoreDisplay_text, [1010, 35])
        
        UserNameDisplay = pygame.draw.rect(screen, DARKGREYPOP, (1010, 65, 180, 20))
        UserNameDisplay_text = (XX_text_font.render(USER.Username,True,WHITE)) #Displays the username
        screen.blit(UserNameDisplay_text, [1010, 65])

        Moves.Display(GameMode, NoOfMoves)

        ProfileDisplay = pygame.draw.rect(screen, DARKGREYPOP, ((1010), (115), (180), (330)))
        
        CordsDisplayLarge = pygame.draw.rect(screen, DARKGREYPOP, ((1010), (445), (180), (45)))
        CordsDisplayLargeBoarder = pygame.draw.rect(screen, BLACK, ((1010), (445), (180), (45)), 3)
        
        EquationInputDisplay = pygame.draw.rect(screen, Message.InputColour, ((1010), (500), (180), (25)))
        EquationInputDisplayBoarder = pygame.draw.rect(screen, DARKGREYPOP, ((1010), (500), (180), (25)), 1)
        
        GameModeDisplay = pygame.draw.rect(screen, DARKGREYPOP, ((1010), (545), (180), (35)))

        GameModeDisplay_text = ScaleText(XXV_text_font.render("Mode: "+GameMode+Tracking,True,GameMode_Colour), 180) #Allows user to see progress
        screen.blit(GameModeDisplay_text, ([1010, 545]))
                    
        if EnterKeyPressedTimes % 2 == 1: 
            ListToString = ''.join(map(str, User_Input_Collection))
            Input_Display = ScaleText(XXV_text_font.render(ListToString,True,WHITE), 180) 
            screen.blit(Input_Display, [(1100)-Format.GetWidth(Input_Display), (500)])

        Message.Display(2)
        
        if SpritePositions.Clicked[0]:
            screen.blit(SpritePositions.Clicked[0], SpritePositions.Clicked[1]) #Prolong display of profile

        if GridGuide: #Only returns true if the space bar is being held down
            pygame.draw.line(screen, WHITE, ([0,600]), ([1000,600]), 5)
            pygame.draw.line(screen, WHITE, ([500,600]), ([500,0]), 5)
        
        if MouseDrag and MouseRightClick:
            MousePosition = pygame.mouse.get_pos()
            CordsToScreen(MousePosition)
        else:
            Display = '<<Hold Right-Click to view Cords>>'
            Prompt_Text = (X_text_font.render(Display,True,WHITE))
            screen.blit(Prompt_Text, [(1100)-Format.GetWidth(Prompt_Text), (462)])
            
        if EnterKeyPressedTimes % 2 != 1: #Enter is pressed once to initialise input box, then twice to confirm function to be sketched
            if Message.InputColour == GREEN:
                Display = '<<Press enter to input>>'
            elif Message.InputColour == RED:
                if Message.Info == 'Welldone! All monsters have been killed! Level complete!':
                    Display = '<<LEVEL COMPLETED>>'
                else:
                    Display = '<<COOLDOWN>>' #based on time.delay
                    
            Prompt_Text = (X_text_font.render(Display,True,WHITE))
            screen.blit(Prompt_Text, ((1100)-Format.GetWidth(Prompt_Text), (505)))
        
        if SpritePositions.AreaOfEffectCords:
            for Area in SpritePositions.AreaOfEffectCords:
                pygame.draw.rect(screen, GREEN, (Area[0],Area[1],3,3)) #Plots graph on GUI
            LaserEffect.Play()
            pygame.display.flip()
            pygame.time.delay(1000) #gives user time to view function on screen
            SpritePositions.AreaOfEffectCords = []
        else:
            pygame.display.flip()
            

        for event in pygame.event.get():
            BackGroundListenner.Listen(event)
            
            if event.type == pygame.MOUSEMOTION:
                MouseDrag = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    MouseRightClick = False
                    MouseDrag = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not Message.Info: #1 -> left-click | 2 -> middle-click | 3 -> right-click | 4 -> scroll-up | 5 -> scroll-down
                    MouseClick = pygame.mouse.get_pos()
                    ButtonClick.Play()
                    if OptionsIcon.collidepoint(MouseClick):
                        if GameMode == 'Sandbox':
                            SandboxMenu.Display(GameMode, ObjectStorage, Tracking, Resurrect, Movement)
                        else:
                            PauseMenu.Display(GameMode, ObjectStorage, Tracking, Resurrect, Movement) #ObjectStorage is passed in, in case restart is called when playing designed level
                    else:
                        SpritePositions.CheckClick(MouseClick) #Check if mouse click resulted in a sprite graphic collision
                elif event.button == 3: 
                    MouseRightClick = True
    
            elif event.type == pygame.KEYDOWN:
                if Moves.MoveIsValid(NoOfMoves, GameMode, ObjectStorage): #Prevents user from making further keyboard input, should moves be depleted
                    if event.key == pygame.K_SPACE:
                        GridGuide = True
                    elif event.key == pygame.K_RETURN:
                        if Message.InputColour == GREEN:
                            EnterKeyPressedTimes += 1
                            if EnterKeyPressedTimes % 2 == 0: #When enter is pressed for a second time
                                if len(User_Input_Collection) <= 2:
                                    Message.Info = 'The function you entered is invalid, please re-enter'
                                else:
                                    if User_Input_Collection[-1] in ['+', '-', '/']: 
                                        del User_Input_Collection[-1]
                                        ListToString = ListToString[:-1] #Updates ListToString based incomplete operator and operand
                                    Equation = User_Input_Collection[2:] #Omit the first 2 characters
                                    SpritePositions.SketchGraph(Equation, ListToString, YorX)
                                    Message.InputColour = RED #Indicates a function was entered
                                    if SpritePositions.GameOver(): #Check if the game is over
                                        Message.Format(TextColour=PURPLE)
                                        Message.Info = 'Welldone! All monsters have been killed! Level complete!'
                                    if GameMode != 'Sandbox': #Sandbox game mode should not trigger restart menu//infinite moves
                                        NoOfMoves += 1
                                #Re-Initialise variables
                                ExponentialValue = 1
                                User_Input_Collection = []
                                  
                    elif EnterKeyPressedTimes % 2 == 1: #Check whether input box is allowed for input
                        if len(User_Input_Collection) != 14:
                            if len(User_Input_Collection) == 0:
                                if pygame.key.name(event.key) in ['y', 'x']:
                                    User_Input_Collection.append(pygame.key.name(event.key))
                                    YorX = pygame.key.name(event.key)
                                    InverseXY = ['x','y'] #Store 'x' if f(x), store 'y' if f(y) // ValidUnknown
                                    InverseXY.remove(YorX)
                                    InverseXY = InverseXY[0]
                                else:
                                    Message.Info = 'You may only enter "y" or "x" as the first letter'
                            elif event.key == pygame.K_BACKSPACE: #Check if backspace is pressed
                                if len(User_Input_Collection) > 0:
                                    del User_Input_Collection[-1]
                                    ExponentialValue = 1
                            elif len(User_Input_Collection) == 1:
                                if event.key == pygame.K_EQUALS:
                                    User_Input_Collection.append('=')
                                else:
                                    Message.Info = 'You should only place "=" as the second letter'
                            else:
                                if pygame.key.name(event.key) in [str(x) for x in range(0,10)]:
                                    print("number")
                                    if pygame.key.name(event.key) == '0': #A '0' should only be entered as a 'trailing zero' and not as multiplication by 0
                                        if User_Input_Collection[-1].isnumeric():
                                            User_Input_Collection.append('0')
                                        else:
                                            Message.Info = 'Only trailing zeros may be entered'
                                        ExponentialValue = 1
                                        
                                    else:        
                                        if User_Input_Collection[-1].isnumeric() or User_Input_Collection[-1] in ['=', '+', '/', '-']:
                                            User_Input_Collection.append(pygame.key.name(event.key))
                                        else:
                                            Message.Info = 'Invalid digit placement'
                                        ExponentialValue = 1
                            
                                        
                                elif type(pygame.key.name(event.key)) is str: #either an operator or unknown
                                    print("checking -")
                                    if pygame.key.name(event.key) == InverseXY:
                                        if User_Input_Collection[-1] in [InverseXY, (InverseXY+'^'+str(ExponentialValue))]:
                                            if ExponentialValue != 4: #capped exponential index at 4
                                                ExponentialValue += 1
                                                User_Input_Collection[-1] = InverseXY+'^'+str(ExponentialValue)
                                        else:
                                            User_Input_Collection.append(InverseXY)

                                    elif pygame.key.name(event.key) == YorX:
                                        Message.Info = 'The first letter was "{0}" so you can only enter "{1}" now'.format(YorX, InverseXY)

                                    elif User_Input_Collection[-1] not in ['/', '+', '-']: #ensures no duplicate operators
                                        if event.key == pygame.K_EQUALS:
                                            if pygame.key.get_mods() and pygame.KMOD_LSHIFT: 
                                                User_Input_Collection.append('+')
                                                ExponentialValue = 1

                                        elif event.key == pygame.K_MINUS:
                                            User_Input_Collection.append('-')
                                            ExponentialValue = 1

                                        elif (event.key == pygame.K_SLASH) and (User_Input_Collection[-1] != '='):
                                            User_Input_Collection.append('/')
                                            ExponentialValue = 1
    
                                else:
                                    Message.Info = 'The key you entered made the equation invalid, please re-enter'
                        else:
                            if event.key == pygame.K_BACKSPACE: #Check if backspace is pressed
                                if len(User_Input_Collection) > 0:
                                    del User_Input_Collection[-1]
                                    ExponentialValue = 1
                            else:
                                Message.Info = 'Maximum equation length'

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    GridGuide = False
        clock.tick(60)
    screen.fill(BLACK)
    pygame.display.flip()

def CursorOverButton(IconBlitList, IconReference):
    CursorPosition = pygame.mouse.get_pos()
    Cords = list(CursorPosition)
    BlitParameterInput = False
    for Icon in range(len(IconBlitList)):
        if IconBlitList[Icon].collidepoint(CursorPosition):
            CursorText = X_text_font.render(IconReference[Icon][0],True,WHITE)
            BlitParameterInput = CursorText, (Cords[0]+10, Cords[1]+10)
            break

    return BlitParameterInput
    
def CordsToScreen(MousePosition, OutLine_Colour=PURPLE): #Cords come in as ACTUAL points on the grid
    Cords = (list(MousePosition))

    GameCords = [int(Cords[0]-500),int(599-Cords[1])] #Convert to Int to remove huge decimal values
    GameCords_Text = X_text_font.render((str(tuple(GameCords))),True,WHITE) #conversion to tuple for co-ordinate visualation, [] imply vector
    GameCords_Text_Large = (XL_text_font.render((str(tuple(GameCords))),True,WHITE))
    if Cords[0] <= 1000: #Cords 1000+ are taken up by a toolbar
        #If statements below ensure all cords can be viewed
        if Cords[1] > 580 and Cords[0] <= 950:
            screen.blit(GameCords_Text, (MousePosition[0]+10, MousePosition[1]-10)) 
        elif Cords[0] > 950 and Cords[1] >= 15:
            screen.blit(GameCords_Text, (MousePosition[0]-50, MousePosition[1]-10))
        elif Cords[0] > 950 and Cords[1] < 15:
            screen.blit(GameCords_Text, (MousePosition[0]-50, MousePosition[1]+10)) # x - moves left(-)/right(+) y = moves up(-)/down(+)
        else:
            screen.blit(GameCords_Text, (MousePosition[0]+10, MousePosition[1]+10))

        MousePosition = Format.GridLock(MousePosition)
        screen.blit(GameCords_Text_Large, ((1100)-Format.GetWidth(GameCords_Text_Large) ,(445)))
        pygame.draw.rect(screen, OutLine_Colour,(MousePosition[0], MousePosition[1], (30), (30)), 3)
    else:
        Cords = False
    return Cords
    
def GetUserInput(LOGINSTAGE, MessageLog, User_Input_Collection=[]):
    PATCH_NOTES = [["By Michael Kyriakou"], [">>Press any key to skip MICHAEL GAMES sequence"], [">>'Resurrect' gravestones in RANDOM and SANDBOX"], [">>Additional random 'movement' in RANDOM"]] ########ANY UPDATES MUST BE REFERENCED HERE
    GetUserInput = True
    LoginFrameEntry = 0
    while GetUserInput:
        screen.fill(BLACK)

        Animation.ImageMotion(Animations.MovingBackGround, 5, 'Down')
        
        screen.blit(Graphics.TrajectoriamLogo, [0, 0])
        if len(User_Input_Collection) == 0:
            User_Input_Collection = ["_"]

        OffSet = 0
        for line in PATCH_NOTES:
            PATCHNOTES_DISPLAY = (XX_text_font.render(line[0],True, PURPLE))
            screen.blit(PATCHNOTES_DISPLAY, [(30), (100+OffSet)])
            OffSet += 20
                
        PROMPT_INFO = (XLV_Gothic_text_font.render(LOGINSTAGE,True, RED))
        pygame.draw.rect(screen,BLACK,((600)-Format.GetWidth(PROMPT_INFO), (300), Format.GetWidth(PROMPT_INFO, False), (55))) #Dynamically shape depending on prompt length
        screen.blit(PROMPT_INFO, [(600)-Format.GetWidth(PROMPT_INFO), (300)])

        if MessageLog:
            OffSet = 0
            while len(MessageLog) >= 5:
                del MessageLog[0]
            for Line in reversed(MessageLog):
                MESSAGE_INFO = (XX_text_font.render(Line, True, ( 255,   OffSet,   OffSet)))
                screen.blit(MESSAGE_INFO, [(210), (500+OffSet)])
                OffSet += 25
        ListToString = ''.join(map(str, User_Input_Collection))


        if LOGINSTAGE == "Enter Username": #otherwise the password would be capitalised
            ListToString = ListToString.title()
            USER_INPUT = (XLV_text_font.render(ListToString,True, WHITE))#added title to capitalise first letter
        elif "password" in LOGINSTAGE:
            if User_Input_Collection[0] != "_":
                Encrypted_Text = '*'*len(ListToString)
                USER_INPUT = (XLV_text_font.render(Encrypted_Text,True, WHITE))
            else:
                USER_INPUT = (XLV_text_font.render(ListToString,True, WHITE))
        else:
            USER_INPUT = (XLV_text_font.render(ListToString,True, WHITE))

        
        screen.blit(Graphics.LoginCharacter, [(475), (20)])
        screen.blit(USER_INPUT, [(600)-Format.GetWidth(USER_INPUT), (400)])
        LoginFrameEntry += 1
        pygame.display.flip()
        for event in pygame.event.get():
            BackGroundListenner.Listen(event) #Don't want to invoke key functionalities
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == 'backspace' and len(User_Input_Collection) >= 1:
                    del User_Input_Collection[-1]
                elif pygame.key.name(event.key) == 'return' and len(User_Input_Collection) >= 1:
                    if len(User_Input_Collection) >= 1 and User_Input_Collection[0] != '_':
                        USERINPUT = ListToString
                        GetUserInput = False
                elif not len(pygame.key.name(event.key)) > 1:
                    if len(User_Input_Collection) != 11:
                        if User_Input_Collection[0] == "_":
                            del User_Input_Collection[-1]
                        User_Input_Collection.append(pygame.key.name(event.key))
                    else:
                        MessageLog.append("Character limit has been exceeded")
        clock.tick(30)
    Message.LoadingScreen()
    return USERINPUT

    
def LoginProcess(MessageLog):
    USEREXISTS = False
    while not USER.Username:
        USER_DATABASE.ReloadData()
        USERNAME = GetUserInput("Enter Username", MessageLog)
        for Row in range(1,len(USER_DATABASE.File_Contents)): #Start from 1, due to first row being headings
            if USERNAME == USER_DATABASE.File_Contents[Row][0]: #Find record corresponding to the user
                CHECKPASSWORD = USER_DATABASE.File_Contents[Row][1]
                USEREXISTS = True
                break
        if not USEREXISTS: 
            MessageLog.append("The username '%s' does not exist" % USERNAME)
            YorN = GetUserInput("Create '%s'? (Y)es (N)o" % USERNAME, MessageLog)
            if YorN == 'y':
                while True:
                    Password1 = GetUserInput("Enter your password", MessageLog)
                    Password2 = GetUserInput("Re-enter your password", MessageLog)
                    if Password1 == Password2:
                        break
                    MessageLog.append("Passwords do not match, please re-try")
                Account = [USERNAME, Password1, 0, 0, 0] #write new user to file along with 3 default scores of 0 to make it easier when sorting and updating scores
                USER_DATABASE.CreateNewUser(Account)
                MessageLog.append("User '%s' successfully created!" % USERNAME)
        else:
            MessageLog.append("Logging into '%s'..." % USERNAME)
            Password = GetUserInput("Enter password", MessageLog)
            if CHECKPASSWORD != Password:
                MessageLog.append("Incorrect password, please try to login again")
                USEREXISTS = False
            else:
                Session_Scores = list(map(int, USER_DATABASE.File_Contents[Row][2:5])) #Reduces unneccesary variable assignments
                USER.Username, USER.Password, USER.Row, USER.Session_Scores = USERNAME, CHECKPASSWORD, Row, Session_Scores
                
def IntroScreen():
    Message.LoadingScreen()
    MessageLog = ["Hit any key to begin entering..."]
    LoginProcess(MessageLog)
    Animation.FlipBook()
    
MainGameMusicLoop = Music('MainGameLoop', -1)
IntroScreen()
