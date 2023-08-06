from tkinter import *


Tk().eval("""
package require Tk

proc sprayDots { path dist {colour firebrick} } {
  set width  [$path cget -width]
  set height [$path cget -height]
  for { set x 0 } { $x <= $width } { incr x $dist } {
    for { set y 0 } { $y <= $height } { incr y $dist } {
      $path create rectangle $x $y $x $y -outline $colour -tag "dot_[set x]_[set y]"
    }
  }
}

proc coordinateSystem { path {colour firebrick} } {
  set width  [$path cget -width]
  set height [$path cget -height]
  set halfWidth  [expr {$width/2}]
  set halfHeight [expr {$height/2}]
  $path create line $halfWidth 0 $halfWidth $height -fill $colour \
    -arrow first -tag "vertical axis"
  $path create line 0 $halfHeight $width $halfHeight -fill $colour \
    -arrow last -tag "horizontal axis"
}

proc newCircle { path x1 y1 x2 y2 {colour firebrick} } {
global circles
  lappend circles [$path create oval $x1 $y1 $x2 $y2 -outline $colour]
}

proc inflate { path id } {
  set cc [$path coords $id]
  foreach {x1 y1 x2 y2} $cc break
  $path coords $id $x1 [expr {$y1-1}] [expr {$x2+2}] [expr {$y2+1}]
}

proc deleteOldest { path } {
global circles
  set id [lindex $circles 0]
  $path delete $id
  set circles [lreplace $circles 0 0]
}

proc mainLoop { path density interval howMany } {
global circles goOn
  set i 0
  while { $goOn } {
    if { [llength $circles] > $howMany } { deleteOldest $path }
    if { $i > $density } { set i 0 ; newCircle $path 50 250 50 250 }
    foreach id $circles { inflate $path $id }
    update
    after $interval
    incr i
  }
}

set canvasPath .c
pack [canvas $canvasPath -height 500 -width 500 -background black]
set id ""
set circles [list]
set goOn 1
bind . <Escape> { exit 0 }
wm protocol . WM_DELETE_WINDOW { set goOn 0 ; exit 0 }
sprayDots $canvasPath 25
coordinateSystem $canvasPath
newCircle $canvasPath 50 250 50 250
# Below: distance between circles 30 pixels, each 20ms new frame, 10 circles kept on canvas
mainLoop $canvasPath 29 20 10
""")