package require struct::set

set filename "day4.txt"
if {[llength $argv] > 0} {
    set filename [lindex $argv 0]
}
set fp [open $filename r]
set data [read $fp]
close $fp

# set data [regsub -all "\r" $data ""]
set lines [split $data "\n"]

set requirednames [lsort "byr iyr eyr hgt hcl ecl pid"]
set numrequired [llength $requirednames]

set count 0
set index 0
set line ""

proc check {passport} {
    set passport [regsub -all ":" $passport " "]
    global numrequired requirednames
    set names [lsort [dict keys $passport]]
    set names [lrange $names 0 $numrequired]

    set hasfields [struct::set subsetof $requirednames $names]

    set valid 0

    if {$hasfields} {
        set byr [dict get $passport byr]
        set validbyr [expr ([string length $byr] == 4) && ($byr >= 1920) && ($byr <= 2002)]

        set iyr [dict get $passport iyr]
        set validiyr [expr [string length $iyr] == 4 && $iyr >= 2010 && $iyr <= 2020]

        set eyr [dict get $passport eyr]
        set valideyr [expr [string length $eyr] == 4 && $eyr >= 2020 && $eyr <= 2030]

        set hgt [dict get $passport hgt]
        set validhgt 0
        if {[regexp {([0-9]+)cm} $hgt match cm]} {
            set validhgt [expr $cm >= 150 && $cm <= 193]
        }
        if {[regexp {([0-9]+)in} $hgt match in]} {
            set validhgt [expr $in >= 59 && $in <= 76]
        }

        set hcl [dict get $passport hcl]
        set validhcl [expr [string length $hcl] == 7 && [regexp {^#[0-9a-f]+$} $hcl]]

        set ecl [dict get $passport ecl]
        set validecl [expr [lsearch -exact "amb blu brn gry grn hzl oth" $ecl] != -1]

        set pid [dict get $passport pid]
        set validpid [expr [string length $pid] == 9 && [regexp {^[0-9]+$} $pid]]

        puts "$validbyr $validiyr $valideyr $validhgt $validhcl $validecl $validpid"
        set valid [expr $validbyr && $validiyr && $valideyr && $validhgt && $validhcl && $validecl && $validpid]
    }

    puts $passport
    puts ""

    return $valid
}

while {$index < [llength $lines]} {
    set curline [lindex $lines $index]
    set curline [string trim $curline]

    if {[llength $curline] != 0} {
        set line "$line $curline"
    } else {
        if {[llength $line] > 0} {
            if {[check $line]} {
                incr count
            }
            set line ""
        }
    }

    incr index
}

puts $count

exit

