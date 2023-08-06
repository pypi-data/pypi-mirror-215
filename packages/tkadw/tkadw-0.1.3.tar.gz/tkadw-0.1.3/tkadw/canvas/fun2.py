from tkinter import *


root = Tk()
root.eval("""
# vectorgraphics.tcl

package require Tk
bind [winfo class .] <Destroy> exit

#
# Elementary mouse actions: select, move
#

namespace eval ::canvasEditorBindings {
  variable canvasMouse ""
  namespace import ::tcl::mathop::*
  namespace export canvasEditor
}

proc ::canvasEditorBindings::canvasEditor {canvas args} {
  variable canvasMouse
  dict set canvasMouse $canvas motion "0 0"
  dict set canvasMouse $canvas action press
  ::canvas $canvas {*}$args
  createContextMenu $canvas
  canvasBindings $canvas on
  canvasBindingsSelect $canvas on
  ::set canvas
}

namespace import ::canvasEditorBindings::canvasEditor

proc ::canvasEditorBindings::canvasBindings {canvas {onOff on}} {
  variable canvasMouse
  dict set canvasMouse $canvas motion "0 0"
  dict set canvasMouse $canvas action press
  dict set canvasMouse $canvas current ""
  if {$onOff} then {
    bind $canvas <1> {
      apply {
        {canvas x y} {
          variable canvasMouse
          dict set canvasMouse $canvas position\
            "[$canvas canvasx $x] [$canvas canvasy $y]"
          dict set canvasMouse $canvas selStart\
            "[$canvas canvasx $x] [$canvas canvasy $y]"
          dict set canvasMouse $canvas action press
          set current [$canvas find withtag current]
          dict set canvasMouse $canvas current $current
          if {$current eq ""} then {
            # $canvas dtag all sel
            canvasUnselect $canvas all
          }
        } ::canvasEditorBindings
      } %W %x %y
    }
    bind $canvas <B1-Motion> {
      apply {
        {canvas x y} {
          variable canvasMouse
          lassign [dict get $canvasMouse $canvas position] x0 y0
          set x1 [$canvas canvasx $x]
          set y1 [$canvas canvasy $y]
          dict set canvasMouse $canvas motion "[- $x1 $x0] [- $y1 $y0]"
          dict set canvasMouse $canvas position "$x1 $y1"
          dict set canvasMouse $canvas action move
          if {[dict get $canvasMouse $canvas current] eq ""} then {
            if {[$canvas find withtag selRect] eq ""} then {
              $canvas create rectangle 10 10 100 100\
                -dash "_    " -tags selRect
            }
            $canvas coords selRect "[dict get $canvasMouse $canvas selStart] $x1 $y1"
          }
        } ::canvasEditorBindings
      } %W %x %y
    }
    bind $canvas <ButtonRelease> {
      apply {
        canvas {
          if {[$canvas find withtag selRect] ne ""} then {
            # $canvas dtag all sel
            # $canvas addtag sel enclosed {*}[$canvas coords selRect]
            canvasSelect $canvas enclosed {*}[$canvas coords selRect]
            $canvas delete selRect
          }
        } ::canvasEditorBindings
      } %W
    }
  } else {
    bind $canvas <1> ""
    bind $canvas <B1-Motion> ""
    bind $canvas <ButtonRelease> ""
  }
}

proc ::canvasEditorBindings::canvasSelect {canvas tagOrItem args} {
  if {$args ne ""} then {
    $canvas addtag sel $tagOrItem {*}$args
  } else {
    $canvas addtag sel withtag $tagOrItem
  }
  foreach item [$canvas find withtag sel] {
    $canvas itemconfigure $item -stipple gray50
    # if {[$canvas type $item] ne "line"} then
    catch {
      $canvas itemconfigure $item -outlinestipple gray50
    }
  }
}

proc ::canvasEditorBindings::canvasUnselect {canvas tagOrItem} {
  $canvas itemconfigure $tagOrItem -stipple {}
  foreach item [$canvas find withtag $tagOrItem] {
    # if {[$canvas type $item] ni {line}} then
    catch {
      $canvas itemconfigure $item -outlinestipple {}
    }
  }
  $canvas dtag $tagOrItem sel
}

proc ::canvasEditorBindings::createContextMenu canvas {
  set colors {white black red green blue yellow}
  destroy $canvas.context
  menu $canvas.context -tearoff no
  #
  $canvas.context add cascade -label Edit\
    -menu [menu $canvas.context.edit -tearoff no]
  $canvas.context.edit add command -label Coordinates\
    -command "canvasEditorBindings::canvasEditItemCoords $canvas current"
  #
  $canvas.context.edit add cascade -label Fill\
    -menu [menu $canvas.context.edit.fill -tearoff no]
  foreach color $colors {
    $canvas.context.edit.fill add command -label [string totitle $color] -command "
      $canvas itemconfigure current -fill $color
    "
  }
  $canvas.context.edit.fill add command -label Transparent -command [list apply {
      canvas {
        $canvas itemconfigure current -fill ""
      }
    } $canvas]
  $canvas.context.edit.fill add separator
  $canvas.context.edit.fill add command -label Choose -command [list apply {
      {canvas item} {
        set currentColor [$canvas itemcget $item -fill]
        if {$currentColor ne ""} then {
          set newColor [tk_chooseColor -initialcolor $currentColor]
        } else {
          set newColor [tk_chooseColor]
        }
        if {$newColor ne ""} then {
          $canvas itemconfigure $item -fill $newColor
        }
      }
    } $canvas current]
  #
  $canvas.context.edit add cascade -label Outline\
    -menu [menu $canvas.context.edit.outline -tearoff  no]
  foreach color $colors {
    $canvas.context.edit.outline add command -label [string totitle $color]\
      -command "catch {[subst -nocommand {
            if {[$canvas type current] eq {line}} then {
              $canvas itemconfigure current -fill $color
            } else {
              $canvas itemconfigure current -outline $color
            }
          }]}"
  }
  $canvas.context.edit.outline add command -label Transparent -command "catch {
      $canvas itemconfigure current -outline {}
    }"
  $canvas.context.edit.outline add separator
  $canvas.context.edit.outline add command -label Choose -command [list apply {
      {canvas item} {
        if {[$canvas type $item] eq "line"} then {
          set outline -fill
        } else {
          set outline -outline
        }
        set currentColor [$canvas itemcget $item $outline]
        if {$currentColor ne ""} then {
          set newColor [tk_chooseColor -initialcolor $currentColor]
        } else {
          set newColor [tk_chooseColor]
        }
        if {$newColor ne ""} then {
          $canvas itemconfigure $item $outline $newColor
        }
      }
    } $canvas current]
  #
  $canvas.context.edit add cascade -label Linewidth\
    -menu [menu $canvas.context.edit.width -tearoff no]
  for {set i 0} {$i <= 10} {incr i} {
    $canvas.context.edit.width add command -label $i\
      -command "$canvas itemconfigure current -width $i"
  }
  #
  $canvas.context.edit add cascade -label Joinstyle\
    -menu [menu $canvas.context.edit.joinstyle -tearoff no]
  foreach style {bevel miter round} {
    $canvas.context.edit.joinstyle add command -label [string totitle $style]\
      -command "catch {
        $canvas itemconfigure current -joinstyle $style
      }"
  }
  #
  $canvas.context.edit add cascade -label Capstyle\
    -menu [menu $canvas.context.edit.capstyle -tearoff no]
  foreach style {butt round projecting} {
    $canvas.context.edit.capstyle add command -label [string totitle $style]\
      -command "catch {
        $canvas itemconfigure current -capstyle $style
      }"
  }
  #
  $canvas.context add cascade -label Create\
    -menu [menu $canvas.context.create -tearoff no]
  $canvas.context.create add command -label Line\
    -command "::canvasEditorBindings::canvasCreate $canvas line"
  $canvas.context.create add command -label Rectangle\
    -command "::canvasEditorBindings::canvasCreate $canvas rectangle"
  $canvas.context.create add command -label Oval\
    -command "::canvasEditorBindings::canvasCreate $canvas oval"
  $canvas.context.create add command -label Polygon\
    -command "::canvasEditorBindings::canvasCreate $canvas polygon"
  #
  $canvas.context add separator
  $canvas.context add command -label Raise -command "$canvas raise current"
  $canvas.context add command -label Lower -command "$canvas lower current"
  $canvas.context add command -label Delete -command "$canvas delete current"
}

proc ::canvasEditorBindings::canvasBindingsSelect {canvas {onOff on}} {
  if {$onOff} then {
    bind $canvas <3> {
      apply {
        {canvas x y} {
          if {[$canvas find withtag current] eq ""} then {
            tk_popup $canvas.context.create $x $y
          } else {
            tk_popup $canvas.context $x $y
          }
        } ::canvasEditorBindings
      } %W %X %Y
    }
    $canvas bind sel <Button-1><B1-Motion> {
      apply {
        canvas {
          variable canvasMouse
          $canvas move sel {*}[dict get $canvasMouse $canvas motion]
        } ::canvasEditorBindings
      } %W
    }
    $canvas bind current <Button-1> {
      apply {
        canvas {
          variable canvasMouse
          if {[dict get $canvasMouse $canvas action] eq "press"} then {
            # $canvas dtag all sel
            canvasUnselect $canvas all
          }
          # $canvas addtag sel withtag current
          canvasSelect $canvas current
        } ::canvasEditorBindings
      } %W
    }
    $canvas bind current <Shift-1> {
      apply {
        canvas {
          variable canvasMouse
          # %W addtag sel withtag current
          if {"sel" in [$canvas gettags current]} then {
            canvasUnselect $canvas current
          } else {
            canvasSelect $canvas current
          }
        } ::canvasEditorBindings
      } %W
    }
  } else {
    bind $canvas <3> ""
    $canvas bind sel <Button-1><B1-Motion> ""
    $canvas bind current <Button-1> ""
    $canvas bind current <Shift-1> ""
  }
}

proc ::canvasEditorBindings::canvasCreate {canvas {line line}} {
  variable canvasMouse
  canvasBindings $canvas off
  canvasBindingsSelect $canvas off
  # $canvas dtag all sel
  canvasUnselect $canvas all
  bind $canvas <Button-1> [list apply {
      {canvas line x y} {
        variable canvasMouse
        dict set canvasMouse $canvas selStart "[$canvas canvasx $x] [$canvas canvasy $y]"
        $canvas create $line\
          "[$canvas canvasx $x] [$canvas canvasy $y]\
             [$canvas canvasx $x] [$canvas canvasy $y]"\
          -width 5 -tags sel
        if {$line in {polygon oval rectangle arc}} then {
          $canvas itemconfigure sel -outline black -fill white
        }
      } ::canvasEditorBindings
    } %W $line %x %y]
  bind $canvas <B1-Motion> [list apply {
      {canvas x y} {
        variable canvasMouse
        $canvas coords sel {*}[dict get $canvasMouse $canvas selStart]\
          [$canvas canvasx $x] [$canvas canvasy $y]
      } ::canvasEditorBindings
    } %W %x %y]
  bind $canvas <B1-Motion><ButtonRelease> [list apply {
      canvas {
        bind $canvas <1> ""
        bind $canvas <B1-Motion> ""
        bind $canvas <B1-Motion><ButtonRelease> ""
        canvasEditItemCoords $canvas sel on
        if {[$canvas type sel] in {polygon}} then {
          addCoord $canvas sel 0
        }
      } ::canvasEditorBindings
    } %W]
}

proc ::canvasEditorBindings::canvasEditItemCoords {canvas item {onOff on}} {
  if {$onOff} then {
    #
    destroy $canvas.context.handle
    menu $canvas.context.handle -tearoff no
    #
    set item [$canvas find withtag $item]
    canvasUnselect $canvas all
    canvasSelect $canvas $item
    canvasBindings $canvas off
    canvasBindingsSelect $canvas off
    set i -1
    foreach {x y} [$canvas coords $item] {
      createCoordHandle $canvas $item [incr i]
    }
    #
    destroy $canvas.context.done
    menu $canvas.context.done -tearoff no
    $canvas.context.done add command -label done\
      -command "::canvasEditorBindings::canvasEditItemCoords $canvas $item off"
    bind $canvas <3> [subst -nocommand {
        if {[$canvas find withtag current&&handle] eq ""} then {
          tk_popup $canvas.context.done %X %Y
        }
      }]
  } else {
    bind $canvas <3> ""
    destroy $canvas.context.done
    $canvas delete handle
    canvasBindings $canvas on
    canvasBindingsSelect $canvas on
  }
}

proc ::canvasEditorBindings::createCoordHandle {canvas item count} {
  set i [* $count 2]
  set j [+ $i 1]
  set coords [$canvas coords $item]
  set x [lindex $coords $i]
  set y [lindex $coords $j]
  set handle [$canvas create oval [list [- $x 5] [- $y 5] [+ $x 5] [+ $y 5]]\
                -fill white -outline black -tags handle]
  $canvas bind $handle <Button-1> [subst -nocommand {
      %W delete handle
      bind $canvas <Button-1><B1-Motion> {
        $canvas coords $item\
          [lreplace [$canvas coords $item] $i $j\
             [$canvas canvasx %%x] [$canvas canvasy %%y]]
      }
      bind $canvas <ButtonRelease> {
        bind $canvas <Button-1><B1-Motion> ""
        bind $canvas <ButtonRelease> ""
        ::canvasEditorBindings::canvasEditItemCoords $canvas $item on
      }
    }]
  if {[$canvas type $item] in {line polygon}} then {
    $canvas.context.handle add cascade -label $count\
      -menu [menu $canvas.context.handle.$count -tearoff no]
    $canvas.context.handle.$count add command -label Add\
      -command "::canvasEditorBindings::addCoord $canvas $item $count"
    $canvas.context.handle.$count add command -label Delete\
      -command "::canvasEditorBindings::delCoord $canvas $item $count"
    $canvas.context.handle.$count add separator
    $canvas.context.handle.$count add command -label Linear\
      -command "$canvas itemconfigure $item -smooth false"
    $canvas.context.handle.$count add command -label Spline\
      -command "$canvas itemconfigure $item -smooth true"
    $canvas.context.handle.$count add command -label Bézier\
      -command "$canvas itemconfigure $item -smooth raw"
    $canvas bind $handle <Button-3> "
      tk_popup $canvas.context.handle.$count %X %Y
    "
  }
}

proc ::canvasEditorBindings::addCoord {canvas item count} {
  canvasEditItemCoords $canvas $item off
  set coords [$canvas coords $item]
  if {($count+1) * 2 < [llength $coords]} then {
    set li [lrange $coords [* $count 2] [+ [* $count 2] 3]]
  } else {
    lappend li\
      [lindex $coords end-1] [lindex $coords end] [lindex $coords 0] [lindex $coords 1]
  }
  lassign $li x0 y0 x1 y1
  set x [/ [+ $x0 $x1] 2]
  set y [/ [+ $y0 $y1] 2]
  if {($count+1) * 2 < [llength $coords]} then {
    set newCoords [lreplace $coords [* [+ $count 1] 2] [- [* [+ $count 1] 2] 1] $x $y] 
  } else {
    set newCoords [concat $coords $x $y]
  }
  $canvas coords $item $newCoords
  canvasEditItemCoords $canvas $item on
}

proc ::canvasEditorBindings::delCoord {canvas item count} {
  set type [$canvas type $item]
  if {$type ni {line polygon}} then return
  set coords [$canvas coords $item]
  if {$type eq "line" && [llength $coords] <= 4} then return
  if {$type eq "polygon" && [llength $coords] <= 6} then return
  #
  canvasEditItemCoords $canvas $item off
  $canvas coords $item [lreplace $coords [* $count 2] [+ [* $count 2] 1]]
  canvasEditItemCoords $canvas $item on
}

if true then {
  pack [canvasEditor .c] -expand yes -fill both
  .c create rectangle 10 10 100 100 -fill yellow
  .c create oval 50 50 150 150 -fill red
  .c itemconfigure all -width 5
}
""")
root.mainloop()