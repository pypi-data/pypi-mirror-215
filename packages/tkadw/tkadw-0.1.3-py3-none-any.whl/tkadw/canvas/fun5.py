from tkinter import *


root = Tk()
root.eval("""
proc roundRect2 {w L T Rad width height colour tag} {

  $w create oval $L $T [expr $L + $Rad] [expr $T + $Rad] -fill $colour -outline $colour -tag $tag
  $w create oval [expr $width-$Rad] $T $width [expr $T + $Rad] -fill $colour -outline $colour -tag $tag
  $w create oval $L [expr $height-$Rad] [expr $L+$Rad] $height -fill $colour -outline $colour -tag $tag
  $w create oval [expr $width-$Rad] [expr $height-$Rad] [expr $width] $height -fill $colour -outline $colour -tag $tag
  $w create rectangle [expr $L + ($Rad/2.0)] $T [expr $width-($Rad/2.0)] $height -fill $colour -outline $colour -tag $tag
  $w create rectangle $L [expr $T + ($Rad/2.0)] $width [expr $height-($Rad/2.0)] -fill $colour -outline $colour -tag $tag

}
""")

canvas = Canvas()

root.eval(f"roundRect2 {canvas} 15 15 30 100 100 black 2")

canvas.pack(fill="both", expand="yes")


root.mainloop()