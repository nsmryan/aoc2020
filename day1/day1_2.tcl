
set fp [open "day1.txt" r]
set data [read $fp]
close $fp

for {set i 0} {$i < [llength $data]} {incr i} {
    for {set j $i} {$j < [llength $data]} {incr j} {
        for {set k $j} {$k < [llength $data]} {incr k} {
            set sum [expr ([lindex $data $i] + [lindex $data $j] + [lindex $data $k])]
            if {$sum == 2020} {
                set prod [expr [lindex $data $i] * [lindex $data $j] * [lindex $data $k]]
                puts $prod
                exit
            }
        }
    }
}

exit

