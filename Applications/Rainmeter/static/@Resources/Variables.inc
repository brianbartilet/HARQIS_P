[Variables]
; =========================================
; GMail may require you to enable "Allow less secure apps" on your account
; You must set these 2 variables before the GMail skin will work
; Set GMailUser to your GMail address without the "@gmail.com"
GMailUser={GMailUsername}
;Not Setup
; Set GMailPassword to your GMail password
GMailPassword={GMailPassword}

; To set additional GMail Accounts, add an increasing number to the above variables
; Increase #ItemLines# variable in GMail.ini to the number of accounts
; Set GMailUser2 to your GMail address without the "@gmail.com"
GMailUser2={GMailUsername2}
; Set GMailPassword2 to your GMail password
GMailPassword2={GMailPassword2}

; =========================================
; Set the PlayerInterface variable below to one of the following players
; AIMP: PlayerInterface=AIMP
; Fully supported. Tested with AIMP 2.61.

; foobar2000: PlayerInterface=CAD
; Fully supported. The foo_cad plugin (download) needs to be installed.

; iTunes: PlayerInterface=iTunes
; Fully supported. Tested with iTunes 10.2.

; J. River Media Center and Media Jukebox: PlayerInterface=CAD
; Fully supported through the CAD interface with Media Center 19 and later. 
; More information here.

; MediaMonkey: PlayerInterface=MediaMonkey
; Fully supported. Tested with MediaMonkey 3.2.5.

; MusicBee: PlayerInterface=CAD
; Fully supported. MusicBee 1.2 (or higher) is required.

; Spotify: PlayerInterface=Spotify
; Not tested

; Winamp: PlayerInterface=Winamp
; Fully supported.

; WMP: PlayerInterface=WMP

PlayerInterface=Winamp

activePlugin=NowPlaying
; 0 = MUSIC, 1=GPMDP, 2 = WEBNOWPLAYING
MusicSwitch=0
Plugin0=Now-Playing
Plugin1=Google-Play-Music
Plugin2=Web-Now-Playing

playerController=Title0
currentlySetName=Winamp
currentlySetPlayer=Winamp

; =========================================
; User Colors {You can change these but the Options skin will overwrite when used}
BGAlpha=180
lightColor=220,220,220
darkColor=30,30,30
alertColor=255,0,0
warnColor=255,255,0
textColor=[#lightColor]
linkColor=255,217,120,255
alttextColor=[ChamFG1]
;[#lightColor]
; [*#Win8Color] or [#AeroColor]
fillColor=0,0,0,100
headerColor=[#AccentColor],#BGAlpha#
;[#AccentColor],#BGAlpha#
; Separator/Bar Color
colorBar=[ChamFG1]
;235,170,0,255
; default bar color: 235,170,0,255
SkinPositionColor=0

; =========================================
; World Time Locations
;
; You have to set locations here.
; There has been a change on the website, so this becomes a little more difficult.
; Go to https://time.yandex.com/
; Add a city you like.
; Move mouse over that city. Click the gear icon.
; Click "Informer".
; Look at the displayed code. Copy the number after "geoid=" for each city, one at a time, and replace the number code after each 'Location#=' below.
; Save this file. Refresh or Unload/Load the skin

Location1=200
;Los Angeles

Location2=202
;New York

Location3=10393
;London

Location4=213
;Moscow

Location5=10619
;Singapore

; Location6=21265
; ;Melbourne

; =========================================
; Font
fontName=Consolas
textSize=8

; =========================================
; SysColors Variables { ** DO NOT EDIT ** }
AccentColor=[&mAccent]
MenuTextColor=[&ChamBG1]
;[&mMenuText]
Win8Color=[&mWin8]
AeroColor=[&mAero]
HighlightColor=[&mHighlight]
MenuColor=[&mMenu]
; Common Skin Variables { ** DO NOT EDIT ** }
U=[!UpdateMeter *][!Redraw]
; Scale values 1~3
Scale=1.2


