grammar ISISAdj;

// Line format: Interface System Level State Hold (secs)
// line: Interface Whitespace Hostname Whitespace Level Whitespace State Whitespace Hold;
inputs : line+ EOF;
line: Interface Whitespace Hostname Whitespace Level Whitespace State Whitespace Hold Whitespace Addr Whitespace? Newline;


// Higher Order tokens
Interface: 'ae' Number Dot Number;
Hostname: Word Number Dot Word Number ;
Addr :
  F_Hex F_Hex ':'
  F_Hex F_Hex ':'
  F_Hex F_Hex ':'
  F_Hex F_Hex ':'
  F_Hex F_Hex ':'
  F_Hex F_Hex
;


// Lower order Parser rules.
Whitespace : F_Whitespace+;
Newline : F_Newline;
Dot: F_Dot;
Dash: F_Dash;
Level: F_Level ;
State: F_Up | F_Down;
Hold: Number;
Word: F_Letter+ ;
Number: F_Digit+ ;


// Fragments
fragment F_Letter : [a-zA-Z] ;
fragment F_Digit: [0-9] ;
fragment F_Whitespace : ' ' | '\t' ;
fragment F_Newline : '\r' '\n'? | '\n';
fragment F_Dot: '.' ;
fragment F_Dash: '-';
fragment F_Colon: ':';
fragment F_Up: 'Up';
fragment F_Down: 'Down';
fragment F_Level: [12] ; 
fragment F_Hex: [A-Fa-f0-9];


// Fallthrough match so all input is tokenized correctly.
InputToIgnore : ':' | '(' | ')' ;
