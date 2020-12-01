set defaults {"" 1 1000}
set args [concat $argv [lrange $defaults [llength $argv] end]]

lassign $args filename scale rate
if {[string equal $filename ""]} {
    puts "Please provide a ppm file!"
    exit
}

set fp [open $filename r]
set data [read $fp]
close $fp

# remove comments
regsub -all {#[^\n]*\n} $data " " data
lassign $data type w h depth
set data [lrange $data 4 end]

if {![string equal $type P3]} {
    puts "$filename type was $type, but expected P3"
    exit
}

proc hexcolor {r g b} {
    global depth
    return [format "#%02x%02x%02x" [expr (255 * $r)/$depth] [expr (255 * $g)/$depth] [expr (255 * $b)/$depth]]
}

set running 0

set c [canvas .c -width [expr $scale * $w] -height [expr $scale * $h] -bg black]
pack $c

proc display {} {
    global running data w h c scale

    $c create rectangle 0 0 [expr $w * $scale] [expr $h * $scale] -fill black
    for {set y 0} {$y < $h} {incr y} {
        for {set x 0} {$x < $w} {incr x} {
            set offset [expr 3 * ($x + ($y * $w))]
            set r [lindex $data [expr $offset + 0]]
            set g [lindex $data [expr $offset + 1]]
            set b [lindex $data [expr $offset + 2]]
            set xpos [expr $x * $scale]
            set ypos [expr $y * $scale]
            set color [hexcolor $r $g $b]
            $c create rectangle $xpos $ypos [expr $xpos + $scale] [expr $ypos + $scale] -fill $color
        }
    }

    set data [lrange $data [expr 3 * $w * $h] end]
    if {[llength $data] == 0} {
        set running 0
    }

    update
}

proc every {ms body} {
    eval $body; after $ms [namespace code [info level 0]]
}

every $rate display
vwait running
after $rate

exit
