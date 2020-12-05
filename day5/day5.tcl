package require struct::set

set filename "day5.txt"
if {[llength $argv] > 0} {
    set filename [lindex $argv 0]
}
set fp [open $filename r]
set data [read $fp]
close $fp

set lines [split $data "\n"]

proc bintonum {bin one zero} {
    set num [string reverse $bin]
    set num [string map [list $one 1 $zero 0] $num]
    set num [binary format b* $num]
    binary scan $num c num
    return $num
}

set highest 0
foreach line $lines {
    if {[string length [string trim $line]] == 0} {
        continue
    }

    set row [string range $line 0 6]
    set row [bintonum $row B F]

    set col [string range $line 7 end]
    set col [bintonum $col R L]

    set seat [expr ($row * 8) + $col]
    puts "row $row col $col seat $seat"
    set highest [expr max($highest, $seat)]
}

puts $highest
