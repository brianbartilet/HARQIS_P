; ----------------------------------

[Metadata]
; Contains basic information of the skin.
Name=SysColor Include
Description=This skin includes measures common to all skin
License=Creative Commons BY-NC-SA 4.0
Version=1.2020.08.12

[mWIN8]
Measure=Plugin
Plugin=SysColor
ColorType=Win8
DisplayType=RGB

[mAERO]
Measure=Plugin
Plugin=SysColor
ColorType=Aero

[mAccent]
Measure=Plugin
Plugin=SysColor
ColorType=DWM_COLOR

[mHighlight]
Measure=Plugin
Plugin=SysColor
ColorType=ACTIVECAPTION

[mMenu]
Measure=Plugin
Plugin=SysColor
ColorType=Menu

[mMenuText]
Measure=Plugin
Plugin=SysColor
ColorType=MenuText

[MeasureScaleIt]
Measure=Plugin
Plugin=ActionTimer
ActionList1=ScaleUp
ScaleUp=[!SetVariable Scale "(Clamp(#Scale#+0.05,1,3))"][!WriteKeyValue Variables Scale "(Clamp(#Scale#+0.05,1,3))" "#@#Variables.inc"][!RefreshGroup "#RootConfig#"]
ActionList2=ScaleDown
ScaleDown=[!SetVariable Scale "(Clamp(#Scale#-0.05,1,3))"][!WriteKeyValue Variables Scale "(Clamp(#Scale#-0.05,1,3))" "#@#Variables.inc"][!RefreshGroup "#RootConfig#"]
DynamicVariables=1

[ChameleonDesktop]
Measure=Plugin
Plugin=Chameleon
Type=Desktop
Format=Dec
ContextAwareColors=#SkinPositionColor#

[ChamFG1]
Measure=Plugin
Plugin=Chameleon
Parent=ChameleonDesktop
Color=Foreground1
Format=Dec

[ChamFG2]
Measure=Plugin
Plugin=Chameleon
Parent=ChameleonDesktop
Color=Foreground2
Format=Dec

[ChamBG1]
Measure=Plugin
Plugin=Chameleon
Parent=ChameleonDesktop
Color=Background1
Format=Dec

[ChamBG2]
Measure=Plugin
Plugin=Chameleon
Parent=ChameleonDesktop
Color=Background2
Format=Dec

