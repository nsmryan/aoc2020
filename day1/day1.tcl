
set fp [open "day1.txt" r]
set data [read $fp]
close $fp

for {set i 0} {$i < [llength $data]} {incr i} {
    for {set j $i} {$j < [llength $data]} {incr j} {
        if {([lindex $data $i] + [lindex $data $j]) == 2020} {
            puts [expr [lindex $data $i] * [lindex $data $j]]
            exit
        }
    }
}

exit

