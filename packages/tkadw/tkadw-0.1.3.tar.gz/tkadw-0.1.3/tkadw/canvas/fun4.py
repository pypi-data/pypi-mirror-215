from tkinter import *


root = Tk()
root.eval("""
 package require Tcl 8.5
 package require Tk

 source [file join [file dirname [info script]] poly.tcl]

 proc draw {win} {
     global demo

     set sharp_pts [list]
     set round_pts [list]
     for {set id 0} {$id < $demo(num_pts)} {incr id} {
         set x [expr {([lindex [$win coords vtx#$id] 0] +
                       [lindex [$win coords vtx#$id] 2]) / 2}]
         set y [expr {([lindex [$win coords vtx#$id] 1] +
                       [lindex [$win coords vtx#$id] 3]) / 2}]
         lappend sharp_pts $x $y
         lappend round_pts $x $y $demo(radius)
     }

     .c delete sharp_poly
     .c create polygon {*}$sharp_pts -outline gray50 -fill ""\
             -dash {6 5} -tags {sharp_poly}

     if {[info exists demo(tag)]} {
         .c delete $demo(tag)
     }
     set demo(tag) [poly_round .c $demo(outline) $demo(fill) {*}$round_pts]
     .c itemconfigure $demo(tag) -width $demo(thickness)

     .c raise vtx
 }

 proc down {win x y} {
     global demo

     $win dtag selected
     $win addtag selected withtag current
     $win raise current
     set demo(last_x) $x
     set demo(last_y) $y
 }
 
 proc move {win x y} {
     global demo

     if {[info exists demo(last_x)]} {
         $win move selected\
                 [expr {$x - $demo(last_x)}]\
                 [expr {$y - $demo(last_y)}]
         set demo(last_x) $x
         set demo(last_y) $y

         draw $win
     }
 }

 proc main {args} {
     global demo

     array set demo {
         num_pts 3       radius 20      thickness 1
         outline black   fill   white   background gray
         width   400     height 400
     }
     foreach {option value} $args {
         set option [regsub {^-} $option ""]
         if {![info exists demo($option)]} {
             puts "Options: -[join [array names demo] " -"]"
             exit
         } else {
             set demo([regsub {^-} $option ""]) $value
         }
     }

     canvas .c -width $demo(width) -height $demo(height) -highlightthickness 0\
             -background $demo(background)
     pack .c
     wm title . "Round Polygon Demo"
     wm resizable . 0 0

     set 2pi [expr {2 * acos(-1)}]
     set cx [expr {$demo(width)  / 2}]; set sx [expr {$demo(width)  * 3 / 8}]
     set cy [expr {$demo(height) / 2}]; set sy [expr {$demo(height) * 3 / 8}]
     for {set id 0} {$id < $demo(num_pts)} {incr id} {
         set x [expr {$cx + $sx * cos(($id + 0.5) * $2pi / $demo(num_pts))}]
         set y [expr {$cy - $sy * sin(($id + 0.5) * $2pi / $demo(num_pts))}]
         .c create oval [expr {$x - 3}] [expr {$y - 3}]\
                        [expr {$x + 3}] [expr {$y + 3}]\
                        -tags [list vtx vtx#$id] -fill brown
     }

     .c bind vtx <Any-Enter> {.c itemconfigure current -fill red}
     .c bind vtx <Any-Leave> {.c itemconfigure current -fill brown}
     .c bind vtx <ButtonPress-1> {down .c %x %y}
     .c bind vtx <ButtonRelease-1> {.c dtag selected}
     bind .c <B1-Motion> {move .c %x %y}

     focus .c
     draw .c
 }

 main

""")
root.mainloop()