
set filename "day10.txt"
if {[llength $argv] > 0} {
    set filename [lindex $argv 0]
}
set fp [open $filename r]
set data [read $fp]
close $fp

set lines [split $data "\n"]
set lines [lrange $lines 0 end-1]

set jolts [lsort -integer $lines]

set diffs [list 3]
set prev 0
for {set i 0} {$i < [llength $jolts]} {incr i} {
    set count [lindex $jolts $i]
    set diff [expr $count - $prev]
    lappend diffs $diff
    set prev $count 
}

set counts [list]
foreach diff $diffs {
    if {![dict exists $counts $diff]} {
        dict set counts $diff 0
    }
    set count [dict get $counts $diff]
    dict set counts $diff [expr $count + 1]
}

puts "part 1 answer => [expr [dict get $counts 1] * [dict get $counts 3]]"

set jolts "0 $jolts"
set branches [list 1]
for {set i 1} {$i < [llength $jolts]} {incr i} {
    set count 0
    for {set j 0} {$j < $i} {incr j} {
        if {([lindex $jolts $i] - [lindex $jolts $j]) <= 3} {
            set count [expr $count + [lindex $branches $j]]
        }
    }

    lappend branches $count
}

puts "part 2 answer => [lindex $branches end]"
