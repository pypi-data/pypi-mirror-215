 # poly.tcl

 proc poly_round {win outline fill args} {
     if {[llength $args] % 3 != 0 || [llength $args] < 9} {
         error "wrong # args: should be \"poly_round\
                 win outline fill x1 y1 d1 x2 y2 d2 x3 y3 d3 ?...?\""
     }

     # Determine the tag to use.
     if {![info exists ::poly_next_id]} {
         set ::poly_next_id 1
     }
     set tag poly#$::poly_next_id
     incr ::poly_next_id

     # Filter out illegal circles and collinear points.
     set pts [list]
     lassign [lrange $args 0 4] Ux Uy d Vx Vy
     foreach {d Wx Wy} [concat [lrange $args 5 end] [lrange $args 0 4]] {
         set test [expr {$Ux * ($Vy - $Wy) - $Vx * ($Uy - $Wy) +
                 $Wx * ($Uy - $Vy)}]
         if {($d > 0) && $test != 0} {
             lappend pts $Vx $Vy $d $test
             lassign [list $Wx $Wy $Vx $Vy] Vx Vy Ux Uy
         } else {
             lassign [list $Wx $Wy] Vx Vy
         }
     }

     # V    C    T   W
     #  *---*----*-+-*-- Given: U, V, W, d
     #  |\ /    /|_|     Find:  S, E, T
     #  | *B   / |
     #  |/ \  /  |       The length of ES and ET each is d.
     # A*   \/   |
     #  |   /\   |       VB bisects angle UVW.  SE _|_ VU; TE _|_ VW.
     #  |  /  \  |       B is halfway between A and C.
     #  | /    \ |       Angles UVW and SET are not necessarily right.
     #  |/      \|       The length of AV and CV each is 1.
     # S*-+------*E
     #  |_|       \      The new polygon is along USTW. 
     # U*          \     The new arc has center E, radius d, and angle SET, and
     #  |           \    it is tangential to VU at S and VW at T.

     # Calculate new polygon vertices and create arcs.
     set coords [list]
     lassign [lrange $pts 0 5] Ux Uy d test Vx Vy
     foreach {d test Wx Wy} [concat [lrange $pts 6 end] [lrange $pts 0 5]] {
         # Find A and C.
         foreach {pt x y} [list A $Ux $Uy C $Wx $Wy] {
             set      k [expr {sqrt(($Vx - $x) ** 2 + ($Vy - $y) ** 2)}]
             set ${pt}x [expr {($x - $Vx) / $k + $Vx}]
             set ${pt}y [expr {($y - $Vy) / $k + $Vy}]
         }

         # Find B.
         set Bx [expr {($Ax + $Cx) / 2.0}]
         set By [expr {($Ay + $Cy) / 2.0}]

         # Find the parameters for lines VB and VW.
         foreach {pt x y} [list B $Bx $By W $Wx $Wy] {
             set       k [expr {sqrt(($Vx - $x) ** 2 + ($Vy - $y) ** 2)}]
             set V${pt}a [expr {+($Vy - $y) / $k}]
             set V${pt}b [expr {-($Vx - $x) / $k}]
             set V${pt}c [expr {($Vx * $y - $Vy * $x) / $k}]
         }

         # Find point E.
         set sign [expr {$test < 0 ? -1 : +1}]
         set  k [expr {$VWa * $VBb - $VWb * $VBa}]
         set Ex [expr {(+$VWb * $VBc - ($VWc - $d * $sign) * $VBb) / $k}]
         set Ey [expr {(-$VWa * $VBc + ($VWc - $d * $sign) * $VBa) / $k}]

         # Find tangent points S and T.
         foreach {pt x y} [list S $Ux $Uy T $Wx $Wy] {
             set      k [expr {($Vx - $x) ** 2 + ($Vy - $y) ** 2}]
             set ${pt}x [expr {($Ex * ($Vx - $x) ** 2 + ($Vy - $y) *
                               ($Ey * ($Vx - $x) - $Vx * $y + $Vy * $x)) / $k}]
             set ${pt}y [expr {($Ex * ($Vx - $x) * ($Vy - $y) +
                               ($Ey * ($Vy - $y) ** 2 + ($Vx - $x) *
                               ($Vx * $y - $Vy * $x))) / $k}]
         }

         # Find directions for lines ES and ET.
         foreach {pt x y} [list S $Sx $Sy T $Tx $Ty] {
             set E${pt}d [expr {atan2($Ey - $y, $x - $Ex)}]
         }

         # Find start and extent directions.
         if {$ESd < 0 && $ETd > 0} {
             set start  [expr {180 / acos(-1) * $ETd}]
             set extent [expr {180 / acos(-1) * ($ESd - $ETd)}]
             if {$sign > 0} {
                 set extent [expr {$extent + 360}]
             }
         } else {
             set start  [expr {180 / acos(-1) * $ESd}]
             set extent [expr {180 / acos(-1) * ($ETd - $ESd)}]
             if {$sign < 0 && $ESd > 0 && $ETd < 0} {
                 set extent [expr {$extent + 360}]
             }
         }

         # Draw arc.
         set opts [list                             \
                 [expr {$Ex - $d}] [expr {$Ey - $d}]\
                 [expr {$Ex + $d}] [expr {$Ey + $d}]\
                 -start $start -extent $extent]
         $win create arc {*}$opts -style pie -tags [list $tag pie]
         $win create arc {*}$opts -style arc -tags [list $tag arc]

         # Draw border line.
         if {[info exists prevx]} {
             $win create line $prevx $prevy $Sx $Sy -tags [list $tag line]
         } else {
             lassign [list $Sx $Sy] firstx firsty
         }
         lassign [list $Tx $Ty] prevx prevy

         # Remember coordinates for polygon.
         lappend coords $Sx $Sy $Tx $Ty

         # Rotate vertices.
         lassign [list $Wx $Wy $Vx $Vy] Vx Vy Ux Uy
     }

     # Draw final border line.
     $win create line $prevx $prevy $firstx $firsty -tags [list $tag line]

     # Draw fill polygon.
     $win create polygon {*}$coords -tags [list $tag poly]

     # Configure colors.
     $win itemconfigure $tag&&(poly||pie) -fill $fill
     $win itemconfigure $tag&&pie         -outline ""
     $win itemconfigure $tag&&line        -fill $outline -capstyle round
     $win itemconfigure $tag&&arc         -outline $outline

     # Set proper stacking order.
     $win raise $tag&&poly
     $win raise $tag&&pie
     $win raise $tag&&(line||arc)

     return $tag
 }

 # vim: set ts=4 sts=4 sw=4 tw=80 et ft=tcl:
