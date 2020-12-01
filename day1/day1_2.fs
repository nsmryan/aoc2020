32 constant max-line
create buffer max-line cells allot
variable line-len

variable file

variable num-expenses  0 num-expenses !
variable index0
variable index1
variable index2

create expenses 201 cells allot

: +1 dup @ 1 + swap ! ;
: .. dup . ;
: index cells expenses + ;

: pexpenses num-expenses @ 0 ?do i index @ . loop ;

: open s" day1.txt" r/o open-file throw file ! ;
: line buffer max-line file @ read-line throw swap line-len ! ;
: place num-expenses @ index ! num-expenses +1 ;
: read begin line while buffer line-len @ s>number? 0 <> if drop place then repeat ;


: check index @ rot index @ rot index @ + + 2020 = ;
: find num-expenses @ 0 ?do
       num-expenses @ i ?do
       num-expenses @ j ?do
       i j k check if i index0 ! j index1 ! k index2 ! then
       loop loop loop ;

( : answer index rot index rot index * * ; )
: answer index0 @ index @  index1 @ index @  index2 @ index @  * * ;
: calculate find answer ;

: solve open read calculate . ;

