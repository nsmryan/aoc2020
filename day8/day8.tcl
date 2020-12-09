package require struct::set

set filename "day8.txt"
if {[llength $argv] > 0} {
    set filename [lindex $argv 0]
}
set fp [open $filename r]
set data [read $fp]
close $fp

set lines [split $data "\n"]
set lines [lrange $lines 0 end-1]


set ip 0
set seen ""
set accum 0

proc nop {arg} {
    global ip
    incr ip
}

proc jmp {arg} {
    global ip 

    set ip [expr $ip + $arg]
}

proc acc {arg} {
    global ip accum

    incr ip

    set accum [expr $accum + $arg]
}

proc run {lines} {
    global accum ip seen

    set accum 0
    set ip 0
    set seen ""

    while {1} {
        if {$ip == [llength $lines]} {
            return found
        }
       
        if {[struct::set contains $seen $ip]} {
            return forever
        }
        struct::set include seen $ip

        eval [lindex $lines $ip]

        #puts "($ip) $seen"
        #puts "ip $ip"
    }
}

proc swapop {line} {
    if {[string equal [lindex $line 0] "jmp"]} {
        return "nop [lindex $line 1]"
    }

    if {[string equal [lindex $line 0] "nop"]} {
        return "jmp [lindex $line 1]"
    }

    return $line
}

run $lines
puts "accum = $accum"

for {set i 0} {$i < [llength $lines]} {incr i} {
    set oldline [lindex $lines $i]
    set newline [swapop $oldline]
    if {[string equal $oldline $newline]} {
        puts "$i $oldline"
        continue
    }

    lset lines $i $newline
    set result [run $lines]
    lset lines $i $oldline

    puts "$i $result $accum"
    if {[string equal $result found]} {
        puts "i = $i"
        puts "accum = $accum"
        exit
    }
}

puts "Huh"
